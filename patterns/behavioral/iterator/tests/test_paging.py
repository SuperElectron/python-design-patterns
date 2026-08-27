"""Behavioral tests for the Iterator pattern's library code."""

from __future__ import annotations

import itertools

from patterns.behavioral.iterator.pattern import iterate_pages


class TestIteratePages:
    def test_yields_all_items_across_pages(self) -> None:
        pages = [[1, 2], [3, 4], [5]]
        fetched: list[int] = []

        def fetch(n: int) -> list[int]:
            fetched.append(n)
            return pages[n] if n < len(pages) else []

        assert list(iterate_pages(fetch)) == [1, 2, 3, 4, 5]
        assert fetched == [0, 1, 2, 3]  # one probe past the end, no more

    def test_is_lazy_until_iterated(self) -> None:
        fetched: list[int] = []

        def fetch(n: int) -> list[int]:
            fetched.append(n)
            return [n] if n < 5 else []

        iterator = iterate_pages(fetch)
        assert fetched == []  # creating the iterator fetched nothing
        next(iterator)
        assert fetched == [0]

    def test_partial_consumption_fetches_only_needed_pages(self) -> None:
        fetched: list[int] = []

        def fetch(n: int) -> list[int]:
            fetched.append(n)
            return list(range(n * 3, n * 3 + 3)) if n < 10 else []

        first_four = list(itertools.islice(iterate_pages(fetch), 4))
        assert first_four == [0, 1, 2, 3]
        assert fetched == [0, 1]  # 10 pages exist; 2 were touched

    def test_empty_source_yields_nothing(self) -> None:
        assert list(iterate_pages(lambda n: [])) == []
