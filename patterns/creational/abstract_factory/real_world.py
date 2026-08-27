"""The stdlib's abstract factory: ``json.loads`` parse hooks.

The parser builds every float through the callable you hand it -- swap
``float`` for ``Decimal`` and the whole document changes family.
"""

from __future__ import annotations

import json
from decimal import Decimal


def load_exact(document: str) -> object:
    """Parse JSON with exact decimal arithmetic instead of binary floats."""
    return json.loads(document, parse_float=Decimal)


def main() -> None:
    doc = '{"price": 0.1, "qty": 3}'
    default = json.loads(doc)
    exact = load_exact(doc)
    assert isinstance(exact, dict) and isinstance(default, dict)
    print(f"float family:   {default['price']!r}")
    print(f"Decimal family: {exact['price']!r}")


if __name__ == "__main__":
    main()
