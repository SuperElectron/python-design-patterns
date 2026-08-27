"""A fake HTTP-ish backend that serves articles in pages and logs each fetch.

The fetch log is the point: tests (and the demo) read it to *prove* the
client fetched only the pages iteration actually consumed.
"""

from __future__ import annotations


class FakeBackend:
    """Serves ``articles`` in pages of ``page_size``; records every request."""

    def __init__(self, articles: list[str], page_size: int = 10) -> None:
        self._articles = list(articles)
        self._page_size = page_size
        self.fetch_log: list[int] = []

    def fetch(self, page_number: int) -> list[str]:
        """One page of articles; empty past the end. Every call is logged."""
        self.fetch_log.append(page_number)
        start = page_number * self._page_size
        return self._articles[start : start + self._page_size]
