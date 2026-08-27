"""``random``: the stdlib's flagship prebound methods.

``random.random`` and ``random.seed`` are bound methods of one hidden
``Random`` instance built when the module is imported.
"""

from __future__ import annotations

import random


def module_functions_share_one_instance() -> bool:
    """Both prebound methods carry the same __self__."""
    a = getattr(random.random, "__self__", None)
    b = getattr(random.seed, "__self__", None)
    return a is not None and a is b and isinstance(a, random.Random)


def seeded_sequence(seed: int, n: int) -> list[float]:
    """Seeding through one prebound method changes what the other returns."""
    random.seed(seed)
    return [random.random() for _ in range(n)]


def main() -> None:
    print(f"one hidden instance: {module_functions_share_one_instance()}")
    print(f"reproducible: {seeded_sequence(42, 2) == seeded_sequence(42, 2)}")


if __name__ == "__main__":
    main()
