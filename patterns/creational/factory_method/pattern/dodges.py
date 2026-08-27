"""Factory Method and its Python dodges, importable as library code.

The guide's ranking, best first: (1) dependency injection — if you can build
the helper up front, pass the object; (2) a class-attribute factory slot —
creation stays inside the class, overridden by a subclass or assignment;
(3) an instance-attribute factory for per-object overrides with no subclass.

The one trap (see docs/implementation.md): a plain function assigned in a
class body becomes a method and binds ``self``, so calling the slot raises
``TypeError``. Classes are safe (they are not descriptors); for any other
callable, wrap it with ``factory_slot``.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import ParamSpec, TypeVar

T = TypeVar("T")
P = ParamSpec("P")

#: A type alias (not one of the dodges): any zero-argument callable
#: building one T. Handy for annotating injected or slotted factories.
Factory = Callable[[], T]


def factory_slot(factory: Callable[P, T]) -> staticmethod[P, T]:
    """Wrap any callable for safe assignment as a class-attribute factory.

    Class-body assignment of a plain function turns it into a method — the
    call then receives ``self`` as an unwanted first argument.  Wrapping in
    ``staticmethod`` keeps the callable's own signature, whatever it is:

    >>> class Client:
    ...     make_response = factory_slot(lambda raw: raw.upper())
    """
    return staticmethod(factory)
