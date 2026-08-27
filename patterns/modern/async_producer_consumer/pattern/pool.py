"""Async producer/consumer as an importable, typed building block.

``WorkerPool`` fans items out to N workers over a bounded ``asyncio.Queue``:
``maxsize`` gives backpressure, and the shutdown discipline — the part the
classic pattern leaves implicit — is an explicit, tested choice
(:class:`Shutdown`). Results are collected in completion order.
"""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable, Iterable
from enum import Enum
from typing import Any, Generic, TypeVar

Item = TypeVar("Item")
Result = TypeVar("Result")

Processor = Callable[[Item], Awaitable[Result]]


class Shutdown(Enum):
    """How the pool tells its workers the work is over.

    ``SENTINEL``: one end-marker per worker is enqueued after the items;
    each worker exits when it dequeues one. ``JOIN_AND_CANCEL``: workers
    loop forever; the pool awaits ``queue.join()`` then cancels them.
    Pick one and test it — mixing disciplines is where shutdown bugs live.
    """

    SENTINEL = "sentinel"
    JOIN_AND_CANCEL = "join-and-cancel"


class _End:
    """Private end-of-work marker for the sentinel discipline."""


_END = _End()


class WorkerPool(Generic[Item, Result]):
    """N workers processing items from a bounded queue.

    The pool is fail-fast: an exception in ``process`` cancels the run and
    surfaces as an ``ExceptionGroup`` (via ``TaskGroup``). Callers who want
    per-item failure capture wrap it in their processor.
    """

    def __init__(
        self,
        process: Processor[Item, Result],
        *,
        workers: int = 4,
        maxsize: int = 8,
        shutdown: Shutdown = Shutdown.JOIN_AND_CANCEL,
    ) -> None:
        if workers < 1:
            raise ValueError("a pool needs at least one worker")
        self._process = process
        self._workers = workers
        self._maxsize = maxsize
        self._shutdown = shutdown

    async def run(self, items: Iterable[Item]) -> list[Result]:
        """Process every item; return results in completion order."""
        if self._shutdown is Shutdown.SENTINEL:
            return await self._run_sentinel(items)
        return await self._run_join_and_cancel(items)

    def _make_channel(self, maxsize: int) -> asyncio.Queue[Any]:
        """Observability seam: tests substitute a recording queue here to
        assert the shutdown *mechanism* (sentinel count, task_done
        bookkeeping, backpressure bound), not just the results."""
        return asyncio.Queue(maxsize=maxsize)

    async def _run_join_and_cancel(self, items: Iterable[Item]) -> list[Result]:
        channel: asyncio.Queue[Item] = self._make_channel(self._maxsize)
        results: list[Result] = []

        async def worker() -> None:
            while True:
                item = await channel.get()
                try:
                    results.append(await self._process(item))
                finally:
                    channel.task_done()

        async with asyncio.TaskGroup() as group:
            workers = [group.create_task(worker()) for _ in range(self._workers)]
            for item in items:
                await channel.put(item)  # blocks when full: backpressure
            await channel.join()  # every item fetched AND task_done()
            for w in workers:
                w.cancel()  # idle workers end; TaskGroup absorbs this
        return results

    async def _run_sentinel(self, items: Iterable[Item]) -> list[Result]:
        channel: asyncio.Queue[Item | _End] = self._make_channel(self._maxsize)
        results: list[Result] = []

        async def worker() -> None:
            while True:
                got = await channel.get()
                if isinstance(got, _End):
                    return  # a worker consumes exactly one sentinel
                results.append(await self._process(got))

        async with asyncio.TaskGroup() as group:
            for _ in range(self._workers):
                group.create_task(worker())
            for item in items:
                await channel.put(item)
            for _ in range(self._workers):
                await channel.put(_END)  # one per worker, after the items
        return results


async def process_all(
    items: Iterable[Item],
    process: Processor[Item, Result],
    *,
    workers: int = 4,
    maxsize: int = 8,
    shutdown: Shutdown = Shutdown.JOIN_AND_CANCEL,
) -> list[Result]:
    """One-shot convenience over :class:`WorkerPool`."""
    pool: WorkerPool[Item, Result] = WorkerPool(
        process, workers=workers, maxsize=maxsize, shutdown=shutdown
    )
    return await pool.run(items)
