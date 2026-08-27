"""Domain types for the feed-client mini-project."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Article:
    """One entry in a news feed."""

    title: str
    body: str
