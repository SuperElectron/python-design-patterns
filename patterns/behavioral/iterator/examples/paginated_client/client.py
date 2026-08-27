"""The client: one generator hides pages, cursors, and fetch calls."""

from __future__ import annotations

from collections.abc import Iterator

from patterns.behavioral.iterator.examples.paginated_client.backend import FakeBackend
from patterns.behavioral.iterator.pattern import iterate_pages


class ArticleClient:
    """Callers iterate articles; pagination never leaks into their code."""

    def __init__(self, backend: FakeBackend) -> None:
        self._backend = backend

    def articles(self) -> Iterator[str]:
        """All articles, fetched lazily page by page as iteration demands."""
        return iterate_pages(self._backend.fetch)
