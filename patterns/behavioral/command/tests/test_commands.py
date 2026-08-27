"""Behavioral tests for the Command pattern's library code."""

from __future__ import annotations

from patterns.behavioral.command.pattern import Undoable, UndoStack


def _append_command(log: list[str], item: str) -> Undoable:
    return Undoable(
        do=lambda: log.append(item),
        undo=lambda: log.remove(item),
        label=f"append {item}",
    )


class TestUndoStack:
    def test_push_executes_and_records(self) -> None:
        log: list[str] = []
        stack = UndoStack()
        stack.push(_append_command(log, "a"))
        stack.push(_append_command(log, "b"))
        assert log == ["a", "b"]
        assert stack.log() == ("append a", "append b")

    def test_undo_reverses_newest_first(self) -> None:
        log: list[str] = []
        stack = UndoStack()
        stack.push(_append_command(log, "a"))
        stack.push(_append_command(log, "b"))
        undone = stack.undo()
        assert undone is not None and undone.label == "append b"
        assert log == ["a"]

    def test_redo_replays_the_undone_command(self) -> None:
        log: list[str] = []
        stack = UndoStack()
        stack.push(_append_command(log, "a"))
        stack.undo()
        assert log == []
        redone = stack.redo()
        assert redone is not None and redone.label == "append a"
        assert log == ["a"]

    def test_new_push_clears_the_redo_branch(self) -> None:
        log: list[str] = []
        stack = UndoStack()
        stack.push(_append_command(log, "a"))
        stack.undo()
        stack.push(_append_command(log, "b"))  # diverge: the undone future dies
        assert stack.redo() is None
        assert log == ["b"]

    def test_undo_redo_on_empty_history_are_safe(self) -> None:
        stack = UndoStack()
        assert stack.undo() is None
        assert stack.redo() is None
        assert not stack.can_undo
        assert not stack.can_redo

    def test_log_reflects_only_applied_commands(self) -> None:
        log: list[str] = []
        stack = UndoStack()
        stack.push(_append_command(log, "a"))
        stack.push(_append_command(log, "b"))
        stack.undo()
        assert stack.log() == ("append a",)
