from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timedelta
import requests
from article import Article
from typing import Dict, List
from progress import Progress
from zoneinfo import ZoneInfo


class Scraper(ABC):

    SOURCE: str

    @dataclass
    class Parameters(ABC):
        start_date: datetime
        end_date: datetime

    def __init__subclass__(cls, **_) -> None:  # type: ignore
        super().__init_subclass__()
        parameters_class = getattr(cls, "Parameters", None)
        assert isinstance(parameters_class, type)
        assert issubclass(parameters_class, Scraper.Parameters)

    def _get(
        self,
        url: str,
        progress: Progress,
        error_message: str,
        parameters: Dict[str, str] | None = None,
    ) -> str | None:
        try:
            response = requests.get(url, params=parameters)
            response.raise_for_status()
            html = response.text
        except Exception:
            progress.add_error_message(error_message)
            return None
        return html

    def _filter_dates(
        self, articles: List[Article], parameters: Scraper.Parameters
    ) -> List[Article]:
        def make_aware(dt, tz):
            if dt.tzinfo is None:
                return dt.replace(tzinfo=tz)
            return dt.astimezone(tz)

        berlin_tz = ZoneInfo("Europe/Berlin")

        start = make_aware(parameters.start_date, berlin_tz)
        end = make_aware(parameters.end_date, berlin_tz)
        return [
            a
            for a in articles
            if start <= make_aware(a.timestamp, berlin_tz) < end + timedelta(days=1)
        ]

    def _content_to_markdown(self, content) -> str:
        text_parts = []

        for child in content.children:
            if child.name == "a":
                label = child.get_text(strip=True)
                href = child.get("href", "")
                text_parts.append(f"[{label}]({href})")

            elif child.name in ("p", "div", "strong", "span", "abbr"):
                text_parts.append(self._content_to_markdown(child).strip() + "\n")

            elif child.name is None:  # NavigableString
                text_parts.append(child)

            else:
                # recursively process any other tag (e.g., <i>)
                text_parts.append(self._content_to_markdown(child))

        return "".join(text_parts)

    @abstractmethod
    def scrape(
        self, parameters: Scraper.Parameters, progress: Progress
    ) -> List[Article]:
        raise NotImplementedError("@abstractmethod")
