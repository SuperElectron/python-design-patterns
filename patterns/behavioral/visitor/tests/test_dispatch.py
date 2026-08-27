"""Behavioral tests for the Operation building block."""

from __future__ import annotations

from dataclasses import dataclass

import pytest

from patterns.behavioral.visitor import Operation, UnhandledNodeError


@dataclass(frozen=True)
class Circle:
    radius: float


@dataclass(frozen=True)
class Square:
    side: float


class TestDispatch:
    def test_calls_dispatch_on_the_nodes_type(self) -> None:
        area: Operation[float] = Operation("area")

        @area.register
        def _(node: Circle) -> float:
            return 3.14159 * node.radius**2

        @area.register
        def _(node: Square) -> float:
            return node.side**2

        assert area(Square(3.0)) == 9.0
        assert area(Circle(1.0)) == pytest.approx(3.14159)

    def test_register_hands_the_case_back_usable(self) -> None:
        name: Operation[str] = Operation("name")

        @name.register
        def circle_name(node: Circle) -> str:
            return "circle"

        assert circle_name(Circle(1.0)) == "circle"

    def test_registered_types_reports_the_handled_family(self) -> None:
        op: Operation[str] = Operation("op")

        @op.register
        def _(node: Circle) -> str:
            return "c"

        assert op.registered_types() == frozenset({Circle})


class TestStrictDefault:
    def test_unregistered_type_raises_naming_operation_and_handled_types(self) -> None:
        area: Operation[float] = Operation("area")

        @area.register
        def _(node: Circle) -> float:
            return 0.0

        with pytest.raises(UnhandledNodeError, match=r"'area' has no case for Square.*Circle"):
            area(Square(2.0))

    def test_operations_are_independent_families(self) -> None:
        first: Operation[int] = Operation("first")
        second: Operation[int] = Operation("second")

        @first.register
        def _(node: Circle) -> int:
            return 1

        assert first(Circle(1.0)) == 1
        with pytest.raises(UnhandledNodeError):
            second(Circle(1.0))
