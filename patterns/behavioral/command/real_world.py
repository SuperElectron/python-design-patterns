"""Callbacks in the stdlib are the Command pattern.

``sched.scheduler`` queues (time, priority, action, arguments) records --
commands with metadata -- and its run loop is the invoker.
"""

from __future__ import annotations

import sched


class FakeClock:
    """A clock the scheduler advances by 'sleeping' -- tests run instantly."""

    def __init__(self) -> None:
        self.now = 0.0

    def time(self) -> float:
        return self.now

    def sleep(self, duration: float) -> None:
        self.now += duration


def run_scheduled(chunks: list[str]) -> list[str]:
    """Queue one append-command per chunk; the scheduler invokes them in order."""
    log: list[str] = []
    clock = FakeClock()
    scheduler = sched.scheduler(timefunc=clock.time, delayfunc=clock.sleep)
    for delay, chunk in enumerate(chunks):
        scheduler.enter(float(delay), 1, log.append, argument=(chunk,))
    scheduler.run()
    return log


def main() -> None:
    print(run_scheduled(["first", "second", "third"]))


if __name__ == "__main__":
    main()
