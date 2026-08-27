"""Commands as callables.

For plain deferral, ``functools.partial`` packages the call and its
arguments. For undo, a command is a (do, undo) pair -- here a small frozen
dataclass of two callables, still no interface or hierarchy.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from functools import partial


def run_queue(queue: list[Callable[[], None]]) -> None:
    """The execute-only invoker: call everything, in order."""
    for command in queue:
        command()


@dataclass(frozen=True)
class Undoable:
    """A reversible command: two callables, no ceremony."""

    do: Callable[[], None]
    undo: Callable[[], None]


@dataclass
class Editor:
    text: str = ""
    _history: list[Undoable] = field(default_factory=list)

    def append(self, chunk: str) -> None:
        command = Undoable(
            do=partial(self._append, chunk),
            undo=partial(self._chop, len(chunk)),
        )
        command.do()
        self._history.append(command)

    def undo(self) -> None:
        if self._history:
            self._history.pop().undo()

    def _append(self, chunk: str) -> None:
        self.text += chunk

    def _chop(self, n: int) -> None:
        self.text = self.text[:-n]


def main() -> None:
    log: list[str] = []
    queue: list[Callable[[], None]] = [partial(log.append, "a"), partial(log.append, "b")]
    run_queue(queue)
    print(f"queued callables ran: {log}")

    editor = Editor()
    editor.append("hello")
    editor.append(" world")
    editor.undo()
    print(f"after undo: {editor.text!r}")


if __name__ == "__main__":
    main()
