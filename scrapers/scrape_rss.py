from typing import List
from article import Article
from scrapers.scraper import Scraper
from dataclasses import dataclass
from datetime import datetime
from bs4 import BeautifulSoup 
from bs4.element import Tag
from progress import Progress
from dateutil import parser
import feedparser
def scrape_rss(URL, source, datestring, progress: Progress):
    feed = feedparser.parse(URL)
    articles = []
    #print(feed)
    if feed.status == 200:
        for entry in progress.start_iteration(feed.entries, len(feed.entries), f"Scraping {source}..."):
            soup = BeautifulSoup(entry.description, "html.parser")
            content = soup.get_text()
            try:
                source_res=entry.source["title"]
            except:
                source_res = source
            articles.append(Article(
                # ACHTUNG: NICHT TIMEZONE AWARE (DATUM KÖNNTE NICHT DAS RICHTIGE SEIN)
                timestamp=parser.parse(entry.published, ignoretz=True),
                title=entry.title,
                medium_organisation=source,
                content=content,
                link=entry.link, 
                source=source_res
            )
        )
            
    return articles