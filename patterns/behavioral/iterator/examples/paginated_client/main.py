"""Demo: consume a few articles; observe how few pages were fetched."""

from __future__ import annotations

import itertools

from patterns.behavioral.iterator.examples.paginated_client.backend import FakeBackend
from patterns.behavioral.iterator.examples.paginated_client.client import ArticleClient


def main() -> None:
    backend = FakeBackend([f"article-{n:02d}" for n in range(30)], page_size=5)
    client = ArticleClient(backend)

    first_seven = list(itertools.islice(client.articles(), 7))
    print(f"read {len(first_seven)} articles: {first_seven[0]} .. {first_seven[-1]}")
    print(f"pages fetched: {backend.fetch_log}  (30 articles = 6 pages exist)")

    total = sum(1 for _ in client.articles())
    print(f"full scan: {total} articles, pages fetched now: {backend.fetch_log}")


if __name__ == "__main__":
    main()
