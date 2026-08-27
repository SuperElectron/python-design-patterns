"""Domain types for the report-pipeline mini-project."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Sale:
    product: str
    quantity: int
    unit_price: float
    refunded: bool = False

    def revenue(self) -> float:
        return self.quantity * self.unit_price


Sales = tuple[Sale, ...]
