from typing import List
from article import Article
from scrapers.scraper import Scraper
from dataclasses import dataclass
from progress import Progress
from scrapers.scrape_rss import scrape_rss


class BsiRssScraper(Scraper):

    SOURCE: str = "BSI"

    @dataclass
    class Parameters(Scraper.Parameters):
        pass

    def scrape(
        self, parameters: Scraper.Parameters, progress: Progress
    ) -> List[Article]:
        datestring = "%a, %d %b %Y %H:%M:%S %z"
        articles = scrape_rss(self._URL, self.SOURCE, datestring, progress)

        return self._filter_dates(articles, parameters)

    _URL_PREFIX: str = "https://www.bsi.bund.de/"
    _URL: str = (
        f"{_URL_PREFIX}SiteGlobals/Functions/RSSFeed/RSSNewsfeed/RSSNewsfeed_Presse_Veranstaltungen.xml"
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
