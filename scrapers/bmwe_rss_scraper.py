from typing import List
from article import Article
from scrapers.scraper import Scraper
from dataclasses import dataclass
from datetime import datetime
from bs4 import BeautifulSoup 
from bs4.element import Tag
from progress import Progress
from scrapers.scrape_rss import scrape_rss


class BmweRssScraper(Scraper):

    SOURCE: str = "BMWE"

    @dataclass
    class Parameters(Scraper.Parameters):
        pass

    def scrape(self, parameters: Scraper.Parameters, progress: Progress) -> List[Article]:
        datestring = "%a, %d %b %Y %H:%M:%S %z"
        articles = scrape_rss(self._URL,self.SOURCE,datestring,progress)

        return self._filter_dates(articles, parameters)


    _URL_PREFIX: str = "https://www.energiewechsel.de/"
    _URL: str = f"{_URL_PREFIX}SiteGlobals/KAENEF/Functions/RSSFeed/DE/RSSFeed-Meldungen.xml"
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
