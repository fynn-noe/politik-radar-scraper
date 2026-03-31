from typing import List
from article import Article
from scrapers.scraper import Scraper
from dataclasses import dataclass
from datetime import datetime
from bs4 import BeautifulSoup 
from bs4.element import Tag
from progress import Progress


class BmvScraper(Scraper):

    SOURCE: str = "BMV"

    @dataclass
    class Parameters(Scraper.Parameters):
        pass

    def scrape(self, parameters: Scraper.Parameters, progress: Progress) -> List[Article]:
        html_text = self._get(self._URL, progress, f"Fehler beim Scrapen der Quelle: {self.SOURCE}")
        if html_text is None:
            return []

        soup = BeautifulSoup(html_text, "html.parser")

        urls = soup.find_all("a",{"class":"card-link"})
        articles = []
        for url in progress.start_iteration(urls, len(urls), "Scraping bmv articles..."):
            link = f"{self._URL_PREFIX}{url.get("href")}"
            html_article = self._get(link, progress, f"Fehler beim Scrapen der Quelle: {self.SOURCE}")
            soup = BeautifulSoup(html_article,"html.parser")
            title = soup.find("h1",{"class":"headline-title"}).get_text(strip=True)
            main = soup.find("main")
    
            if main:
                ps = main.find_all("p")
                content = "\n\n".join([p.text for p in ps])
                datestring = soup.find("p",{"class":"number"}).get_text(strip=True)
                timestamp = datetime.strptime(datestring,"%d.%m.%Y")
                articles.append(Article(
                    timestamp=timestamp,
                    title=title,
                    medium_organisation=self.SOURCE,
                    content=content,
                    link=link, 
                    source=self.SOURCE
                ))

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
        "Dezember"
    ]
