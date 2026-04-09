from typing import List
from article import Article
from scrapers.scraper import Scraper
from dataclasses import dataclass
from datetime import datetime
from bs4 import BeautifulSoup
from progress import Progress


class BmvScraper(Scraper):

    SOURCE: str = "BMV"

    @dataclass
    class Parameters(Scraper.Parameters):
        pass

    def scrape(
        self, parameters: Scraper.Parameters, progress: Progress
    ) -> List[Article]:
        html_text = self._get(
            self._URL, progress, f"Fehler beim Scrapen der Quelle: {self.SOURCE}"
        )
        if html_text is None:
            return []

        soup = BeautifulSoup(html_text, "html.parser")

        urls = soup.find_all("a", {"class": "card-link"})
        articles = []
        for url in progress.start_iteration(
            urls, len(urls), "Scraping bmv articles..."
        ):
            link = f"{self._URL_PREFIX}{url.get('href')}"
            html_article = self._get(
                link, progress, f"Fehler beim Scrapen der Quelle: {self.SOURCE}"
            )
            assert html_article
            soup = BeautifulSoup(html_article, "html.parser")
            assert soup
            h1 = soup.find("h1", {"class": "headline-title"})
            assert h1
            title = h1.get_text(strip=True)
            main = soup.find("main")
            figure = soup.find("figure")
            assert figure
            main = figure.find_next_siblings()
            if main:
                ps = []
                for elem in main:
                    p = elem.find("p")
                    if p is not None:
                        ps.append(p)
                content = "\n\n".join([p.text for p in ps])
                date_p = soup.find("p", class_="number")
                assert date_p
                datestring = date_p.get_text(strip=True)
                timestamp = datetime.strptime(datestring, "%d.%m.%Y")
                articles.append(
                    Article(
                        timestamp=timestamp,
                        title=title,
                        medium_organisation=self.SOURCE,
                        content=content,
                        link=link,
                        source=self.SOURCE,
                    )
                )

        return self._filter_dates(articles, parameters)

    _URL_PREFIX: str = "https://www.bmv.de/"
    _URL: str = f"{_URL_PREFIX}DE/Meta/BMV-Aktuell/bmv-aktuell.html"

    _GERMAN_MONTHS: List[str] = [
        "",
        "Januar",
        "Februar",
        "März",
        "April",
        "Mai",
        "Juni",
        "Juli",
        "August",
        "September",
        "Oktober",
        "November",
        "Dezember",
    ]
