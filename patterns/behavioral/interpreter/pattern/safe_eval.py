"""Interpreting with Python's own parser: a safe arithmetic evaluator.

The preferred alternative when the "little language" is arithmetic:
``ast.parse`` builds the tree and a restricted walk evaluates only the node
types we allow. User input never reaches eval(). Security-reviewed: rejects
bool constants (``True + 1``) and depth-limits nesting.
"""

from __future__ import annotations

import ast
import operator
from collections.abc import Callable

# The depth limit is the unit's ONE security knob: read from ``rules`` at
# call time so hardening the exported constant tightens this evaluator too.
from patterns.behavioral.interpreter.pattern import rules

_BINOPS: dict[type[ast.operator], Callable[[float, float], float]] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def safe_eval(formula: str) -> float:
    """Evaluate arithmetic like '2 * (3 + 4)'; anything else is ValueError.

    That includes division by zero: every rejection this evaluator makes is
    a ValueError, so callers wrap untrusted input in exactly one except.
    """
    try:
        return _walk(ast.parse(formula, mode="eval").body, depth=0)
    except ZeroDivisionError:
        raise ValueError("division by zero") from None


def _walk(node: ast.expr, depth: int) -> float:
    if depth > rules.MAX_DEPTH:
        raise ValueError("expression too deeply nested")
    if (
        isinstance(node, ast.Constant)
        and isinstance(node.value, int | float)
        and not isinstance(node.value, bool)
        # bool subclasses int, and a *safe* evaluator should not quietly
        # compute True + 1 -- so it is excluded explicitly.
    ):
        return float(node.value)
    if isinstance(node, ast.BinOp) and type(node.op) in _BINOPS:
        return _BINOPS[type(node.op)](_walk(node.left, depth + 1), _walk(node.right, depth + 1))
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return -_walk(node.operand, depth + 1)
    raise ValueError(f"disallowed syntax: {ast.dump(node)[:40]}")
