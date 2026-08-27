"""Demo: a batch of feeds through the pool, under both shutdown disciplines."""

from __future__ import annotations

import asyncio

from patterns.modern.async_producer_consumer.examples.feed_fetcher.fetcher import (
    fetch_all,
    summarize,
)
from patterns.modern.async_producer_consumer.examples.feed_fetcher.models import Feed
from patterns.modern.async_producer_consumer.pattern import Shutdown


def main() -> None:
    feeds = [
        Feed("python-insider", "https://feeds.example/python-insider"),
        Feed("lwn", "https://feeds.example/lwn"),
        Feed("hn", "https://feeds.example/hn"),
        Feed("dead-blog", "https://unreachable.example/rss"),
        Feed("release-notes", "https://feeds.example/releases"),
    ]
    for shutdown in Shutdown:
        outcomes = asyncio.run(fetch_all(feeds, shutdown=shutdown))
        print(f"{shutdown.value}: {summarize(outcomes)}")


if __name__ == "__main__":
    main()
