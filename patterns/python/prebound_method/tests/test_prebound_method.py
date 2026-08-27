"""Behavioral tests for all three prebound-method variants."""

from typing import Any

from patterns.python.prebound_method import naive, pythonic, real_world


class TestNaive:
    def test_loose_global_counts(self) -> None:
        start = naive.increment()
        assert naive.increment() == start + 1

    def test_diy_instances_are_isolated(self) -> None:
        a, b = naive.Counter(), naive.Counter()
        a.increment()
        assert b.count == 0


class TestPythonic:
    def test_module_functions_share_the_hidden_instance(self) -> None:
        before = pythonic.peek()
        pythonic.increment()
        assert pythonic.peek() == before + 1

    def test_functions_are_bound_methods_of_one_instance(self) -> None:
        increment: Any = pythonic.increment
        peek: Any = pythonic.peek
        assert increment.__self__ is peek.__self__

    def test_public_class_gives_isolation(self) -> None:
        isolated = pythonic.Counter()
        pythonic.increment()
        assert isolated.peek() == 0


class TestRealWorld:
    def test_random_module_is_prebound(self) -> None:
        assert real_world.module_functions_share_one_instance()

    def test_seeding_is_shared_state(self) -> None:
        assert real_world.seeded_sequence(7, 3) == real_world.seeded_sequence(7, 3)
