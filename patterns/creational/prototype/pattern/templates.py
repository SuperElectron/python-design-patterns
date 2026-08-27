"""Prototype without ``clone()``: a registry of template callables.

The GoF pattern stores pre-configured *instances* and copies them on demand.
In Python the exemplar can simply be a callable that builds the product —
``functools.partial`` freezes the configuration — and per-request tweaks are
``dataclasses.replace`` on a frozen product. Same menu-of-templates shape, no
copy protocol.
"""

from __future__ import annotations

import dataclasses
from collections.abc import Callable
from typing import Generic, TypeVar, cast

T = TypeVar("T")

#: A template is any zero-argument callable producing one fresh product.
Template = Callable[[], T]


class TemplateRegistry(Generic[T]):
    """A menu of named templates; every ``create`` builds a fresh product."""

    def __init__(self) -> None:
        self._templates: dict[str, Template[T]] = {}

    def register(self, name: str, template: Template[T]) -> Template[T]:
        """Add a template under ``name``; returns it, so it can wrap a def."""
        self._templates[name] = template
        return template

    def names(self) -> list[str]:
        return sorted(self._templates)

    def create(self, name: str, **overrides: object) -> T:
        """Build a fresh product; overrides customize this one product only.

        Overrides use ``dataclasses.replace``, so they require the product to
        be a dataclass instance (frozen ones work — that is the point).
        """
        try:
            template = self._templates[name]
        except KeyError:
            raise ValueError(f"unknown template {name!r} (has: {self.names()})") from None
        product = template()
        if not overrides:
            return product
        if not dataclasses.is_dataclass(product) or isinstance(product, type):
            raise TypeError(f"overrides need a dataclass product, got {type(product).__name__}")
        return cast("T", dataclasses.replace(product, **overrides))
