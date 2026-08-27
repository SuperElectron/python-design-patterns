"""Two pythonic state machines.

1. Enum + transition table: the machine is data, visible in one dict.
2. A generator: the suspension point is the state; send() drives it.
"""

from __future__ import annotations

from collections.abc import Generator
from enum import Enum, auto


class State(Enum):
    LOCKED = auto()
    UNLOCKED = auto()


#: (state, event) -> (next_state, output)
TRANSITIONS: dict[tuple[State, str], tuple[State, str]] = {
    (State.LOCKED, "coin"): (State.UNLOCKED, "unlocked"),
    (State.LOCKED, "push"): (State.LOCKED, "locked: push refused"),
    (State.UNLOCKED, "coin"): (State.UNLOCKED, "already unlocked: coin returned"),
    (State.UNLOCKED, "push"): (State.LOCKED, "pushed through, locking"),
}


class Turnstile:
    def __init__(self) -> None:
        self.state = State.LOCKED

    def handle(self, event: str) -> str:
        self.state, output = TRANSITIONS[(self.state, event)]
        return output


def turnstile_machine() -> Generator[str, str, None]:
    """The generator form: 'where the code is paused' is the state."""
    output = "ready"
    while True:
        event = yield output
        if event == "coin":
            output = "unlocked"
            event = yield output  # ---- the UNLOCKED state lives here ----
            while event == "coin":
                event = yield "already unlocked: coin returned"
            output = "pushed through, locking"
        else:
            output = "locked: push refused"


def main() -> None:
    machine = Turnstile()
    print([machine.handle(e) for e in ("push", "coin", "push")])

    gen = turnstile_machine()
    next(gen)
    print([gen.send(e) for e in ("push", "coin", "push")])


if __name__ == "__main__":
    main()
