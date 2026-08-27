"""Behavioral tests for the pattern's Sentinel and MISSING."""

from __future__ import annotations

from patterns.python.sentinel_object import MISSING, Sentinel


class TestSentinel:
    def test_identity_is_the_meaning(self) -> None:
        assert MISSING is MISSING
        assert Sentinel("MISSING") is not MISSING  # same name, different marker

    def test_a_sentinel_lives_in_no_value_domain(self) -> None:
        store: dict[str, object] = {"none": None, "zero": 0, "empty": ""}
        assert all(store.get(k, MISSING) is not MISSING for k in store)
        assert store.get("absent", MISSING) is MISSING

    def test_repr_is_debuggable(self) -> None:
        assert repr(MISSING) == "<MISSING>"
        assert repr(Sentinel("NOT_GIVEN")) == "<NOT_GIVEN>"

    def test_distinguishes_stored_none_from_absence(self) -> None:
        cache: dict[str, str | None] = {"hit": None}
        assert cache.get("hit", MISSING) is None
        assert cache.get("miss", MISSING) is MISSING

    def test_equality_cannot_forge_a_sentinel(self) -> None:
        # No name-based __eq__: a same-named marker is a different marker.
        assert (Sentinel("MISSING") == MISSING) is False
        assert Sentinel("MISSING") != MISSING

    def test_a_sentinel_is_truthy(self) -> None:
        # "if value:" must never mistake the marker for an absence/falsy value.
        assert bool(MISSING) is True

    def test_every_import_path_yields_the_same_marker(self) -> None:
        from patterns.python.sentinel_object import MISSING as unit_missing
        from patterns.python.sentinel_object.pattern import MISSING as pkg_missing
        from patterns.python.sentinel_object.pattern.sentinel import (
            MISSING as module_missing,
        )

        assert unit_missing is pkg_missing is module_missing
