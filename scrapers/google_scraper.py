from typing import List
from article import Article
from scrapers.scraper import Scraper
from dataclasses import dataclass
from datetime import datetime
from bs4 import BeautifulSoup 
from bs4.element import Tag
from progress import Progress
from scrapers.scrape_rss import scrape_rss
import feedparser

class GoogleScraper(Scraper):

    SOURCE: str = "Google News"

    @dataclass
    class Parameters(Scraper.Parameters):
        pass

    def scrape(self, parameters: Scraper.Parameters, progress: Progress) -> List[Article]:
        datestring = "%a, %d %b %Y %H:%M:%S %Z"
        articles = scrape_rss(self._URL,self.SOURCE,datestring,progress)

        return self._filter_dates(articles, parameters)


    _URL_PREFIX: str = "https://news.google.com/"
    _URL: str = f"{_URL_PREFIX}rss?hl=de&gl=DE&ceid=DE:de"
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
