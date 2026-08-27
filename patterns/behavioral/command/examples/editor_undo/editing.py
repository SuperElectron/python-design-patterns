"""Edit operations as reversible commands.

Each factory captures everything its undo needs *at execution time* —
``delete_span`` must remember the text it removed, which is exactly the
state a bare callback cannot carry and the reason Command earns its keep.
"""

from __future__ import annotations

from patterns.behavioral.command.examples.editor_undo.models import Document
from patterns.behavioral.command.pattern import Undoable


def insert_text(doc: Document, position: int, chunk: str) -> Undoable:
    """Insert ``chunk`` at ``position``; undo removes exactly that span."""

    def undo() -> None:
        doc.delete(position, len(chunk))

    return Undoable(
        do=lambda: doc.insert(position, chunk),
        undo=undo,
        label=f"insert {chunk!r}@{position}",
    )


def delete_span(doc: Document, position: int, length: int) -> Undoable:
    """Delete ``length`` chars at ``position``; undo restores what was removed."""
    removed: list[str] = []  # captured by do, needed by undo

    def do() -> None:
        removed.append(doc.delete(position, length))

    def undo() -> None:
        doc.insert(position, removed.pop())

    return Undoable(do=do, undo=undo, label=f"delete {length}@{position}")


def replace_span(doc: Document, position: int, length: int, chunk: str) -> Undoable:
    """Replace ``length`` chars at ``position`` with ``chunk``, reversibly."""
    removed: list[str] = []

    def do() -> None:
        removed.append(doc.delete(position, length))
        doc.insert(position, chunk)

    def undo() -> None:
        doc.delete(position, len(chunk))
        doc.insert(position, removed.pop())

    return Undoable(do=do, undo=undo, label=f"replace {length}@{position} with {chunk!r}")
