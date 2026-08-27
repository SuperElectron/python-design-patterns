"""The thread version: queue.Queue, sentinel-per-worker shutdown.

Works, but every worker is an OS thread and the coordination is manual.
"""

from __future__ import annotations

import queue
import threading


def process_all(items: list[str], worker_count: int = 2) -> list[str]:
    channel: queue.Queue[str | None] = queue.Queue()
    results: list[str] = []
    lock = threading.Lock()

    def worker() -> None:
        while (item := channel.get()) is not None:
            with lock:
                results.append(item.upper())

    workers = [threading.Thread(target=worker) for _ in range(worker_count)]
    for w in workers:
        w.start()
    for item in items:
        channel.put(item)
    for _ in workers:
        channel.put(None)  # one sentinel per worker
    for w in workers:
        w.join()
    return sorted(results)


def main() -> None:
    print(process_all(["a", "b", "c", "d"]))


if __name__ == "__main__":
    main()
