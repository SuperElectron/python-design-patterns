"""The Gang of Four Interpreter: one class per grammar rule."""

from __future__ import annotations

from abc import ABC, abstractmethod


class Expression(ABC):
    @abstractmethod
    def interpret(self) -> int: ...


class Number(Expression):
    def __init__(self, value: int) -> None:
        self.value = value

    def interpret(self) -> int:
        return self.value


class Add(Expression):
    def __init__(self, left: Expression, right: Expression) -> None:
        self.left, self.right = left, right

    def interpret(self) -> int:
        return self.left.interpret() + self.right.interpret()


class Mul(Expression):
    def __init__(self, left: Expression, right: Expression) -> None:
        self.left, self.right = left, right

    def interpret(self) -> int:
        return self.left.interpret() * self.right.interpret()


def main() -> None:
    # (2 + 3) * 4
    tree = Mul(Add(Number(2), Number(3)), Number(4))
    print(tree.interpret())


if __name__ == "__main__":
    main()
