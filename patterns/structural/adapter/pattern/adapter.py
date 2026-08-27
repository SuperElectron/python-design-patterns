"""Adapter as an importable, typed building block.

An adapter translates the calls your code makes into the calls a class you
cannot edit understands. Python needs less machinery than the classic form:
a one-method mismatch is just a function, and for wider surfaces
``DelegatingAdapter`` translates what differs and forwards the rest.
"""

from __future__ import annotations

from typing import Any, Generic, TypeVar

Adaptee = TypeVar("Adaptee")


class DelegatingAdapter(Generic[Adaptee]):
    """Translate the methods that differ; forward everything else.

    Subclass it, store nothing yourself, and define only the target-interface
    methods your callers actually use. Attributes you don't define fall
    through to the adaptee via ``__getattr__`` — the adapter never has to
    re-list a surface it isn't changing.
    """

    def __init__(self, adaptee: Adaptee) -> None:
        self._adaptee = adaptee

    @property
    def adaptee(self) -> Adaptee:
        """The wrapped object, for callers that need to reach past the adapter."""
        return self._adaptee

    def __getattr__(self, name: str) -> Any:
        # Only called for names not found on the adapter itself, so a
        # translated method always wins over the adaptee's original.
        return getattr(self._adaptee, name)
