"""Constructor injection with Protocol seams and production defaults.

The test hands in a frozen clock and a fake store; production changes
nothing and passes nothing.
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import datetime
from typing import Protocol


class Store(Protocol):
    def append(self, message: str) -> None: ...


def wall_clock_hour() -> int:
    return datetime.now().hour


class GreetingService:
    def __init__(
        self,
        store: Store | None = None,
        hour_now: Callable[[], int] = wall_clock_hour,
    ) -> None:
        self.store: Store = store if store is not None else []
        self.hour_now = hour_now

    def greet(self, name: str) -> str:
        prefix = "good morning" if self.hour_now() < 12 else "good day"
        message = f"{prefix}, {name}"
        self.store.append(message)
        return message


def main() -> None:
    print(GreetingService().greet("ada"))  # production wiring: defaults
    frozen = GreetingService(hour_now=lambda: 9)  # test wiring: injected
    print(frozen.greet("grace"))


if __name__ == "__main__":
    main()
