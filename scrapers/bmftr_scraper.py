from typing import List
from article import Article
from scrapers.scraper import Scraper
from dataclasses import dataclass
from datetime import datetime
from bs4 import BeautifulSoup
from progress import Progress
import json


class BmftrScraper(Scraper):

    SOURCE: str = "BMFTR"

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

        urls = soup.find_all(
            "a", {"class": "c-teaser-search-result__link-main is-internal-link"}
        )
        articles = []
        for url in progress.start_iteration(
            urls, len(urls), "Scraping bmftr articles..."
        ):
            link = url.get("href")
            html_article = self._get(
                link, progress, f"Fehler beim Scrapen der Quelle: {self.SOURCE}"
            )
            assert html_article
            soup = BeautifulSoup(html_article, "html.parser")
            title_h1 = soup.find("h1", class_="l-intro__headline")
            assert title_h1
            title = title_h1.get_text(strip=True)
            main = soup.find("div", class_="l-article__content s-article-content")

            if main:
                ps = main.find_all("p")
                content = "\n\n".join([p.text for p in ps])
                script = soup.find("script", type_="application/ld+json")
                assert script
                assert script.string
                data = json.loads(script.string)
                timestamp = datetime.fromisoformat(data.get("datePublished")).replace(
                    tzinfo=None
                )
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

    _URL_PREFIX: str = "https://www.bmftr.bund.de/"
    _URL: str = (
        f"{_URL_PREFIX}SiteGlobals/Forms/Suche/Expertensuche/Expertensuche_Formular.html?format_str=pressrelease"
    )

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
