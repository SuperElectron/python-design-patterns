"""Factory Method and its Python dodges, importable as library code.

The guide's ranking, best first: (1) dependency injection — if you can build
the helper up front, pass the object; (2) a class-attribute factory —
creation stays inside the class, but overriding is assignment or a one-line
subclass, and *any* callable is accepted; (3) an instance-attribute factory
for per-object overrides with no subclass at all.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")

#: A factory is nothing special: any zero-argument callable that builds one T.
Factory = Callable[[], T]


class Shipment:
    def __init__(self, kind: str) -> None:
        self.kind = kind


def express() -> Shipment:
    return Shipment("express")


def standard() -> Shipment:
    return Shipment("standard")


class InjectedStore:
    """1. The dodge: don't defer creation — receive the object."""

    def __init__(self, shipment: Shipment) -> None:
        self.shipment = shipment

    def ship(self) -> str:
        return f"shipping via {self.shipment.kind}"


class Store:
    """2. Class-attribute factory: any callable; override by subclass or assignment."""

    shipment_factory: Factory[Shipment] = staticmethod(standard)

    def __init__(self, shipment_factory: Factory[Shipment] | None = None) -> None:
        # 3. Instance attribute overrides the class attribute per object.
        if shipment_factory is not None:
            self.shipment_factory = shipment_factory

    def ship(self) -> str:
        return f"shipping via {self.shipment_factory().kind}"


class ExpressStore(Store):
    shipment_factory = staticmethod(express)
