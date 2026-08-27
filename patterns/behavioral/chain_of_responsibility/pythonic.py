"""The chain as a list of callables and one loop.

Each handler returns an answer or None; the first answer wins, and the
unhandled case is explicit at the end of the loop.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence

Handler = Callable[[int], str | None]


def helpdesk(severity: int) -> str | None:
    return "helpdesk resolves it" if severity <= 1 else None


def engineer(severity: int) -> str | None:
    return "engineer resolves it" if severity <= 3 else None


def management(severity: int) -> str | None:
    return "management escalation" if severity <= 5 else None


CHAIN: list[Handler] = [helpdesk, engineer, management]


def handle(severity: int, chain: Sequence[Handler] | None = None) -> str:
    for handler in chain if chain is not None else CHAIN:
        answer = handler(severity)
        if answer is not None:
            return answer
    return "unhandled"  # falling off the end is a decision, made visible


def main() -> None:
    for severity in (1, 3, 5, 9):
        print(f"severity {severity}: {handle(severity)}")


if __name__ == "__main__":
    main()
