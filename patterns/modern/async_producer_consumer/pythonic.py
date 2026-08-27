"""asyncio.Queue + TaskGroup workers.

maxsize bounds memory (backpressure), join() waits for all items to be
processed, cancellation ends the idle workers.
"""

from __future__ import annotations

import asyncio


async def process_all(items: list[str], worker_count: int = 3) -> list[str]:
    channel: asyncio.Queue[str] = asyncio.Queue(maxsize=2)  # backpressure
    results: list[str] = []

    async def worker() -> None:
        while True:
            item = await channel.get()
            try:
                await asyncio.sleep(0)  # stand-in for real async I/O
                results.append(item.upper())
            finally:
                channel.task_done()

    async with asyncio.TaskGroup() as group:
        workers = [group.create_task(worker()) for _ in range(worker_count)]
        for item in items:
            await channel.put(item)  # blocks when the queue is full
        await channel.join()  # all items fetched AND task_done()
        for w in workers:
            w.cancel()  # idle workers end; TaskGroup absorbs the cancellation

    return sorted(results)


def main() -> None:
    print(asyncio.run(process_all(["a", "b", "c", "d", "e"])))


if __name__ == "__main__":
    main()
