"""The mediator: a checkout form whose rules genuinely tangle.

Country restricts shipping methods; shipping gates payment options and
changes the total; submit enables only when the whole set is coherent.
Fields know none of it — every rule lives in ``_recheck``, one readable
place, and a country change cascades through the dependent fields.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from patterns.behavioral.mediator.examples.checkout_form.rules import (
    PAYMENTS_BY_SHIPPING,
    SHIPPING_BY_COUNTRY,
)
from patterns.behavioral.mediator.pattern import Field


@dataclass
class CheckoutForm:
    """Every cross-field rule, in one place."""

    cart_cents: int
    country: Field = field(init=False)
    shipping: Field = field(init=False)
    payment: Field = field(init=False)
    shipping_options: tuple[str, ...] = ()
    payment_options: tuple[str, ...] = ()
    total_cents: int = 0
    submit_enabled: bool = False

    def __post_init__(self) -> None:
        self.country = Field(self._recheck)
        self.shipping = Field(self._recheck)
        self.payment = Field(self._recheck)
        self._recheck()

    def _recheck(self) -> None:
        lanes = SHIPPING_BY_COUNTRY.get(self.country.value, {})
        self.shipping_options = tuple(lanes)
        if self.shipping.value not in lanes:
            self.shipping.value = ""  # country change invalidated the lane
        self.payment_options = PAYMENTS_BY_SHIPPING.get(self.shipping.value, ())
        if self.payment.value not in self.payment_options:
            self.payment.value = ""
        self.total_cents = self.cart_cents + lanes.get(self.shipping.value, 0)
        self.submit_enabled = bool(
            self.country.value and self.shipping.value and self.payment.value
        )
