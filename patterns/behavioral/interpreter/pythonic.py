"""The same grammar as data: nested tuples, one recursive evaluator.

Extending the language is a dict entry, not a class.
"""

from __future__ import annotations

import operator
from collections.abc import Callable

Expr = int | tuple[str, "Expr", "Expr"]

OPS: dict[str, Callable[[int, int], int]] = {
    "+": operator.add,
    "*": operator.mul,
    "-": operator.sub,
}


def interpret(expr: Expr) -> int:
    if isinstance(expr, int):
        return expr
    op, left, right = expr
    return OPS[op](interpret(left), interpret(right))


def main() -> None:
    tree: Expr = ("*", ("+", 2, 3), 4)
    print(interpret(tree))


if __name__ == "__main__":
    main()
