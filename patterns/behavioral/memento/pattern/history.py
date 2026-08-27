"""Memento as an importable, typed building block.

The originator's state is any value — ideally immutable, so a snapshot *is*
the old state object. ``History`` is the caretaker: it stores snapshots and
hands them back, but never looks inside. Undo is LIFO; named checkpoints
("before-upgrade") are random-access.
"""

from __future__ import annotations

from typing import Generic, TypeVar

Snapshot = TypeVar("Snapshot")


class NoSnapshotError(LookupError):
    """The history has nothing to restore."""


class History(Generic[Snapshot]):
    """A caretaker for opaque snapshots: an undo stack plus named checkpoints."""

    def __init__(self) -> None:
        self._stack: list[Snapshot] = []
        self._checkpoints: dict[str, Snapshot] = {}

    def save(self, snapshot: Snapshot) -> Snapshot:
        """Push a snapshot onto the undo stack and return it unchanged."""
        self._stack.append(snapshot)
        return snapshot

    def undo(self) -> Snapshot:
        """Pop and return the most recent snapshot; raise if there is none."""
        if not self._stack:
            raise NoSnapshotError("history is empty")
        return self._stack.pop()

    def checkpoint(self, name: str, snapshot: Snapshot, *, replace: bool = False) -> Snapshot:
        """Store a snapshot under a name; the name must be free.

        A duplicate name is an error unless ``replace=True`` — a rollback API
        that silently swaps what "before-migration" points at is untrustworthy
        exactly where it must not be.
        """
        if name in self._checkpoints and not replace:
            raise ValueError(f"checkpoint {name!r} already exists (pass replace=True)")
        self._checkpoints[name] = snapshot
        return snapshot

    def rollback_to(self, name: str) -> Snapshot:
        """Return the named checkpoint; raise if the name is unknown."""
        try:
            return self._checkpoints[name]
        except KeyError:
            known = sorted(self._checkpoints) or "none"
            raise NoSnapshotError(f"no checkpoint {name!r} (known: {known})") from None

    def __len__(self) -> int:
        return len(self._stack)

    def __bool__(self) -> bool:
        return bool(self._stack) or bool(self._checkpoints)
