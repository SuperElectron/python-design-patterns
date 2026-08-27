"""``queue.Queue``: the mediator between threads.

Producer and consumer never reference each other; the queue owns all the
coordination (ordering, blocking, thread safety).
"""

from __future__ import annotations

import queue
import threading


def pipeline(items: list[str]) -> list[str]:
    """Producer and consumer meet only at the queue."""
    channel: queue.Queue[str | None] = queue.Queue()
    results: list[str] = []

    def producer() -> None:
        for item in items:
            channel.put(item)
        channel.put(None)  # sentinel: end of stream

    def consumer() -> None:
        while (item := channel.get()) is not None:
            results.append(item.upper())

    threads = [threading.Thread(target=producer), threading.Thread(target=consumer)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return results


def main() -> None:
    print(pipeline(["a", "b", "c"]))


if __name__ == "__main__":
    main()
