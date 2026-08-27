"""Behavioral tests for the AtomicWrite and temporarily managers."""

from __future__ import annotations

import os
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

    def test_commit_is_one_atomic_replace_from_the_same_directory(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """The docstring's old-or-new promise rests on os.replace, and on the
        temp file living beside the target (same filesystem, no EXDEV)."""
        calls: list[tuple[str, Path]] = []
        real_replace = os.replace

        def spy(src: str | os.PathLike[str], dst: str | os.PathLike[str]) -> None:
            calls.append((str(src), Path(dst)))
            real_replace(src, dst)

        monkeypatch.setattr(os, "replace", spy)
        target = tmp_path / "config.toml"
        with AtomicWrite(target) as handle:
            handle.write("v2")
        assert target.read_text() == "v2"
        assert len(calls) == 1  # exactly one atomic rename — never a rewrite
        src, dst = calls[0]
        assert dst == target
        assert Path(src).parent == target.parent  # beside the target, not /tmp

    def test_non_default_encoding_is_honored(self, tmp_path: Path) -> None:
        target = tmp_path / "latin.txt"
        with AtomicWrite(target, encoding="latin-1") as handle:
            handle.write("café")
        assert target.read_text(encoding="latin-1") == "café"
        assert target.read_bytes() == b"caf\xe9"  # actually latin-1, not utf-8


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
