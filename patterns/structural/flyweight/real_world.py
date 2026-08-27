"""The interpreter's own flyweights.

CPython interns small integers and many strings; ``sys.intern`` requests
interning explicitly, turning string equality into pointer equality.
"""

from __future__ import annotations

import sys


def small_ints_are_interned() -> bool:
    """Integers in -5..256 are pre-built and shared."""
    a = 254 + 2
    b = 250 + 6
    return a is b


def interned_strings_share_identity() -> bool:
    # Build strings at runtime so the compiler can't fold them together.
    a = sys.intern("flyweight " + "pattern")
    b = sys.intern("flyweight" + " pattern")
    return a is b


def main() -> None:
    print(f"small ints interned:      {small_ints_are_interned()}")
    print(f"sys.intern shares:        {interned_strings_share_identity()}")


if __name__ == "__main__":
    main()
