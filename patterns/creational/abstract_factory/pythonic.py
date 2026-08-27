"""What to write instead: factories are callables, families are dataclasses.

``Decimal`` itself is already a factory -- pass it. When several builders
travel together, bundle them in a plain dataclass; swapping the family is
constructing a different bundle.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from decimal import Decimal


def parse_numbers(texts: list[str], build: Callable[[str], object] = float) -> list[object]:
    """A factory is just an argument with a sensible default."""
    return [build(t) for t in texts]


@dataclass(frozen=True)
class Family:
    """The 'complete' abstract factory: a bundle of callables."""

    number: Callable[[str], object]
    sequence: Callable[[list[object]], object]


PYTHON_FAMILY = Family(number=float, sequence=list)
EXACT_FAMILY = Family(number=Decimal, sequence=tuple)


def parse(texts: list[str], family: Family = PYTHON_FAMILY) -> object:
    return family.sequence([family.number(t) for t in texts])


def main() -> None:
    print(parse_numbers(["1.1"], Decimal))
    print(parse(["1.1", "2.2"], EXACT_FAMILY))


if __name__ == "__main__":
    main()
