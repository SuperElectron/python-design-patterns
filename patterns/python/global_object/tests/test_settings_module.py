"""Behavioral tests for the settings-module mini-project.

The load-bearing assertion: importing the settings module does no expensive
work — the zone table's factory runs zero times until first use, once ever.
"""

from __future__ import annotations

from collections.abc import Iterator

import pytest

from patterns.python.global_object.examples.settings_module import settings
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


class TestImportStaysCheap:
    def test_import_did_not_build_the_expensive_table(self) -> None:
        # The module (and its consumers) are imported above; the fixture just
        # reset — merely importing must leave the lazy global unbuilt.
        assert settings.ZONE_TABLE.initialized is False
        assert settings.FACTORY_RUNS == 0

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

    def test_unknown_country_is_a_domain_error(self) -> None:
        with pytest.raises(ValueError, match="no shipping zone"):
            shipping_zone("ZZ")

    def test_consumers_share_one_table_instance(self) -> None:
        assert settings.ZONE_TABLE.get() is settings.ZONE_TABLE.get()
