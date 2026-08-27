"""The Gang of Four chain: successor pointers through handler objects."""

from __future__ import annotations

from abc import ABC, abstractmethod


class Handler(ABC):
    def __init__(self, successor: Handler | None = None) -> None:
        self.successor = successor

    def handle(self, severity: int) -> str:
        answer = self._attempt(severity)
        if answer is not None:
            return answer
        if self.successor is None:
            return "unhandled"
        return self.successor.handle(severity)

    @abstractmethod
    def _attempt(self, severity: int) -> str | None: ...


class Helpdesk(Handler):
    def _attempt(self, severity: int) -> str | None:
        return "helpdesk resolves it" if severity <= 1 else None


class Engineer(Handler):
    def _attempt(self, severity: int) -> str | None:
        return "engineer resolves it" if severity <= 3 else None


class Management(Handler):
    def _attempt(self, severity: int) -> str | None:
        return "management escalation" if severity <= 5 else None


def build_chain() -> Handler:
    return Helpdesk(Engineer(Management()))


def main() -> None:
    chain = build_chain()
    for severity in (1, 3, 5, 9):
        print(f"severity {severity}: {chain.handle(severity)}")


if __name__ == "__main__":
    main()
