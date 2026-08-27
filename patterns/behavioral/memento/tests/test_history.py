"""Behavioral tests for the Memento pattern's History caretaker."""

from __future__ import annotations

import pytest

from patterns.behavioral.memento import History, NoSnapshotError


class TestUndoStack:
    def test_undo_returns_snapshots_last_in_first_out(self) -> None:
        history: History[str] = History()
        history.save("first")
        history.save("second")
        assert history.undo() == "second"
        assert history.undo() == "first"

    def test_undo_on_empty_history_raises(self) -> None:
        history: History[str] = History()
        with pytest.raises(NoSnapshotError):
            history.undo()

    def test_save_returns_the_snapshot_unchanged(self) -> None:
        history: History[tuple[int, ...]] = History()
        snapshot = (1, 2, 3)
        assert history.save(snapshot) is snapshot

    def test_len_counts_only_the_undo_stack(self) -> None:
        history: History[int] = History()
        history.save(1)
        history.checkpoint("named", 2)
        assert len(history) == 1


class TestCheckpoints:
    def test_rollback_to_returns_the_named_snapshot(self) -> None:
        history: History[int] = History()
        history.checkpoint("before-upgrade", 41)
        history.save(42)
        assert history.rollback_to("before-upgrade") == 41

    def test_unknown_checkpoint_raises_and_names_the_known_ones(self) -> None:
        history: History[int] = History()
        history.checkpoint("alpha", 1)
        with pytest.raises(NoSnapshotError, match="alpha"):
            history.rollback_to("beta")

    def test_renaming_a_checkpoint_overwrites_it(self) -> None:
        history: History[int] = History()
        history.checkpoint("mark", 1)
        history.checkpoint("mark", 2)
        assert history.rollback_to("mark") == 2

    def test_bool_reflects_any_stored_snapshot(self) -> None:
        history: History[int] = History()
        assert not history
        history.checkpoint("only-named", 1)
        assert history
