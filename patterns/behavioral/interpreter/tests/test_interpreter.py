"""Behavioral tests for all three interpreter variants."""

import pytest

from patterns.behavioral.interpreter import naive, pythonic, real_world


class TestNaive:
    def test_tree_interprets(self) -> None:
        tree = naive.Mul(naive.Add(naive.Number(2), naive.Number(3)), naive.Number(4))
        assert tree.interpret() == 20


class TestPythonic:
    def test_tuple_tree_interprets(self) -> None:
        assert pythonic.interpret(("*", ("+", 2, 3), 4)) == 20

    def test_bare_number(self) -> None:
        assert pythonic.interpret(7) == 7

    def test_language_extends_by_dict_entry(self) -> None:
        assert pythonic.interpret(("-", 10, 4)) == 6


class TestRealWorld:
    def test_safe_arithmetic(self) -> None:
        assert real_world.safe_eval("2 * (3 + 4)") == 14.0
        assert real_world.safe_eval("-5 + 1") == -4.0

    def test_attack_is_rejected_not_executed(self) -> None:
        with pytest.raises(ValueError, match="disallowed"):
            real_world.safe_eval("__import__('os').system('true')")

    def test_names_are_rejected(self) -> None:
        with pytest.raises(ValueError):
            real_world.safe_eval("x + 1")

    def test_bool_constants_are_rejected(self) -> None:
        # bool subclasses int; a safe evaluator must not compute True + 1.
        with pytest.raises(ValueError, match="disallowed"):
            real_world.safe_eval("True + 1")

    def test_hostile_nesting_gets_a_clean_error_not_a_crash(self) -> None:
        bomb = "1" + " + 1" * 200  # deeper than MAX_DEPTH
        with pytest.raises(ValueError, match="deeply nested"):
            real_world.safe_eval(bomb)
