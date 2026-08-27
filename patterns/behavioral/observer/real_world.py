"""``Future.add_done_callback``: the stdlib observer.

Any callable can subscribe to a future's completion; late subscribers to an
already-resolved future fire immediately.
"""

from __future__ import annotations

from concurrent.futures import Future


def observe_completion() -> list[str]:
    events: list[str] = []
    future: Future[int] = Future()
    future.add_done_callback(lambda f: events.append(f"log: {f.result()}"))
    future.add_done_callback(lambda f: events.append(f"metrics: {f.result()}"))
    future.set_result(42)
    return events


def late_subscription_fires_immediately() -> bool:
    future: Future[str] = Future()
    future.set_result("done")
    fired: list[str] = []
    future.add_done_callback(lambda f: fired.append(f.result()))
    return fired == ["done"]


def main() -> None:
    print(observe_completion())
    print(f"late subscriber still notified: {late_subscription_fires_immediately()}")


if __name__ == "__main__":
    main()
