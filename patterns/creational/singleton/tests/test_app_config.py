"""Behavioral tests for the app-config mini-project."""

import dataclasses
from collections.abc import Iterator

import pytest

from patterns.creational.singleton.examples.app_config import (
    get_settings,
    load_settings,
    reset_settings,
)


@pytest.fixture(autouse=True)
def clean_slate() -> Iterator[None]:
    reset_settings()  # the seam under test is also what isolates these tests
    yield
    reset_settings()


class TestAppConfig:
    def test_whole_process_shares_one_settings_object(self) -> None:
        assert get_settings() is get_settings()

    def test_reset_seam_builds_fresh(self) -> None:
        first = get_settings()
        reset_settings()
        assert get_settings() is not first

    def test_env_changes_invisible_until_reset(self, monkeypatch: pytest.MonkeyPatch) -> None:
        before = get_settings().max_workers
        monkeypatch.setenv("APP_MAX_WORKERS", str(before + 12))
        assert get_settings().max_workers == before  # cached
        reset_settings()
        assert get_settings().max_workers == before + 12  # re-read

    def test_loader_takes_an_injected_mapping(self) -> None:
        settings = load_settings({"APP_ENV": "test", "APP_DEBUG": "1"})
        assert settings.env == "test"
        assert settings.debug is True
        assert settings.max_workers == 4  # defaults still apply

    def test_settings_are_immutable(self) -> None:
        with pytest.raises(dataclasses.FrozenInstanceError):
            get_settings().env = "prod"  # type: ignore[misc]

    def test_malformed_worker_count_fails_loudly(self) -> None:
        # Documented: a non-integer APP_MAX_WORKERS raises at load time —
        # through the accessor, that means on first use.
        with pytest.raises(ValueError):
            load_settings({"APP_MAX_WORKERS": "many"})
