"""Domain objects for the feed-fetching pipeline."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Feed:
    """A feed to fetch: a name and its URL."""

    name: str
    url: str


@dataclass(frozen=True)
class FetchOutcome:
    """What happened to one feed — success with entries, or a recorded error.

    The pool itself is fail-fast; capturing per-feed failures is this
    project's policy, applied inside its processor.
    """

    feed: Feed
    entries: int = 0
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.error is None
