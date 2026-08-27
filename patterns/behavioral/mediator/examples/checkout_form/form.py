"""The mediator: a checkout form whose rules genuinely tangle.

Country restricts shipping methods; shipping gates payment options and
changes the total; submit enables only when the whole set is coherent.
Fields know none of it — every rule lives in ``recheck``, one readable
place, and a country change cascades through the dependent fields.
"""

from __future__ import annotations

from patterns.behavioral.mediator.examples.checkout_form.rules import (
    PAYMENTS_BY_SHIPPING,
    SHIPPING_BY_COUNTRY,
)
from patterns.behavioral.mediator.pattern import Form


class CheckoutForm(Form):
    """Every cross-field rule, in one place — the ``recheck`` the base calls."""

    def __init__(self, cart_cents: int) -> None:
        super().__init__()
        self.cart_cents = cart_cents
        self.shipping_options: tuple[str, ...] = ()
        self.payment_options: tuple[str, ...] = ()
        self.total_cents = 0
        self.submit_enabled = False
        self.country = self.add_field("country")
        self.shipping = self.add_field("shipping")
        self.payment = self.add_field("payment")
        self.recheck()

    def recheck(self) -> None:
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
