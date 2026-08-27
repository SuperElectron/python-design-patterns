"""One ``PaymentProcessor`` target; one adapter per vendor shape.

The target interface is defined by what *checkout* needs — not by either
vendor. Each adapter translates amounts, currencies, and (crucially) the
vendors' different failure conventions into one ``PaymentResult``.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from patterns.structural.adapter.examples.payment_gateways.vendors import (
    PayPalLikeGateway,
    StripeLikeClient,
)
from patterns.structural.adapter.pattern import DelegatingAdapter


@dataclass(frozen=True)
class PaymentResult:
    """The one result shape checkout understands."""

    ok: bool
    reference: str
    reason: str = ""


class PaymentProcessor(Protocol):
    """The target interface — everything checkout will ever call."""

    def charge(self, amount_cents: int, currency: str) -> PaymentResult: ...


class StripeAdapter(DelegatingAdapter[StripeLikeClient]):
    """Translate ``charge``; the vendor's extras still reachable by forwarding."""

    def charge(self, amount_cents: int, currency: str) -> PaymentResult:
        outcome = self.adaptee.create_charge(amount_cents, currency.lower())
        if outcome["status"] == "succeeded":
            return PaymentResult(ok=True, reference=outcome["id"])
        return PaymentResult(ok=False, reference=outcome["id"], reason=outcome["status"])


class PayPalAdapter:
    """A hand-rolled adapter: cents -> decimal string, exception -> result."""

    def __init__(self, gateway: PayPalLikeGateway) -> None:
        self._gateway = gateway

    def charge(self, amount_cents: int, currency: str) -> PaymentResult:
        amount = f"{amount_cents / 100:.2f}"
        try:
            confirmation = self._gateway.submit_payment(amount, currency.upper())
        except ValueError as refusal:
            return PaymentResult(ok=False, reference="", reason=str(refusal))
        return PaymentResult(ok=True, reference=confirmation)
