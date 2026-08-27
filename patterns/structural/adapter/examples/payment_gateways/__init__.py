"""Payment checkout over mismatched vendor SDKs, built on the Adapter.

Run it: ``uv run python -m patterns.structural.adapter.examples.payment_gateways``
"""

from patterns.structural.adapter.examples.payment_gateways.adapters import (
    PaymentProcessor,
    PaymentResult,
    PayPalAdapter,
    StripeAdapter,
)
from patterns.structural.adapter.examples.payment_gateways.checkout import Receipt, checkout
from patterns.structural.adapter.examples.payment_gateways.vendors import (
    PayPalLikeGateway,
    StripeLikeClient,
)

__all__ = [
    "PayPalAdapter",
    "PayPalLikeGateway",
    "PaymentProcessor",
    "PaymentResult",
    "Receipt",
    "StripeAdapter",
    "StripeLikeClient",
    "checkout",
]
