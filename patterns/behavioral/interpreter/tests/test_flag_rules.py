"""Behavioral tests for the flag-rules mini-project."""

from __future__ import annotations

import pytest

from patterns.behavioral.interpreter.examples.flag_rules import FlagEngine
from patterns.behavioral.interpreter.pattern import Expr, Value

FLAGS: dict[str, Expr] = {
    "new-dashboard": ("and", (">=", "age", 18), ("==", "country", "CA")),
    "beta-exports": ("or", ("==", "plan", "pro"), ("==", "role", "staff")),
    "legacy-ui": ("not", (">=", "signup_year", 2024)),
}


def _flag(rule: Expr, user: dict[str, Value]) -> bool:
    return FlagEngine({"probe": rule}).is_enabled("probe", user)


class TestComparisonOperators:
    """Every operator, at its boundary — off-by-one is this engine's real risk."""

    def test_ge_boundary(self) -> None:
        assert _flag((">=", "age", 18), {"age": 18})
        assert not _flag((">=", "age", 18), {"age": 17})

    def test_gt_boundary(self) -> None:
        assert not _flag((">", "age", 18), {"age": 18})
        assert _flag((">", "age", 18), {"age": 19})

    def test_le_boundary(self) -> None:
        assert _flag(("<=", "age", 18), {"age": 18})
        assert not _flag(("<=", "age", 18), {"age": 19})

    def test_lt_boundary(self) -> None:
        assert not _flag(("<", "age", 18), {"age": 18})
        assert _flag(("<", "age", 18), {"age": 17})

    def test_ne(self) -> None:
        assert _flag(("!=", "plan", "pro"), {"plan": "free"})
        assert not _flag(("!=", "plan", "pro"), {"plan": "pro"})

    def test_ordered_comparison_refuses_booleans(self) -> None:
        with pytest.raises(ValueError, match="ordered comparison on booleans"):
            _flag((">=", "flagged", 1), {"flagged": True})

    def test_ordered_comparison_refuses_non_numbers(self) -> None:
        with pytest.raises(ValueError, match="needs numbers"):
            _flag((">=", "plan", 18), {"plan": "pro"})


class TestFlagEngine:
    def test_conjunction_requires_both_sides(self) -> None:
        engine = FlagEngine(FLAGS)
        adult_canadian: dict[str, Value] = {"age": 31, "country": "CA"}
        minor_canadian: dict[str, Value] = {"age": 17, "country": "CA"}
        adult_american: dict[str, Value] = {"age": 31, "country": "US"}
        assert engine.is_enabled("new-dashboard", adult_canadian)
        assert not engine.is_enabled("new-dashboard", minor_canadian)
        assert not engine.is_enabled("new-dashboard", adult_american)

    def test_disjunction_takes_either_side(self) -> None:
        engine = FlagEngine(FLAGS)
        assert engine.is_enabled("beta-exports", {"plan": "pro", "role": "user"})
        assert engine.is_enabled("beta-exports", {"plan": "free", "role": "staff"})
        assert not engine.is_enabled("beta-exports", {"plan": "free", "role": "user"})

    def test_negation(self) -> None:
        engine = FlagEngine(FLAGS)
        assert engine.is_enabled("legacy-ui", {"signup_year": 2021})
        assert not engine.is_enabled("legacy-ui", {"signup_year": 2025})

    def test_string_leaf_is_field_when_context_has_it_else_literal(self) -> None:
        engine = FlagEngine({"self-country": ("==", "country", "country")})
        # Both leaves resolve to the user's country -> always equal.
        assert engine.is_enabled("self-country", {"country": "CA"})
        engine2 = FlagEngine({"is-ca": ("==", "country", "CA")})
        # "CA" is not a context field, so it stays a literal.
        assert engine2.is_enabled("is-ca", {"country": "CA"})
        assert not engine2.is_enabled("is-ca", {"country": "US"})

    def test_unknown_flag_names_the_known_ones(self) -> None:
        engine = FlagEngine(FLAGS)
        with pytest.raises(KeyError, match="beta-exports"):
            engine.is_enabled("nope", {})

    def test_hostile_rule_depth_is_rejected(self) -> None:
        bomb: Expr = ("==", "x", 1)
        for _ in range(200):
            bomb = ("and", bomb, True)
        engine = FlagEngine({"bomb": bomb})
        with pytest.raises(ValueError, match="too deeply nested"):
            engine.is_enabled("bomb", {"x": 1})

    def test_rollout_reports_every_flag(self) -> None:
        engine = FlagEngine(FLAGS)
        user: dict[str, Value] = {
            "age": 31,
            "country": "CA",
            "plan": "pro",
            "role": "user",
            "signup_year": 2021,
        }
        assert engine.rollout(user) == {
            "beta-exports": True,
            "legacy-ui": True,
            "new-dashboard": True,
        }
