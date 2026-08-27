"""Grammar-as-data: nested tuples, one recursive evaluator.

The tree needs no class per rule. A sentence is a value or a tuple whose
head names an operation: ``("*", ("+", 2, 3), 4)``. Extending the language
is a dict entry, not a class — and the evaluator is depth-capped so a
hostile, deeply nested input fails with ``ValueError`` instead of blowing
the recursion limit.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping

#: Deeper than any human-written sentence; shallower than the recursion
#: limit, so hostile nesting gets a clean ValueError, not a RecursionError.
MAX_DEPTH = 50

Value = int | float | str | bool
Expr = Value | tuple[object, ...]

#: An operation receives its already-evaluated operands.
Operation = Callable[[tuple[Value, ...]], Value]

#: Resolves a leaf — the hook where "age" becomes the user's age. Default:
#: leaves are literals.
Resolver = Callable[[Value], Value]


class Interpreter:
    """Evaluate tuple-tree sentences against an operation table."""

    def __init__(
        self,
        operations: Mapping[str, Operation],
        *,
        resolve: Resolver | None = None,
        max_depth: int = MAX_DEPTH,
    ) -> None:
        self._operations = dict(operations)
        self._resolve: Resolver = resolve if resolve is not None else lambda leaf: leaf
        self._max_depth = max_depth

    def evaluate(self, expr: Expr) -> Value:
        """Interpret one sentence; reject unknown operations and deep nesting."""
        return self._walk(expr, depth=0)

    def _walk(self, expr: Expr, depth: int) -> Value:
        if depth > self._max_depth:
            raise ValueError("expression too deeply nested")
        if not isinstance(expr, tuple):
            return self._resolve(expr)
        if not expr or not isinstance(expr[0], str):
            raise ValueError(f"malformed expression: {expr!r}")
        head = expr[0]
        if head not in self._operations:
            raise ValueError(f"unknown operation: {head!r}")
        operands = tuple(self._walk(_as_expr(arg), depth + 1) for arg in expr[1:])
        return self._operations[head](operands)


def _as_expr(node: object) -> Expr:
    """Narrow a tuple element back to Expr, rejecting foreign objects."""
    if isinstance(node, int | float | str | bool | tuple):
        return node
    raise ValueError(f"unsupported node: {node!r}")
