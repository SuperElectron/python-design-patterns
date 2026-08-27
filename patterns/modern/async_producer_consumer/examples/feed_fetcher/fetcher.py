"""The pipeline: N workers pull feeds through a bounded queue.

A fake network stands in for HTTP so the demo and tests run offline and
deterministically; swap ``fetch_entries`` for a real client and nothing
else changes.
"""

from __future__ import annotations

import asyncio
from collections.abc import Iterable

from patterns.modern.async_producer_consumer.examples.feed_fetcher.models import (
    Feed,
    FetchOutcome,
)
from patterns.modern.async_producer_consumer.pattern import Shutdown, WorkerPool


async def fetch_entries(feed: Feed) -> int:
    """Pretend to fetch and parse one feed; raise on a bad host."""
    await asyncio.sleep(0)  # stand-in for real async I/O
    if "unreachable" in feed.url:
        raise ConnectionError(f"cannot reach {feed.url}")
    return len(feed.name)  # deterministic stand-in for "entries parsed"


async def fetch_all(
    feeds: Iterable[Feed],
    *,
    workers: int = 3,
    maxsize: int = 2,
    shutdown: Shutdown = Shutdown.JOIN_AND_CANCEL,
) -> list[FetchOutcome]:
    """Fetch every feed; failures become recorded outcomes, not crashes."""

    async def capture(feed: Feed) -> FetchOutcome:
        try:
            return FetchOutcome(feed, entries=await fetch_entries(feed))
        except ConnectionError as exc:
            return FetchOutcome(feed, error=str(exc))

    pool: WorkerPool[Feed, FetchOutcome] = WorkerPool(
        capture, workers=workers, maxsize=maxsize, shutdown=shutdown
    )
    return await pool.run(feeds)


def summarize(outcomes: Iterable[FetchOutcome]) -> str:
    """One line a human can read at the end of a run."""
    outcomes = list(outcomes)
    fetched = sum(o.entries for o in outcomes if o.ok)
    failed = [o.feed.name for o in outcomes if not o.ok]
    line = f"{fetched} entries from {sum(o.ok for o in outcomes)} feeds"
    if failed:
        line += f"; failed: {', '.join(sorted(failed))}"
    return line
