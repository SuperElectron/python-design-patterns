"""Behavioral tests for all three memento variants."""

from patterns.behavioral.memento import naive, pythonic, real_world


class TestNaive:
    def test_save_and_restore(self) -> None:
        editor, history = naive.Editor(), naive.History()
        editor.type_text("hello")
        history.push(editor.save())
        editor.type_text(" world")
        editor.restore(history.pop())
        assert (editor.text, editor.cursor) == ("hello", 5)


class TestPythonic:
    def test_undo_restores_previous_state(self) -> None:
        editor = pythonic.Editor()
        editor.type_text("hello")
        editor.type_text(" world")
        editor.undo()
        assert editor.state == pythonic.EditorState("hello", 5)

    def test_undo_to_the_beginning_then_noop(self) -> None:
        editor = pythonic.Editor()
        editor.type_text("x")
        editor.undo()
        editor.undo()  # empty history: must not raise
        assert editor.state == pythonic.EditorState()

    def test_snapshots_are_immutable(self) -> None:
        import dataclasses

        import pytest

        with pytest.raises(dataclasses.FrozenInstanceError):
            pythonic.EditorState().text = "nope"  # type: ignore[misc]


class TestRealWorld:
    def test_pickle_round_trip_restores_state(self) -> None:
        game = real_world.Game()
        game.inventory.append("sword")
        save = real_world.checkpoint(game)
        game.level, game.inventory = 9, []
        restored = real_world.rollback(save)
        assert (restored.level, restored.inventory) == (1, ["sword"])

    def test_snapshot_is_independent_of_later_mutation(self) -> None:
        game = real_world.Game(inventory=["map"])
        save = real_world.checkpoint(game)
        game.inventory.clear()
        assert real_world.rollback(save).inventory == ["map"]
