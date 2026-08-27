"""Behavioral tests for the AtomicWrite and temporarily managers."""

from __future__ import annotations

from pathlib import Path

import pytest

from patterns.modern.context_manager.pattern import AtomicWrite, temporarily


class TestAtomicWrite:
    def test_clean_exit_commits(self, tmp_path: Path) -> None:
        target = tmp_path / "config.toml"
        with AtomicWrite(target) as handle:
            handle.write("v2")
        assert target.read_text() == "v2"

    def test_exception_discards_and_keeps_the_old_content(self, tmp_path: Path) -> None:
        target = tmp_path / "config.toml"
        target.write_text("v1")
        with pytest.raises(RuntimeError, match="boom"), AtomicWrite(target) as handle:
            handle.write("half-written v2")
            raise RuntimeError("boom")
        assert target.read_text() == "v1"  # reader never sees the half-write

    def test_exception_on_a_fresh_path_leaves_nothing(self, tmp_path: Path) -> None:
        target = tmp_path / "new.toml"
        with pytest.raises(RuntimeError), AtomicWrite(target) as handle:
            handle.write("partial")
            raise RuntimeError("boom")
        assert not target.exists()
        assert list(tmp_path.iterdir()) == []  # no orphaned temp file either


class TestTemporarily:
    class Settings:
        retries = 3

    def test_restores_after_the_block(self) -> None:
        settings = self.Settings()
        with temporarily(settings, "retries", 99):
            assert settings.retries == 99
        assert settings.retries == 3

    def test_restores_even_when_the_body_raises(self) -> None:
        settings = self.Settings()
        with pytest.raises(ValueError), temporarily(settings, "retries", 99):
            raise ValueError("mid-block failure")
        assert settings.retries == 3

    def test_never_swallows_the_body_exception(self) -> None:
        settings = self.Settings()
        # The KeyError reaches pytest.raises: __exit__ returns falsy.
        with pytest.raises(KeyError), temporarily(settings, "retries", 0):
            raise KeyError("must propagate")
