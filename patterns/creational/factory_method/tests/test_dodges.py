"""Behavioral tests for the factory-slot mechanics in ``pattern/``."""

from __future__ import annotations

import pytest

from patterns.creational.factory_method.pattern import Factory, factory_slot


class Widget:
    def __init__(self, kind: str = "plain") -> None:
        self.kind = kind


def make_fancy() -> Widget:
    return Widget("fancy")


class TestFactorySlot:
    def test_plain_function_bare_in_class_body_is_the_trap(self) -> None:
        class Shop:
            build = make_fancy  # bound as a method: the documented mistake

        with pytest.raises(TypeError):
            # mypy flags the very mistake this test demonstrates at runtime.
            Shop().build()  # type: ignore[misc]

    def test_factory_slot_makes_the_same_assignment_safe(self) -> None:
        class Shop:
            build = factory_slot(make_fancy)

        assert Shop().build().kind == "fancy"

    def test_classes_are_safe_bare(self) -> None:
        class Shop:
            build = Widget  # classes are not descriptors: no binding

        assert Shop().build().kind == "plain"

    def test_instance_override_accepts_any_callable_unwrapped(self) -> None:
        class Shop:
            build = factory_slot(make_fancy)

            def __init__(self, build: Factory[Widget] | None = None) -> None:
                if build is not None:
                    self.build = build  # instance attributes never bind

        assert Shop(build=lambda: Widget("custom")).build().kind == "custom"

    def test_subclass_overrides_only_the_slot(self) -> None:
        class Shop:
            build = factory_slot(make_fancy)

            def describe(self) -> str:
                return f"selling {self.build().kind}"

        class PlainShop(Shop):
            build = factory_slot(Widget)

        assert Shop().describe() == "selling fancy"
        assert PlainShop().describe() == "selling plain"

    def test_slot_keeps_the_callables_signature(self) -> None:
        class Shop:
            build = factory_slot(Widget)

        assert Shop().build("bespoke").kind == "bespoke"
