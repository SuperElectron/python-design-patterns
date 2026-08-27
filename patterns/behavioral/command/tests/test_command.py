"""Behavioral tests for all three command variants."""

from functools import partial

from patterns.behavioral.command import naive, pythonic, real_world


class TestNaive:
    def test_execute_mutates_receiver(self) -> None:
        doc, editor = naive.Document(), naive.Editor()
        editor.do(naive.AppendText(doc, "hi"))
        assert doc.text == "hi"

    def test_undo_reverses_last_command(self) -> None:
        doc, editor = naive.Document(), naive.Editor()
        editor.do(naive.AppendText(doc, "hello"))
        editor.do(naive.AppendText(doc, " world"))
        editor.undo()
        assert doc.text == "hello"

    def test_undo_on_empty_history_is_a_noop(self) -> None:
        naive.Editor().undo()  # must not raise


class TestPythonic:
    def test_partial_queue_runs_in_order(self) -> None:
        log: list[str] = []
        pythonic.run_queue([partial(log.append, "a"), partial(log.append, "b")])
        assert log == ["a", "b"]

    def test_undoable_editor_round_trip(self) -> None:
        editor = pythonic.Editor()
        editor.append("hello")
        editor.append(" world")
        assert editor.text == "hello world"
        editor.undo()
        editor.undo()
        assert editor.text == ""


class TestRealWorld:
    def test_scheduler_invokes_queued_commands_in_order(self) -> None:
        assert real_world.run_scheduled(["x", "y", "z"]) == ["x", "y", "z"]
