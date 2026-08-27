"""The business tables the checkout mediator coordinates over."""

from __future__ import annotations

SHIPPING_BY_COUNTRY: dict[str, dict[str, int]] = {
    "CA": {"standard": 900, "express": 2400},
    "US": {"standard": 700, "express": 1900},
    "DE": {"standard": 1100},  # no express lane
}

#: cash-on-delivery is only offered on express shipments
PAYMENTS_BY_SHIPPING: dict[str, tuple[str, ...]] = {
    "standard": ("card",),
    "express": ("card", "cod"),
}
