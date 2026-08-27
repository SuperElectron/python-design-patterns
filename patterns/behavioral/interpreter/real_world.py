"""Interpreting with Python's own parser: a safe arithmetic evaluator.

``ast.parse`` builds the tree; a restricted walk evaluates only the node
types we allow. User input never reaches eval().
"""

from __future__ import annotations

import ast
import operator
from collections.abc import Callable

_BINOPS: dict[type[ast.operator], Callable[[float, float], float]] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def safe_eval(formula: str) -> float:
    """Evaluate arithmetic like '2 * (3 + 4)'; reject everything else."""
    return _walk(ast.parse(formula, mode="eval").body)


def _walk(node: ast.expr) -> float:
    if isinstance(node, ast.Constant) and isinstance(node.value, int | float):
        return float(node.value)
    if isinstance(node, ast.BinOp) and type(node.op) in _BINOPS:
        return _BINOPS[type(node.op)](_walk(node.left), _walk(node.right))
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return -_walk(node.operand)
    raise ValueError(f"disallowed syntax: {ast.dump(node)[:40]}")


def main() -> None:
    print(safe_eval("2 * (3 + 4)"))
    try:
        safe_eval("__import__('os')")
    except ValueError as exc:
        print(f"rejected: {exc}")


if __name__ == "__main__":
    main()
