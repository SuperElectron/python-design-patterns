"""Behavioral tests for the InternPool building block."""

from __future__ import annotations

from dataclasses import dataclass

import pytest

from patterns.structural.flyweight.pattern import InternPool


@dataclass(frozen=True)
class Color:
    name: str


def test_same_key_yields_the_identical_object() -> None:
    pool: InternPool[str, Color] = InternPool(Color)
    assert pool.get("red") is pool.get("red")


def test_distinct_keys_stay_distinct() -> None:
    pool: InternPool[str, Color] = InternPool(Color)
    assert pool.get("red") is not pool.get("blue")
    assert len(pool) == 2


def test_build_runs_once_per_key() -> None:
    built: list[str] = []

    def build(name: str) -> Color:
        built.append(name)
        return Color(name)

    pool = InternPool(build)
    pool.get("red"), pool.get("red"), pool.get("red")
    assert built == ["red"]


def test_contains_reflects_what_was_interned() -> None:
    pool: InternPool[str, Color] = InternPool(Color)
    pool.get("red")
    assert "red" in pool
    assert "blue" not in pool


def test_strict_pool_accepts_frozen_values() -> None:
    pool: InternPool[str, Color] = InternPool(Color, strict=True)
    assert pool.get("red") is pool.get("red")


def test_strict_pool_refuses_mutable_values() -> None:
    pool: InternPool[str, list[str]] = InternPool(lambda k: [k], strict=True)
    with pytest.raises(TypeError, match="must be immutable"):
        pool.get("red")
