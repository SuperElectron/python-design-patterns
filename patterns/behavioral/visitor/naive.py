"""The Gang of Four Visitor: accept() on every node, visit_X on every visitor."""

from __future__ import annotations

from abc import ABC, abstractmethod


class Node(ABC):
    @abstractmethod
    def accept(self, visitor: Visitor) -> str: ...


class Number(Node):
    def __init__(self, value: int) -> None:
        self.value = value

    def accept(self, visitor: Visitor) -> str:
        return visitor.visit_number(self)


class Add(Node):
    def __init__(self, left: Node, right: Node) -> None:
        self.left, self.right = left, right

    def accept(self, visitor: Visitor) -> str:
        return visitor.visit_add(self)


class Visitor(ABC):
    @abstractmethod
    def visit_number(self, node: Number) -> str: ...

    @abstractmethod
    def visit_add(self, node: Add) -> str: ...


class Renderer(Visitor):
    def visit_number(self, node: Number) -> str:
        return str(node.value)

    def visit_add(self, node: Add) -> str:
        return f"({node.left.accept(self)} + {node.right.accept(self)})"


def main() -> None:
    tree = Add(Number(1), Add(Number(2), Number(3)))
    print(tree.accept(Renderer()))


if __name__ == "__main__":
    main()
