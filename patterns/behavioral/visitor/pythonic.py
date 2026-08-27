"""The visitor with the plumbing deleted: functools.singledispatch.

Node classes are plain dataclasses with no accept(); each operation is a
dispatch family of small functions.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import singledispatch


@dataclass(frozen=True)
class Number:
    value: int


@dataclass(frozen=True)
class Add:
    left: Number | Add
    right: Number | Add


@singledispatch
def render(node: object) -> str:
    raise TypeError(f"no renderer for {type(node).__name__}")


@render.register
def _(node: Number) -> str:
    return str(node.value)


@render.register
def _(node: Add) -> str:
    return f"({render(node.left)} + {render(node.right)})"


@singledispatch
def evaluate(node: object) -> int:
    raise TypeError(f"no evaluator for {type(node).__name__}")


@evaluate.register
def _(node: Number) -> int:
    return node.value


@evaluate.register
def _(node: Add) -> int:
    return evaluate(node.left) + evaluate(node.right)


def main() -> None:
    tree = Add(Number(1), Add(Number(2), Number(3)))
    print(f"{render(tree)} = {evaluate(tree)}")


if __name__ == "__main__":
    main()
