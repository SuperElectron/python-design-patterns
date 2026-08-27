"""Behavioral tests for the paginated-client mini-project."""

from __future__ import annotations

import itertools

from patterns.behavioral.iterator.examples.paginated_client.backend import FakeBackend
from patterns.behavioral.iterator.examples.paginated_client.client import ArticleClient


def _backend(count: int = 30, page_size: int = 5) -> FakeBackend:
    return FakeBackend([f"article-{n:02d}" for n in range(count)], page_size)


class TestArticleClient:
    def test_full_iteration_sees_every_article_in_order(self) -> None:
        backend = _backend(12, page_size=5)
        client = ArticleClient(backend)
        articles = list(client.articles())
        assert len(articles) == 12
        assert articles[0] == "article-00"
        assert articles[-1] == "article-11"

    def test_consuming_seven_articles_fetches_two_pages(self) -> None:
        backend = _backend(30, page_size=5)
        client = ArticleClient(backend)
        list(itertools.islice(client.articles(), 7))
        assert backend.fetch_log == [0, 1]  # pages 2..5 were never requested

    def test_each_call_returns_a_fresh_iterator(self) -> None:
        backend = _backend(4, page_size=2)
        client = ArticleClient(backend)
        assert list(client.articles()) == list(client.articles())

    def test_empty_backend(self) -> None:
        backend = _backend(0)
        client = ArticleClient(backend)
        assert list(client.articles()) == []
        assert backend.fetch_log == [0]
