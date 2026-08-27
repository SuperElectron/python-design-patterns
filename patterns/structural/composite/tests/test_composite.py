"""Behavioral tests for the Composite building block."""

from __future__ import annotations

from dataclasses import dataclass

import pytest

from patterns.structural.composite import Composite


@dataclass(frozen=True)
class Task:
    hours: int

    def total(self) -> int:
        return self.hours


class TestRollup:
    def test_a_container_totals_its_leaves(self) -> None:
        team = Composite[int](sum, [Task(3), Task(5)])
        assert team.total() == 8

    def test_nesting_rolls_up_through_every_level(self) -> None:
        team = Composite[int](sum, [Task(3), Task(5)])
        project = Composite[int](sum, [team, Task(8)])
        portfolio = Composite[int](sum, [project])
        assert portfolio.total() == 16

    def test_an_empty_container_totals_the_combine_identity(self) -> None:
        assert Composite[int](sum).total() == 0

    def test_leaf_and_subtree_are_interchangeable_to_callers(self) -> None:
        def describe(node: Task | Composite[int]) -> str:
            return f"{node.total()}h"  # never asks which kind it holds

        assert describe(Task(4)) == "4h"
        assert describe(Composite[int](sum, [Task(4)])) == "4h"


class TestHonestInterfaces:
    def test_child_management_lives_only_on_the_container(self) -> None:
        assert not hasattr(Task(1), "add")
        assert not hasattr(Task(1), "remove")

    def test_add_and_remove_change_the_rollup(self) -> None:
        team = Composite[int](sum, [Task(3)])
        extra = Task(5)
        team.add(extra)
        assert team.total() == 8
        team.remove(extra)
        assert team.total() == 3

    def test_removing_a_stranger_raises(self) -> None:
        with pytest.raises(ValueError):
            Composite[int](sum).remove(Task(1))

    def test_iteration_walks_direct_children_in_order(self) -> None:
        first, second = Task(1), Task(2)
        team = Composite[int](sum, [first, second])
        assert list(team) == [first, second]
        assert len(team) == 2
