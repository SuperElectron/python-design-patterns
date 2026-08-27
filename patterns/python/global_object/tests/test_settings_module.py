"""Behavioral tests for the settings-module mini-project.

The load-bearing assertion: importing the settings module does no expensive
work — the zone table's factory runs zero times until first use, once ever.
"""

from __future__ import annotations

import subprocess
import sys
from collections.abc import Iterator
from pathlib import Path

import pytest

from patterns.python.global_object.examples.settings_module import settings
from patterns.python.global_object.examples.settings_module.__main__ import main
from patterns.python.global_object.examples.settings_module.shipping import (
    is_valid_slug,
    shipping_zone,
)


@pytest.fixture(autouse=True)
def fresh_lazy_state() -> Iterator[None]:
    """The pattern's test seam: order-independence via reset()."""
    settings.ZONE_TABLE.reset()
    settings.FACTORY_RUNS = 0
    yield
    settings.ZONE_TABLE.reset()
    settings.FACTORY_RUNS = 0


REPO_ROOT = Path(__file__).resolve().parents[4]


class TestImportStaysCheap:
    def test_import_did_not_build_the_expensive_table(self) -> None:
        # A fresh subprocess is the only honest witness: in-process, this
        # module is already imported and the autouse reset fixture would have
        # erased the evidence either way. Here nothing can reset before the
        # assertion reads the counter.
        probe = (
            "from patterns.python.global_object.examples.settings_module import settings; "
            "assert settings.FACTORY_RUNS == 0, settings.FACTORY_RUNS; "
            "assert settings.ZONE_TABLE.initialized is False"
        )
        result = subprocess.run(
            [sys.executable, "-c", probe],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        assert result.returncode == 0, result.stderr

    def test_first_use_builds_once_and_only_once(self) -> None:
        assert shipping_zone("CA") == 1
        assert shipping_zone("DE") == 3
        assert settings.FACTORY_RUNS == 1


class TestSettingsBehavior:
    def test_constants_are_immutable_types(self) -> None:
        assert isinstance(settings.SUPPORTED_LOCALES, frozenset)
        assert settings.RETRY_LIMIT == 3

    def test_prebuilt_regex_validates_slugs(self) -> None:
        assert is_valid_slug("summer-sale")
        assert not is_valid_slug("Summer Sale!")
        # Fails past position 0: fullmatch must reject what match would accept.
        assert not is_valid_slug("summer sale!")

    def test_unknown_country_is_a_domain_error(self) -> None:
        with pytest.raises(ValueError, match="no shipping zone"):
            shipping_zone("ZZ")

    def test_consumers_share_one_table_instance(self) -> None:
        assert settings.ZONE_TABLE.get() is settings.ZONE_TABLE.get()


class TestDemo:
    def test_demo_tells_the_lazy_story(self, capsys: pytest.CaptureFixture[str]) -> None:
        main()
        out = capsys.readouterr().out
        assert "lazy built at import? False" in out
        assert "shipping_zone('FR'):  3" in out
        assert "lazy built after use? True" in out
        assert "factory ran:          1 time(s)" in out
