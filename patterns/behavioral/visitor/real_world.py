"""``ast.NodeVisitor``: the Visitor pattern as a stdlib API.

Count the function definitions and calls in any piece of Python source.
"""

from __future__ import annotations

import ast


class Census(ast.NodeVisitor):
    def __init__(self) -> None:
        self.functions: list[str] = []
        self.calls = 0

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self.functions.append(node.name)
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        self.calls += 1
        self.generic_visit(node)


def census_of(source: str) -> Census:
    census = Census()
    census.visit(ast.parse(source))
    return census


def main() -> None:
    source = "def greet():\n    print('hi')\n\ndef leave():\n    print(exit())\n"
    census = census_of(source)
    print(f"functions: {census.functions}, calls: {census.calls}")


if __name__ == "__main__":
    main()
