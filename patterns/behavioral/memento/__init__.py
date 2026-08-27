"""Memento — public API.

>>> from patterns.behavioral.memento import History
"""

from patterns.behavioral.memento.pattern import History, NoSnapshotError

__all__ = ["History", "NoSnapshotError"]
