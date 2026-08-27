"""The Gang of Four State: a class per state, context delegates."""

from __future__ import annotations

from abc import ABC, abstractmethod


class TurnstileState(ABC):
    @abstractmethod
    def coin(self, turnstile: Turnstile) -> str: ...

    @abstractmethod
    def push(self, turnstile: Turnstile) -> str: ...


class Locked(TurnstileState):
    def coin(self, turnstile: Turnstile) -> str:
        turnstile.state = Unlocked()
        return "unlocked"

    def push(self, turnstile: Turnstile) -> str:
        return "locked: push refused"


class Unlocked(TurnstileState):
    def coin(self, turnstile: Turnstile) -> str:
        return "already unlocked: coin returned"

    def push(self, turnstile: Turnstile) -> str:
        turnstile.state = Locked()
        return "pushed through, locking"


class Turnstile:
    def __init__(self) -> None:
        self.state: TurnstileState = Locked()

    def coin(self) -> str:
        return self.state.coin(self)

    def push(self) -> str:
        return self.state.push(self)


def main() -> None:
    turnstile = Turnstile()
    for event in ("push", "coin", "coin", "push", "push"):
        result = turnstile.coin() if event == "coin" else turnstile.push()
        print(f"{event}: {result}")


if __name__ == "__main__":
    main()
