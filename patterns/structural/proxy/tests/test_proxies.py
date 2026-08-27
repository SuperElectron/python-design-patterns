"""Behavioral tests for the proxy building blocks."""

from __future__ import annotations

import pytest

from patterns.structural.proxy.pattern import LazyProxy, MeteringProxy, ProtectionProxy


class Subject:
    def __init__(self) -> None:
        self.color = "green"

    def greet(self) -> str:
        return "hello"


def test_lazy_proxy_defers_construction_until_first_access() -> None:
    built: list[str] = []

    def factory() -> Subject:
        built.append("now")
        return Subject()

    proxy = LazyProxy(factory)
    assert not proxy.is_built
    assert built == []
    assert proxy.greet() == "hello"
    assert proxy.is_built
    assert built == ["now"]


def test_lazy_proxy_builds_exactly_once() -> None:
    built: list[str] = []

    def factory() -> Subject:
        built.append("now")
        return Subject()

    proxy = LazyProxy(factory)
    proxy.greet(), proxy.greet(), proxy.color
    assert built == ["now"]


def test_lazy_proxy_caches_a_none_subject_once() -> None:
    # A factory may legitimately produce None (e.g. a failed connect that the
    # caller inspects); that result is still "built" and must not retrigger.
    built: list[str] = []

    def factory() -> None:
        built.append("now")
        return None

    proxy = LazyProxy(factory)
    with pytest.raises(AttributeError):
        proxy.anything  # noqa: B018 — the access itself is the trigger
    with pytest.raises(AttributeError):
        proxy.other  # noqa: B018
    assert built == ["now"]
    assert proxy.is_built


def test_protection_proxy_forwards_allowed_and_denies_the_rest() -> None:
    proxy = ProtectionProxy(Subject(), allow=lambda name: name == "greet")
    assert proxy.greet() == "hello"
    with pytest.raises(PermissionError, match="color"):
        proxy.color  # noqa: B018 — the access itself is the assertion


def test_metering_proxy_counts_each_attribute_access() -> None:
    proxy = MeteringProxy(Subject())
    proxy.greet(), proxy.greet(), proxy.color
    assert proxy.access_counts == {"greet": 2, "color": 1}


def test_stacked_proxies_compose_their_mediations() -> None:
    built: list[str] = []

    def factory() -> Subject:
        built.append("now")
        return Subject()

    stack = MeteringProxy(ProtectionProxy(LazyProxy(factory), lambda n: n == "greet"))
    with pytest.raises(PermissionError):
        stack.color  # noqa: B018 — denied by the protection layer
    assert built == []  # denial happened before the lazy layer built anything
    assert stack.greet() == "hello"
    assert built == ["now"]
    assert stack.access_counts == {"color": 1, "greet": 1}  # denials metered too


def test_the_disguise_is_skin_deep() -> None:
    # Dunder lookups bypass __getattr__: a subject that supports len() does
    # not make the proxy support it. That is the caveat, behaviorally.
    class Sized:
        def __len__(self) -> int:
            return 3

    proxy = LazyProxy(Sized)
    with pytest.raises(TypeError):
        len(proxy)
