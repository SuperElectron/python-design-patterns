"""Singletons the interpreter already ships.

``None``, ``Ellipsis``, and ``NotImplemented`` each have exactly one instance,
which is why identity comparison (``is``) against them is the correct idiom.
And every module is a singleton: ``import`` consults ``sys.modules`` and
returns the cached object rather than building a new one.
"""

from __future__ import annotations

import sys
import types


def none_is_a_singleton() -> bool:
    """All ``None`` values in a program are the very same object."""
    a: object | None = None
    b: object | None = None
    # Every None in the process is literally the same object.
    return a is b and a is None


def modules_are_singletons() -> bool:
    """A second import returns the cached module object, not a copy."""
    first = __import__("json")
    second = __import__("json")
    return first is second and sys.modules["json"] is first


def main() -> None:
    print(f"None is a singleton:    {none_is_a_singleton()}")
    print(f"modules are singletons: {modules_are_singletons()}")
    print(f"a module's type:        {types.ModuleType.__name__}")


if __name__ == "__main__":
    main()
