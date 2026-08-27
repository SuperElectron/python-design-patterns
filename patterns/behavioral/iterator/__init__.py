"""Iterator — public API.

>>> from patterns.behavioral.iterator import iterate_pages
"""

from patterns.behavioral.iterator.pattern import PageFetcher, iterate_pages

__all__ = ["PageFetcher", "iterate_pages"]
