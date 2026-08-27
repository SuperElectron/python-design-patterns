"""The Memento pattern, importable as library code."""

from patterns.behavioral.memento.pattern.history import History, NoSnapshotError

__all__ = ["History", "NoSnapshotError"]
