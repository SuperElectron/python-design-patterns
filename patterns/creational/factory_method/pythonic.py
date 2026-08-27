"""The guide's alternatives, best first.

1. Dependency Injection: if you can build the helper up front, pass it in.
2. Class attribute factory: creation stays internal, overriding is trivial.
3. Instance attribute factory: per-object override, no subclass at all.
"""

from __future__ import annotations

from collections.abc import Callable


class Shipment:
    def __init__(self, kind: str) -> None:
        self.kind = kind


def express() -> Shipment:
    return Shipment("express")


def standard() -> Shipment:
    return Shipment("standard")


class InjectedStore:
    """1. The dodge: don't defer creation -- receive the object."""

    def __init__(self, shipment: Shipment) -> None:
        self.shipment = shipment

    def ship(self) -> str:
        return f"shipping via {self.shipment.kind}"


class Store:
    """2. Class attribute factory: any callable; override by subclass or assignment."""

    shipment_factory: Callable[[], Shipment] = staticmethod(standard)

    def __init__(self, shipment_factory: Callable[[], Shipment] | None = None) -> None:
        # 3. Instance attribute overrides the class attribute per object.
        if shipment_factory is not None:
            self.shipment_factory = shipment_factory

    def ship(self) -> str:
        return f"shipping via {self.shipment_factory().kind}"


class ExpressStore(Store):
    shipment_factory = staticmethod(express)


def main() -> None:
    print(InjectedStore(express()).ship())
    print(Store().ship())
    print(ExpressStore().ship())
    print(Store(shipment_factory=express).ship())


if __name__ == "__main__":
    main()
