"""``codecs``: the stdlib's plugin registry in daily use.

Every str.encode(name) is a registry lookup; codecs.register() adds a
search function that can serve entirely new names.
"""

from __future__ import annotations

import codecs


def rot13(text: str) -> str:
    """'rot13' resolves through the codec registry."""
    return codecs.encode(text, "rot13")


def lookup_is_the_registry(name: str) -> str:
    """Ask the registry directly for a codec entry."""
    return codecs.lookup(name).name


def main() -> None:
    print(rot13("gura fur fnvq"))
    print(f"'UTF8' resolves to: {lookup_is_the_registry('UTF8')}")


if __name__ == "__main__":
    main()
