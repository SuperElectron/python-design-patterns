"""Command as an importable, typed building block.

For plain deferral, a callable (or ``functools.partial``) already *is* the
packaged request. The class form earns its keep when commands carry undo:
``Undoable`` pairs a do with its inverse, and ``UndoStack`` is the invoker
that remembers history and replays it in either direction.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

Action = Callable[[], None]


@dataclass(frozen=True)
class Undoable:
    """A reversible command: two callables and a label for the log."""

    do: Action
    undo: Action
    label: str = ""


class UndoStack:
    """The invoker: executes commands, remembers them, undoes and redoes.

    Pushing a new command clears the redo history — after diverging, the
    undone future can no longer be replayed (the standard editor contract).
    """

    def __init__(self) -> None:
        self._done: list[Undoable] = []
        self._undone: list[Undoable] = []

    def push(self, command: Undoable) -> None:
        """Execute ``command`` and record it as the newest history entry."""
        command.do()
        self._done.append(command)
        self._undone.clear()

    def undo(self) -> Undoable | None:
        """Reverse the newest command; return it, or ``None`` if no history."""
        if not self._done:
            return None
        command = self._done.pop()
        command.undo()
        self._undone.append(command)
        return command

    def redo(self) -> Undoable | None:
        """Re-execute the most recently undone command, if any."""
        if not self._undone:
            return None
        command = self._undone.pop()
        command.do()
        self._done.append(command)
        return command

    @property
    def can_undo(self) -> bool:
        return bool(self._done)

    @property
    def can_redo(self) -> bool:
        return bool(self._undone)

    def log(self) -> tuple[str, ...]:
        """Labels of every command currently applied, oldest first."""
        return tuple(command.label for command in self._done)
