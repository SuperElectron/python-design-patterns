"""Demo: the same checkout code through two mismatched vendor SDKs."""

from __future__ import annotations

from patterns.structural.adapter.examples.payment_gateways.adapters import (
    PaymentProcessor,
    PayPalAdapter,
    StripeAdapter,
)
from patterns.structural.adapter.examples.payment_gateways.checkout import checkout
from patterns.structural.adapter.examples.payment_gateways.vendors import (
    PayPalLikeGateway,
    StripeLikeClient,
)


def main() -> None:
    processors: dict[str, PaymentProcessor] = {
        "stripe-like": StripeAdapter(StripeLikeClient()),
        "paypal-like": PayPalAdapter(PayPalLikeGateway()),
    }
    for vendor, processor in processors.items():
        ok = checkout("A-1", 2_499, processor)
        declined = checkout("A-2", 999_999, processor)
        print(f"{vendor}: A-1 paid={ok.paid} ({ok.reference})")
        print(f"{vendor}: A-2 paid={declined.paid} ({declined.note})")


if __name__ == "__main__":
    main()
