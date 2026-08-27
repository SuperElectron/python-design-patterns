"""Behavioral tests for the pattern's ``Registry``."""

from __future__ import annotations

from collections.abc import Callable

import pytest

from patterns.modern.registry import Registry, UnknownKeyError

Handler = Callable[[str], str]


def make_registry() -> Registry[Handler]:
    return Registry(kind="handler")


class TestRegistration:
    def test_the_decorator_registers_and_returns_the_function_unchanged(self) -> None:
        registry = make_registry()

        @registry.register("upper")
        def shout(text: str) -> str:
            return text.upper()

        assert registry.get("upper") is shout
        assert shout("hi") == "HI"  # still an ordinary function

    def test_duplicate_names_are_an_error(self) -> None:
        registry = make_registry()
        registry.register("upper")(str.upper)
        with pytest.raises(ValueError, match="handler 'upper' is already registered"):
            registry.register("upper")(str.lower)
        assert registry.get("upper")("hi") == "HI"  # original untouched

    def test_replace_makes_an_override_explicit(self) -> None:
        registry = make_registry()
        registry.register("case")(str.upper)
        registry.register("case", replace=True)(str.lower)
        assert registry.get("case")("Hi") == "hi"


class TestLookup:
    def test_unknown_names_fail_loudly_and_list_known_ones(self) -> None:
        registry = make_registry()
        registry.register("upper")(str.upper)
        registry.register("lower")(str.lower)
        message = r"unknown handler 'title' \(known: lower, upper\)"
        with pytest.raises(UnknownKeyError, match=message):
            registry.get("title")

    def test_an_empty_registry_says_so(self) -> None:
        with pytest.raises(UnknownKeyError, match="<none>"):
            make_registry().get("anything")

    def test_introspection_surface(self) -> None:
        registry = make_registry()
        registry.register("b")(str.upper)
        registry.register("a")(str.lower)
        assert registry.names() == ("a", "b")
        assert "a" in registry and "z" not in registry
        assert len(registry) == 2
