"""Behavioral tests for the WorkerPool building block."""

from __future__ import annotations

import asyncio

import pytest

from patterns.modern.async_producer_consumer.pattern import (
    Shutdown,
    WorkerPool,
    process_all,
)


async def upper(item: str) -> str:
    await asyncio.sleep(0)
    return item.upper()


class TestBothDisciplines:
    @pytest.mark.parametrize("shutdown", list(Shutdown))
    async def test_processes_every_item_despite_backpressure(self, shutdown: Shutdown) -> None:
        items = [chr(ord("a") + n) for n in range(10)]  # far more than maxsize
        results = await process_all(items, upper, maxsize=2, shutdown=shutdown)
        assert sorted(results) == [c.upper() for c in items]

    @pytest.mark.parametrize("shutdown", list(Shutdown))
    async def test_zero_items(self, shutdown: Shutdown) -> None:
        assert await process_all([], upper, shutdown=shutdown) == []

    @pytest.mark.parametrize("shutdown", list(Shutdown))
    async def test_more_workers_than_items(self, shutdown: Shutdown) -> None:
        assert await process_all(["x"], upper, workers=5, shutdown=shutdown) == ["X"]

    @pytest.mark.parametrize("shutdown", list(Shutdown))
    async def test_processor_error_fails_fast_as_exception_group(self, shutdown: Shutdown) -> None:
        async def explode(item: str) -> str:
            raise ValueError(f"bad item {item}")

        pool: WorkerPool[str, str] = WorkerPool(explode, shutdown=shutdown)
        with pytest.raises(ExceptionGroup) as excinfo:
            await pool.run(["a"])
        assert excinfo.group_contains(ValueError)


class TestConcurrencyContract:
    async def test_in_flight_work_is_bounded_by_worker_count(self) -> None:
        in_flight = 0
        seen_max = 0

        async def track(item: int) -> int:
            nonlocal in_flight, seen_max
            in_flight += 1
            seen_max = max(seen_max, in_flight)
            await asyncio.sleep(0)  # yield so other workers get a turn
            in_flight -= 1
            return item

        await process_all(range(20), track, workers=3, maxsize=2)
        assert seen_max <= 3

    async def test_results_are_not_sorted_by_the_pool(self) -> None:
        async def slow_first(item: int) -> int:
            await asyncio.sleep(0.02 if item == 0 else 0)
            return item

        results = await process_all([0, 1, 2, 3], slow_first, workers=4)
        assert sorted(results) == [0, 1, 2, 3]
        assert results[-1] == 0  # the slow item finishes last, and stays last

    def test_pool_requires_at_least_one_worker(self) -> None:
        with pytest.raises(ValueError):
            WorkerPool(upper, workers=0)
