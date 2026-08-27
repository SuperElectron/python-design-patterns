"""Behavioral tests for the pattern's canonical prebound Counter."""

from __future__ import annotations

import random

from patterns.python.prebound_method import Counter, increment, peek, shares_instance


class TestPreboundCounter:
    def test_module_functions_share_one_instance(self) -> None:
        assert shares_instance(increment, peek)

    def test_calls_through_either_name_hit_the_same_state(self) -> None:
        before = peek()
        value = increment()
        assert value == before + 1
        assert peek() == value

    def test_isolated_instances_do_not_touch_the_shared_one(self) -> None:
        shared_before = peek()
        isolated = Counter()
        assert isolated.increment() == 1
        assert peek() == shared_before


class TestSharesInstance:
    def test_the_stdlib_flagship_passes(self) -> None:
        assert shares_instance(random.random, random.seed)

    def test_plain_functions_fail(self) -> None:
        def f() -> None: ...
        def g() -> None: ...

        assert not shares_instance(f, g)

    def test_methods_of_different_instances_fail(self) -> None:
        assert not shares_instance(Counter().increment, Counter().increment)

    def test_empty_call_is_not_a_vacuous_pass(self) -> None:
        assert not shares_instance()
