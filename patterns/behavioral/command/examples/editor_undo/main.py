"""Demo: an editing session with undo, redo, and a command log."""

from __future__ import annotations

from patterns.behavioral.command.examples.editor_undo.editing import (
    delete_span,
    insert_text,
    replace_span,
)
from patterns.behavioral.command.examples.editor_undo.models import Document
from patterns.behavioral.command.pattern import UndoStack


def main() -> None:
    doc = Document()
    history = UndoStack()

    history.push(insert_text(doc, 0, "hello world"))
    history.push(replace_span(doc, 0, 5, "goodbye"))
    history.push(delete_span(doc, 7, 6))
    print(f"after edits: {doc.text!r}")

    history.undo()
    history.undo()
    print(f"after 2 undos: {doc.text!r}")

    history.redo()
    print(f"after redo: {doc.text!r}")
    print("session log:", " | ".join(history.log()))


if __name__ == "__main__":
    main()
