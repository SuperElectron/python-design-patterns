"""The client code: written once against the target, never per vendor."""

from __future__ import annotations

from dataclasses import dataclass

from patterns.structural.adapter.examples.payment_gateways.adapters import PaymentProcessor


@dataclass(frozen=True)
class Receipt:
    order_id: str
    paid: bool
    reference: str
    note: str = ""


def checkout(order_id: str, total_cents: int, processor: PaymentProcessor) -> Receipt:
    """Charge an order through whichever vendor the adapter hides."""
    result = processor.charge(total_cents, "usd")
    if result.ok:
        return Receipt(order_id, paid=True, reference=result.reference)
    return Receipt(order_id, paid=False, reference=result.reference, note=result.reason)
