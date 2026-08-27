"""Two fake vendor SDKs we must integrate but cannot edit.

Each has its own idea of amounts, currencies, and results — exactly the
mismatch the adapters in :mod:`adapters` reconcile.
"""

from __future__ import annotations


class StripeLikeClient:
    """Charges in integer cents; answers with a result dict."""

    def create_charge(self, amount_cents: int, currency: str) -> dict[str, str]:
        if amount_cents <= 0:
            return {"id": "", "status": "invalid_amount"}
        if amount_cents > 500_000:
            return {"id": "ch_declined", "status": "card_declined"}
        return {"id": f"ch_{amount_cents}", "status": "succeeded"}

    def diagnostics(self) -> str:
        """Vendor extra our checkout never calls — but support scripts do."""
        return "stripe-like: all systems normal"


class PayPalLikeGateway:
    """Charges via decimal strings; failure is an exception, not a status."""

    def submit_payment(self, amount: str, currency_code: str) -> str:
        value = float(amount)
        if value <= 0:
            raise ValueError("PAYPAL_INVALID_AMOUNT")
        if value > 5000.0:
            raise ValueError("PAYPAL_DECLINED")
        return f"PAYPAL-OK-{amount}-{currency_code}"
