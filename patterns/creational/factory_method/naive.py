"""The Gang of Four Factory Method, translated literally.

An abstract creator defers one construction decision to an abstract method;
each choice of helper costs a subclass.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class Shipment:
    def __init__(self, kind: str) -> None:
        self.kind = kind


class Express(Shipment):
    def __init__(self) -> None:
        super().__init__("express")


class Standard(Shipment):
    def __init__(self) -> None:
        super().__init__("standard")


class Store(ABC):
    """The creator: works with shipments, defers building them."""

    @abstractmethod
    def make_shipment(self) -> Shipment: ...

    def ship(self) -> str:
        return f"shipping via {self.make_shipment().kind}"


class ExpressStore(Store):
    def make_shipment(self) -> Shipment:
        return Express()


class StandardStore(Store):
    def make_shipment(self) -> Shipment:
        return Standard()


def main() -> None:
    print(ExpressStore().ship())
    print(StandardStore().ship())


if __name__ == "__main__":
    main()
