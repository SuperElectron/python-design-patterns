"""The idiom shaped as a pipeline: N workers, bounded queue, ordered results.

A fake fetcher stands in for HTTP so the demo and tests run offline; swap it
for a real client and nothing else changes.
"""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable

Fetcher = Callable[[str], Awaitable[str]]


async def fake_fetch(url: str) -> str:
    await asyncio.sleep(0)
    return f"body-of-{url}"


async def crawl(urls: list[str], fetch: Fetcher = fake_fetch, workers: int = 4) -> dict[str, str]:
    """Fan URLs out to workers; collect {url: body} whatever the finish order."""
    channel: asyncio.Queue[str] = asyncio.Queue(maxsize=8)
    pages: dict[str, str] = {}

    async def worker() -> None:
        while True:
            url = await channel.get()
            try:
                pages[url] = await fetch(url)
            finally:
                channel.task_done()

    async with asyncio.TaskGroup() as group:
        tasks = [group.create_task(worker()) for _ in range(workers)]
        for url in urls:
            await channel.put(url)
        await channel.join()
        for t in tasks:
            t.cancel()
    return pages


def main() -> None:
    urls = [f"https://example.com/{n}" for n in range(3)]
    print(asyncio.run(crawl(urls)))


if __name__ == "__main__":
    main()
