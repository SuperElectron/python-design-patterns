"""Behavioral tests for the Interpreter pattern's library code."""

from __future__ import annotations

import operator

import pytest

from patterns.behavioral.interpreter.pattern import (
    Expr,
    Interpreter,
    Operation,
    Value,
    safe_eval,
)


def _binop(fn: object) -> Operation:
    def apply(args: tuple[Value, ...]) -> Value:
        left, right = args
        assert callable(fn)
        result: Value = fn(left, right)
        return result

    return apply


ARITHMETIC: dict[str, Operation] = {
    "+": _binop(operator.add),
    "*": _binop(operator.mul),
    "-": _binop(operator.sub),
}


class TestInterpreter:
    def test_evaluates_nested_sentences(self) -> None:
        interpreter = Interpreter(ARITHMETIC)
        tree: Expr = ("*", ("+", 2, 3), 4)
        assert interpreter.evaluate(tree) == 20

    def test_leaves_pass_through_the_resolver(self) -> None:
        context = {"age": 31}
        interpreter = Interpreter(
            ARITHMETIC,
            resolve=lambda leaf: context.get(leaf, leaf) if isinstance(leaf, str) else leaf,
        )
        assert interpreter.evaluate(("+", "age", 1)) == 32

    def test_unknown_operation_is_a_value_error(self) -> None:
        interpreter = Interpreter(ARITHMETIC)
        with pytest.raises(ValueError, match="unknown operation"):
            interpreter.evaluate(("/", 1, 2))

    def test_depth_bomb_fails_cleanly(self) -> None:
        interpreter = Interpreter(ARITHMETIC)
        bomb: Expr = 1
        for _ in range(200):
            bomb = ("+", bomb, 1)
        with pytest.raises(ValueError, match="too deeply nested"):
            interpreter.evaluate(bomb)

    def test_malformed_tuple_head_rejected(self) -> None:
        interpreter = Interpreter(ARITHMETIC)
        with pytest.raises(ValueError, match="malformed"):
            interpreter.evaluate((1, 2, 3))


class TestSafeEval:
    """The hardened arithmetic evaluator keeps its security-review contract."""

    def test_evaluates_arithmetic(self) -> None:
        assert safe_eval("2 * (3 + 4)") == 14.0

    def test_every_operator_is_pinned(self) -> None:
        # The operator table is a security surface: each entry asserted
        # individually so a mis-mapped operator cannot survive review.
        assert safe_eval("7 + 2") == 9.0
        assert safe_eval("7 - 2") == 5.0
        assert safe_eval("7 * 2") == 14.0
        assert safe_eval("7 / 2") == 3.5
        assert safe_eval("-7") == -7.0
        assert safe_eval("-(3 - 5)") == 2.0

    def test_division_by_zero_is_a_value_error(self) -> None:
        # The documented contract: every rejection is ValueError.
        with pytest.raises(ValueError, match="division by zero"):
            safe_eval("1/0")

    def test_the_exported_depth_constant_is_the_one_enforced(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        # One MAX_DEPTH knob for the whole unit — tightening the exported
        # constant must actually tighten this evaluator.
        from patterns.behavioral.interpreter.pattern import rules

        monkeypatch.setattr(rules, "MAX_DEPTH", 3)
        with pytest.raises(ValueError, match="too deeply nested"):
            safe_eval("1 + 1 + 1 + 1 + 1 + 1")
        assert safe_eval("1 + 1") == 2.0

    def test_rejects_imports_and_names(self) -> None:
        with pytest.raises(ValueError, match="disallowed"):
            safe_eval("__import__('os')")

    def test_rejects_bool_constants(self) -> None:
        with pytest.raises(ValueError, match="disallowed"):
            safe_eval("True + 1")

    def test_depth_limit_is_a_value_error_not_recursion(self) -> None:
        deep_formula = "1" + " + 1" * 60  # left-deep BinOp tree past MAX_DEPTH
        with pytest.raises(ValueError, match="too deeply nested"):
            safe_eval(deep_formula)
