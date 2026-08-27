"""Behavioral tests for the config-checkpoints mini-project."""

from __future__ import annotations

import pytest

from patterns.behavioral.memento.examples.config_checkpoints import (
    ConfigEditor,
    InvalidConfigError,
    ServiceConfig,
)
from patterns.behavioral.memento.examples.config_checkpoints.__main__ import main


class TestValidateOrRollback:
    def test_a_valid_batch_commits_atomically(self) -> None:
        editor = ConfigEditor()
        editor.apply({"workers": 8, "log_level": "ERROR"})
        assert editor.config.workers == 8
        assert editor.config.log_level == "ERROR"

    def test_an_invalid_batch_is_rejected_whole(self) -> None:
        editor = ConfigEditor()
        before = editor.config
        with pytest.raises(InvalidConfigError, match="workers"):
            editor.apply({"workers": 0, "log_level": "ERROR"})
        assert editor.config is before  # not even the valid half applied

    def test_a_rejected_batch_does_not_pollute_undo(self) -> None:
        editor = ConfigEditor()
        editor.apply({"workers": 4})
        with pytest.raises(InvalidConfigError):
            editor.apply({"timeout_s": -1.0})
        assert editor.undo() == ServiceConfig()  # straight back to the start

    def test_error_message_names_every_broken_rule(self) -> None:
        editor = ConfigEditor()
        with pytest.raises(InvalidConfigError, match=r"workers.*timeout_s"):
            editor.apply({"workers": -1, "timeout_s": 0.0})


class TestUndoAndCheckpoints:
    def test_undo_steps_back_one_committed_batch(self) -> None:
        editor = ConfigEditor()
        editor.apply({"workers": 4})
        editor.apply({"workers": 16})
        assert editor.undo().workers == 4
        assert editor.undo().workers == 2

    def test_rollback_to_a_named_checkpoint_after_later_edits(self) -> None:
        editor = ConfigEditor()
        editor.apply({"log_level": "WARNING"})
        editor.checkpoint("before-upgrade")
        editor.apply({"feature_flags": frozenset({"risky"})})
        restored = editor.rollback_to("before-upgrade")
        assert restored.log_level == "WARNING"
        assert restored.feature_flags == frozenset()

    def test_a_rollback_is_itself_undoable(self) -> None:
        editor = ConfigEditor()
        editor.checkpoint("start")
        editor.apply({"workers": 9})
        editor.rollback_to("start")
        assert editor.undo().workers == 9


class TestDemo:
    def test_main_shows_reject_upgrade_and_rollback(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        main()
        out = capsys.readouterr().out
        assert "batch rejected" in out
        assert "new-renderer" in out
        assert "rolled back" in out
