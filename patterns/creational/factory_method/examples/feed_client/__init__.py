"""A feed-client framework built on the unit's ``pattern`` package.

Run it: ``uv run python -m patterns.creational.factory_method.examples.feed_client``
"""

from patterns.creational.factory_method.examples.feed_client.client import (
    DigestClient,
    DigestResponse,
    FeedClient,
    FeedResponse,
    StrictClient,
    Transport,
    parse_strictly,
)
from patterns.creational.factory_method.examples.feed_client.models import Article

__all__ = [
    "Article",
    "DigestClient",
    "DigestResponse",
    "FeedClient",
    "FeedResponse",
    "StrictClient",
    "Transport",
    "parse_strictly",
]
