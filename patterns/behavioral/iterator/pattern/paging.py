"""Iterator as an importable building block: traversal behind one generator.

Python absorbed this pattern into the language — ``for``, comprehensions,
and generators all speak the protocol. What remains worth packaging is the
*shape*: hide a chunked or remote traversal behind a single generator so
callers iterate items and never see pages, cursors, or fetch calls.
"""

from __future__ import annotations

import itertools
from collections.abc import Callable, Iterator, Sequence
from typing import TypeVar

T = TypeVar("T")

#: Fetches one zero-indexed page; an empty page means the sequence is over.
PageFetcher = Callable[[int], Sequence[T]]


def iterate_pages(fetch_page: PageFetcher[T]) -> Iterator[T]:
    """Yield items lazily, page by page, stopping at the first empty page.

    Nothing is fetched until iteration demands it, and only the pages
    actually consumed are ever requested — the laziness is the contract.
    """
    for page_number in itertools.count():
        page = fetch_page(page_number)
        if not page:
            return
        yield from page
