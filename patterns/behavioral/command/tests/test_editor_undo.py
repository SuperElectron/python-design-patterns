"""Behavioral tests for the editor-undo mini-project."""

from __future__ import annotations

from patterns.behavioral.command.examples.editor_undo.editing import (
    delete_span,
    insert_text,
    replace_span,
)
from patterns.behavioral.command.examples.editor_undo.models import Document
from patterns.behavioral.command.pattern import UndoStack


class TestEditingCommands:
    def test_insert_then_undo_restores_exact_text(self) -> None:
        doc = Document("hello world")
        stack = UndoStack()
        stack.push(insert_text(doc, 5, ","))
        assert doc.text == "hello, world"
        stack.undo()
        assert doc.text == "hello world"

    def test_delete_remembers_what_it_removed(self) -> None:
        doc = Document("hello world")
        stack = UndoStack()
        stack.push(delete_span(doc, 0, 6))
        assert doc.text == "world"
        stack.undo()
        assert doc.text == "hello world"  # the removed span came back verbatim

    def test_replace_round_trips(self) -> None:
        doc = Document("hello world")
        stack = UndoStack()
        stack.push(replace_span(doc, 0, 5, "goodbye"))
        assert doc.text == "goodbye world"
        stack.undo()
        assert doc.text == "hello world"

    def test_delete_undo_redo_cycle_reuses_captured_state(self) -> None:
        doc = Document("abcdef")
        stack = UndoStack()
        stack.push(delete_span(doc, 1, 3))
        stack.undo()
        stack.redo()
        assert doc.text == "aef"
        stack.undo()
        assert doc.text == "abcdef"

    def test_session_log_reads_as_an_audit_trail(self) -> None:
        doc = Document()
        stack = UndoStack()
        stack.push(insert_text(doc, 0, "hi"))
        stack.push(delete_span(doc, 0, 1))
        assert stack.log() == ("insert 'hi'@0", "delete 1@0")

    def test_editing_session_end_to_end(self) -> None:
        doc = Document()
        stack = UndoStack()
        stack.push(insert_text(doc, 0, "hello world"))
        stack.push(replace_span(doc, 0, 5, "goodbye"))
        stack.push(delete_span(doc, 7, 6))
        assert doc.text == "goodbye"
        stack.undo()
        stack.undo()
        assert doc.text == "hello world"
        stack.redo()
        assert doc.text == "goodbye world"
