"""A checkout form built on the Mediator pattern.

Run it: ``uv run python -m patterns.behavioral.mediator.examples.checkout_form``
"""

from patterns.behavioral.mediator.examples.checkout_form.form import CheckoutForm
from patterns.behavioral.mediator.examples.checkout_form.rules import (
    PAYMENTS_BY_SHIPPING,
    SHIPPING_BY_COUNTRY,
)

__all__ = ["PAYMENTS_BY_SHIPPING", "SHIPPING_BY_COUNTRY", "CheckoutForm"]
