"""Feature-flag rules stored as data, evaluated per user.

A rule is a sentence in a tiny boolean language::

    ("and", (">=", "age", 18), ("==", "country", "CA"))

Rules live in config (they're just tuples — JSON-serializable shapes), and
extending the language is one entry in ``OPERATIONS``. Leaves that name a
context field resolve to the user's value; anything else is a literal.
"""

from __future__ import annotations

from collections.abc import Mapping

from patterns.behavioral.interpreter.pattern import Expr, Interpreter, Operation, Value


def _cmp(pair: tuple[Value, ...]) -> tuple[float, float]:
    left, right = pair
    if isinstance(left, bool) or isinstance(right, bool):
        raise ValueError("ordered comparison on booleans")
    if not isinstance(left, int | float) or not isinstance(right, int | float):
        raise ValueError(f"ordered comparison needs numbers, got {pair!r}")
    return float(left), float(right)


def _all(args: tuple[Value, ...]) -> Value:
    return all(bool(a) for a in args)


def _any(args: tuple[Value, ...]) -> Value:
    return any(bool(a) for a in args)


def _not(args: tuple[Value, ...]) -> Value:
    (only,) = args
    return not bool(only)


OPERATIONS: dict[str, Operation] = {
    "and": _all,
    "or": _any,
    "not": _not,
    "==": lambda a: a[0] == a[1],
    "!=": lambda a: a[0] != a[1],
    ">=": lambda a: _cmp(a)[0] >= _cmp(a)[1],
    "<=": lambda a: _cmp(a)[0] <= _cmp(a)[1],
    ">": lambda a: _cmp(a)[0] > _cmp(a)[1],
    "<": lambda a: _cmp(a)[0] < _cmp(a)[1],
}


class FlagEngine:
    """Evaluate named feature flags against a user context."""

    def __init__(self, flags: Mapping[str, Expr]) -> None:
        self._flags = dict(flags)

    def is_enabled(self, flag: str, user: Mapping[str, Value]) -> bool:
        """True if ``flag``'s rule accepts this user; KeyError on unknown flag."""
        if flag not in self._flags:
            raise KeyError(f"unknown flag {flag!r} (has: {sorted(self._flags)})")

        def resolve(leaf: Value) -> Value:
            # A string leaf names a context field when the user has one;
            # otherwise it is a literal ("CA" in a country comparison).
            if isinstance(leaf, str) and leaf in user:
                return user[leaf]
            return leaf

        interpreter = Interpreter(OPERATIONS, resolve=resolve)
        return bool(interpreter.evaluate(self._flags[flag]))

    def rollout(self, user: Mapping[str, Value]) -> dict[str, bool]:
        """Every flag's verdict for one user."""
        return {flag: self.is_enabled(flag, user) for flag in sorted(self._flags)}
