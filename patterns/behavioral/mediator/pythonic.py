"""The mediator without a Colleague hierarchy.

A checkout form with enough interdependent rules to *justify* a mediator:
country restricts shipping methods, shipping method gates payment options
and recomputes the total, and submit is enabled only when the whole set is
coherent. Widgets know none of it -- every rule lives in one method.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field

SHIPPING_BY_COUNTRY = {
    "CA": {"standard": 900, "express": 2400},
    "US": {"standard": 700, "express": 1900},
    "DE": {"standard": 1100},  # no express lane
}
#: cash-on-delivery is only offered on express shipments
PAYMENTS_BY_SHIPPING: dict[str, tuple[str, ...]] = {
    "standard": ("card",),
    "express": ("card", "cod"),
}


@dataclass
class Field:
    """A dumb widget: holds a value, reports changes. No rules."""

    notify: Callable[[], None]
    value: str = ""

    def set(self, value: str) -> None:
        self.value = value
        self.notify()


@dataclass
class CheckoutForm:
    """The mediator: every cross-field rule, in one readable place."""

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


def main() -> None:
    form = CheckoutForm(cart_cents=5000)
    form.country.set("CA")
    form.shipping.set("express")
    form.payment.set("cod")
    print(f"total {form.total_cents}, submit={form.submit_enabled}")
    form.country.set("DE")  # express vanishes; dependent fields reset
    print(f"after DE: shipping={form.shipping.value!r}, submit={form.submit_enabled}")


if __name__ == "__main__":
    main()
