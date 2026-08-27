"""Behavioral tests for the atomic_deploy mini-project."""

from __future__ import annotations

from pathlib import Path

import pytest

from patterns.modern.context_manager.examples.atomic_deploy.deploy import (
    ReleaseError,
    deploy,
    require_nonempty,
)
from patterns.modern.context_manager.examples.atomic_deploy.main import main

V1 = {"app.toml": "retries = 3\n", "logging.toml": "level = 'info'\n"}


class TestDeploy:
    def test_good_release_writes_every_file(self, tmp_path: Path) -> None:
        written = deploy(V1, tmp_path)
        assert sorted(p.name for p in written) == ["app.toml", "logging.toml"]
        assert (tmp_path / "app.toml").read_text() == V1["app.toml"]

    def test_failing_release_restores_previous_contents(self, tmp_path: Path) -> None:
        deploy(V1, tmp_path)
        bad_v2 = {"app.toml": "retries = 5\n", "logging.toml": "   "}
        with pytest.raises(ReleaseError, match=r"logging\.toml"):
            deploy(bad_v2, tmp_path, validate=require_nonempty)
        # app.toml sorts before logging.toml, so it WAS written — and rolled back.
        assert (tmp_path / "app.toml").read_text() == V1["app.toml"]
        assert (tmp_path / "logging.toml").read_text() == V1["logging.toml"]

    def test_failing_release_on_fresh_target_leaves_no_files(self, tmp_path: Path) -> None:
        bad = {"a.toml": "ok = true\n", "z.toml": ""}
        with pytest.raises(ReleaseError):
            deploy(bad, tmp_path, validate=require_nonempty)
        assert list(tmp_path.iterdir()) == []  # a.toml was created, then removed


class TestDemo:
    def test_demo_shows_deploy_then_rollback(self, capsys: pytest.CaptureFixture[str]) -> None:
        main()
        out = capsys.readouterr().out
        assert "v1 deployed: ['app.toml', 'logging.toml']" in out
        assert "v2 rejected" in out
        assert "app.toml still reads: retries = 3" in out
