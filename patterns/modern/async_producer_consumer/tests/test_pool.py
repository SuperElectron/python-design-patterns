"""Behavioral tests for the WorkerPool building block."""

from __future__ import annotations

import asyncio
from typing import Any

import pytest

from patterns.modern.async_producer_consumer.pattern import (
    Shutdown,
    WorkerPool,
    process_all,
)
from patterns.modern.async_producer_consumer.pattern.pool import _End


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


class RecordingQueue(asyncio.Queue[Any]):
    """An asyncio.Queue that logs puts, task_done calls, and peak backlog."""

    def __init__(self, maxsize: int = 0) -> None:
        super().__init__(maxsize)
        self.created_maxsize = maxsize
        self.put_log: list[Any] = []
        self.max_backlog = 0
        self.task_done_calls = 0

    async def put(self, item: Any) -> None:
        await super().put(item)
        self.put_log.append(item)
        self.max_backlog = max(self.max_backlog, self.qsize())

    def task_done(self) -> None:
        self.task_done_calls += 1
        super().task_done()


class ObservablePool(WorkerPool[str, str]):
    """WorkerPool with the channel seam swapped for a RecordingQueue."""

    channel: RecordingQueue

    def _make_channel(self, maxsize: int) -> asyncio.Queue[Any]:
        self.channel = RecordingQueue(maxsize)
        return self.channel


class TestShutdownMechanism:
    """The disciplines must differ observably — not just agree on results.

    Collapsing ``run``'s switch to either branch fails one of these tests,
    so the switch itself is pinned, not merely the outcomes.
    """

    async def test_sentinel_enqueues_one_marker_per_worker_and_drains(self) -> None:
        pool = ObservablePool(upper, workers=3, shutdown=Shutdown.SENTINEL)
        await pool.run(["a", "b", "c", "d", "e"])
        markers = [x for x in pool.channel.put_log if isinstance(x, _End)]
        assert len(markers) == 3  # exactly one per worker, no orphans
        assert pool.channel.qsize() == 0  # every marker consumed: clean drain
        assert pool.channel.task_done_calls == 0  # no join bookkeeping here

    async def test_join_and_cancel_uses_task_done_and_no_sentinels(self) -> None:
        pool = ObservablePool(upper, workers=3, shutdown=Shutdown.JOIN_AND_CANCEL)
        await pool.run(["a", "b", "c", "d", "e"])
        assert pool.channel.task_done_calls == 5  # join() waits on these
        assert not any(isinstance(x, _End) for x in pool.channel.put_log)
        assert pool.channel.qsize() == 0

    async def test_backpressure_bounds_the_queue(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Observes the REAL pool's queue (not the test seam), so making the
        pool construct an unbounded queue fails here."""
        created: list[RecordingQueue] = []

        class TrackingQueue(RecordingQueue):
            def __init__(self, maxsize: int = 0) -> None:
                super().__init__(maxsize)
                created.append(self)

        monkeypatch.setattr(asyncio, "Queue", TrackingQueue)

        async def slow(item: str) -> str:
            await asyncio.sleep(0.001)
            return item.upper()

        await process_all([chr(ord("a") + n) for n in range(10)], slow, workers=2, maxsize=2)
        (channel,) = created
        assert channel.created_maxsize == 2  # the bound is actually passed through
        assert channel.max_backlog <= 2  # and never exceeded during the run
