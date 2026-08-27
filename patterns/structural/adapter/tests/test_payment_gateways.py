"""Behavioral tests for the payment-gateways mini-project.

The point under test: checkout is written once against ``PaymentProcessor``
and every vendor behaves identically from its seat — including failures.
"""

from __future__ import annotations

from collections.abc import Callable

import pytest

from patterns.structural.adapter.examples.payment_gateways import (
    PaymentProcessor,
    PayPalAdapter,
    PayPalLikeGateway,
    StripeAdapter,
    StripeLikeClient,
    checkout,
)
from patterns.structural.adapter.examples.payment_gateways.__main__ import main


def stripe() -> PaymentProcessor:
    return StripeAdapter(StripeLikeClient())


def paypal() -> PaymentProcessor:
    return PayPalAdapter(PayPalLikeGateway())


@pytest.mark.parametrize("make_processor", [stripe, paypal], ids=["stripe-like", "paypal-like"])
class TestAnyVendor:
    """One suite, every adapter: the client contract is vendor-independent.

    Adapters are built inside each test — construction at collection time
    would share instances across the class and break if a vendor gains state.
    """

    def test_a_normal_charge_pays_the_order(
        self, make_processor: Callable[[], PaymentProcessor]
    ) -> None:
        receipt = checkout("A-1", 2_499, make_processor())
        assert receipt.paid
        assert receipt.reference != ""

    def test_a_huge_charge_is_declined_not_raised(
        self, make_processor: Callable[[], PaymentProcessor]
    ) -> None:
        receipt = checkout("A-2", 999_999, make_processor())
        assert not receipt.paid
        assert receipt.note != ""

    def test_a_zero_charge_is_refused(self, make_processor: Callable[[], PaymentProcessor]) -> None:
        assert not checkout("A-3", 0, make_processor()).paid


class TestTranslationDetails:
    def test_paypal_amounts_become_decimal_strings(self) -> None:
        gateway = PayPalLikeGateway()
        result = PayPalAdapter(gateway).charge(2_499, "usd")
        assert result.reference == "PAYPAL-OK-24.99-USD"

    def test_paypal_exceptions_become_results(self) -> None:
        result = PayPalAdapter(PayPalLikeGateway()).charge(999_999, "usd")
        assert not result.ok
        assert "DECLINED" in result.reason

    def test_stripe_currency_is_normalized_to_lowercase(self) -> None:
        seen: list[str] = []

        class RecordingStripe(StripeLikeClient):
            def create_charge(self, amount_cents: int, currency: str) -> dict[str, str]:
                seen.append(currency)
                return super().create_charge(amount_cents, currency)

        StripeAdapter(RecordingStripe()).charge(2_499, "USD")
        assert seen == ["usd"]

    def test_stripe_extras_stay_reachable_through_forwarding(self) -> None:
        adapter = StripeAdapter(StripeLikeClient())
        assert "all systems normal" in adapter.diagnostics()


class TestDemo:
    def test_main_charges_both_vendors(self, capsys: pytest.CaptureFixture[str]) -> None:
        main()
        out = capsys.readouterr().out
        assert "stripe-like: A-1 paid=True" in out
        assert "paypal-like: A-1 paid=True" in out
        assert "paid=False" in out
