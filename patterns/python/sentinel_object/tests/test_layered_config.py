"""Behavioral tests for the layered-config mini-project."""

from __future__ import annotations

import pytest

from patterns.python.sentinel_object.examples.layered_config import (
    EmailNotifier,
    LayeredConfig,
    NullNotifier,
    notifier_for,
)
from patterns.python.sentinel_object.examples.layered_config.__main__ import main


def build_config() -> LayeredConfig:
    return LayeredConfig(
        defaults={"timeout_s": 30, "alert_email": "ops@example.com", "proxy": None},
        file={"timeout_s": 60, "alert_email": None},
        cli={"timeout_s": 10},
    )


class TestLayering:
    def test_highest_layer_with_the_key_wins(self) -> None:
        config = build_config()
        assert config.get("timeout_s") == 10
        assert config.source_of("timeout_s") == "cli"

    def test_a_stored_none_wins_over_lower_layers(self) -> None:
        # The file layer explicitly disabled alerts; the default email below
        # it must NOT shine through — None is a value, not a hole.
        config = build_config()
        assert config.get("alert_email") is None
        assert config.source_of("alert_email") == "file"

    def test_none_in_defaults_is_still_a_value(self) -> None:
        config = build_config()
        assert config.get("proxy") is None
        assert config.source_of("proxy") == "defaults"

    def test_missing_key_without_default_raises(self) -> None:
        with pytest.raises(KeyError, match="not set in any layer"):
            build_config().get("nope")

    def test_missing_key_with_default_returns_it(self) -> None:
        config = build_config()
        assert config.get("nope", default=42) == 42
        assert config.get("nope", default=None) is None  # None is a usable default
        assert config.source_of("nope") == "unset"


class TestNullObject:
    def test_disabled_alerts_yield_the_null_notifier(self) -> None:
        notifier = notifier_for(build_config())
        assert isinstance(notifier, NullNotifier)
        notifier.notify("nobody hears this")  # and that is fine — no branching

    def test_configured_email_yields_a_real_notifier(self) -> None:
        config = LayeredConfig(defaults={"alert_email": "oncall@example.com"})
        notifier = notifier_for(config)
        assert isinstance(notifier, EmailNotifier)
        notifier.notify("disk almost full")
        assert notifier.sent == ["to oncall@example.com: disk almost full"]


class TestDemo:
    def test_main_shows_provenance_and_the_null_notifier(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        main()
        out = capsys.readouterr().out
        assert "(from cli)" in out
        assert "(from file)" in out
        assert "NullNotifier" in out
