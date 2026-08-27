"""The Sentinel Object pattern as importable, typed building blocks.

``Sentinel`` is a named, unforgeable marker (a PEP 661-inspired shape;
unlike the PEP's proposal, two same-named sentinels here are deliberately
distinct objects — tested). ``MISSING`` is the one most APIs need. A
sentinel's identity is its meaning: compare with ``is``, never ``==``.
"""

from __future__ import annotations


class Sentinel:
    """A unique marker object with a readable repr.

    >>> MISSING = Sentinel("MISSING")
    >>> value is MISSING          # identity is the only correct check
    """

    __slots__ = ("_name",)

    def __init__(self, name: str) -> None:
        self._name = name

    def __repr__(self) -> str:
        return f"<{self._name}>"


#: The workhorse: "no value here", even where None is a legitimate value.
MISSING = Sentinel("MISSING")
