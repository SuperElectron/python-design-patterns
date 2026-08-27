"""The Prebound Method pattern as importable, typed building blocks.

The pattern itself is one line — ``name = _instance.method`` at module level —
so the library code here is the canonical minimal instance plus the one
verification helper worth sharing: ``shares_instance`` proves that a set of
module functions really are bound methods of a single hidden object (the
check ``random.random`` and ``random.seed`` would pass).
"""

from __future__ import annotations

from collections.abc import Callable


class Counter:
    """The canonical shape: an ordinary class, instantiable for isolation."""

    def __init__(self) -> None:
        self.count = 0

    def increment(self) -> int:
        self.count += 1
        return self.count

    def peek(self) -> int:
        return self.count


#: The pattern, applied to itself: one hidden instance built at import
#: (cheaply, no I/O), its bound methods published as module functions.
_instance = Counter()
increment = _instance.increment
peek = _instance.peek


def shares_instance(*functions: Callable[..., object]) -> bool:
    """True if every function is a bound method of one identical instance.

    The introspective proof of the pattern: ``shares_instance(random.random,
    random.seed)`` holds because both carry the same ``__self__``.
    """
    owners = [getattr(function, "__self__", None) for function in functions]
    return len(owners) > 0 and owners[0] is not None and all(o is owners[0] for o in owners)
