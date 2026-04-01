from typing import List
from article import Article
from scrapers.scraper import Scraper
from dataclasses import dataclass
from datetime import datetime
from progress import Progress
from bs4 import BeautifulSoup 

class BmuknScraper(Scraper):

    SOURCE: str = "BMUKN"

    @dataclass
    class Parameters(Scraper.Parameters):
        pass

    def scrape(self, parameters: Scraper.Parameters, progress: Progress) -> List[Article]:
        html_text = self._get(self._URL, progress, f"Fehler beim Scrapen der Quelle: {self.SOURCE}")
        if html_text is None:
            return []
        soup = BeautifulSoup(html_text,"html.parser")
        rows = soup.find_all("div",{"class":"c-articles-list__item"})
        entries = []
        for row in rows:
            if row:
                timestamp = datetime.fromisoformat(row.find("time").get("datetime"))
                title = row.find("span",{"itemprop":"name"}).get_text(strip=True)
                link = f"{self._URL_PREFIX}{row.find("a").get("href")}"
                entries.append((timestamp,title,link))
        articles = []
        for timestamp, title, link in progress.start_iteration(entries, total=len(entries), desc="Scraping BMUKN articles"):
            html_article = self._get(link, progress, f"Fehler beim Scrapen der Quelle: {self.SOURCE} bei Artikel: {title}")
            if html_article is None:
                continue
        
            soup_article = BeautifulSoup(html_article,"html.parser")

            main = soup_article.find("div",{"class":"c-ce-formated"})
            if main:
                ps = main.find_all("p")
                content = "\n\n".join([p.text for p in ps])
                articles.append(Article(
                    timestamp=timestamp,
                    title=title,
                    medium_organisation=self.SOURCE,
                    content=content,
                    link=link,
                    source=self.SOURCE
            ))
                
        assert articles

        return self._filter_dates(articles, parameters)


    _URL_PREFIX: str = "https://www.bundesumweltministerium.de/"
    _URL: str = f"{_URL_PREFIX}presse/pressemitteilungen"
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

