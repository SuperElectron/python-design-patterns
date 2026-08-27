"""What survives of the Builder in Python.

First: keyword arguments with defaults already solve the telescoping
constructor, so most "builders" should just be a call. Second: when assembly
really is staged, a small mutable builder in front of a frozen product keeps
the product immutable while giving callers a friendly surface.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Pizza:
    """The immutable product."""

    size: str
    toppings: tuple[str, ...] = ()


def order_pizza(size: str = "medium", *toppings: str) -> Pizza:
    """The kwargs 'builder': one readable call, no ceremony."""
    return Pizza(size=size, toppings=toppings)


@dataclass
class PizzaBuilder:
    """The staged builder: mutate freely, then emit the frozen product."""

    size: str = "medium"
    _toppings: list[str] = field(default_factory=list)

    def topped_with(self, *toppings: str) -> PizzaBuilder:
        self._toppings.extend(toppings)
        return self  # chainable

    def build(self) -> Pizza:
        return Pizza(size=self.size, toppings=tuple(self._toppings))


def main() -> None:
    print(order_pizza("large", "basil", "mozzarella"))
    print(PizzaBuilder(size="small").topped_with("olive").topped_with("caper").build())


if __name__ == "__main__":
    main()
