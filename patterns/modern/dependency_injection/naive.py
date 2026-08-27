"""Hard-wired dependencies: the class news up its own collaborators.

The cost is invisible until you try to test it -- there is no seam to
substitute the clock or the store.
"""

from __future__ import annotations

from datetime import datetime


class GreetingService:
    def __init__(self) -> None:
        self.sent: list[str] = []  # the "store", welded in

    def greet(self, name: str) -> str:
        hour = datetime.now().hour  # the clock, welded in
        prefix = "good morning" if hour < 12 else "good day"
        message = f"{prefix}, {name}"
        self.sent.append(message)
        return message


def main() -> None:
    service = GreetingService()
    print(service.greet("ada"))
    print(f"stored: {service.sent}")


if __name__ == "__main__":
    main()
