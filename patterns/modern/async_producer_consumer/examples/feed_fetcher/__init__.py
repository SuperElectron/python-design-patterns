"""Feed-fetching pipeline built on the async producer/consumer pool.

Run it: ``uv run python -m patterns.modern.async_producer_consumer.examples.feed_fetcher``
"""

from patterns.modern.async_producer_consumer.examples.feed_fetcher.fetcher import (
    fetch_all,
    fetch_entries,
    summarize,
)
from patterns.modern.async_producer_consumer.examples.feed_fetcher.models import (
    Feed,
    FetchOutcome,
)

__all__ = ["Feed", "FetchOutcome", "fetch_all", "fetch_entries", "summarize"]
