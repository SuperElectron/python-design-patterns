"""A paginated API client built on the Iterator pattern.

Run it: ``uv run python -m patterns.behavioral.iterator.examples.paginated_client``
"""

from patterns.behavioral.iterator.examples.paginated_client.backend import FakeBackend
from patterns.behavioral.iterator.examples.paginated_client.client import ArticleClient

__all__ = ["ArticleClient", "FakeBackend"]
