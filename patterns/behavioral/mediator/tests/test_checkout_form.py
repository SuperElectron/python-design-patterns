"""Behavioral tests for the checkout-form mini-project."""

from __future__ import annotations

from patterns.behavioral.mediator.examples.checkout_form import CheckoutForm


class TestCheckoutForm:
    def test_starts_incoherent_and_disabled(self) -> None:
        form = CheckoutForm(cart_cents=5000)
        assert form.shipping_options == ()
        assert form.payment_options == ()
        assert not form.submit_enabled

    def test_country_choice_reveals_its_lanes(self) -> None:
        form = CheckoutForm(cart_cents=5000)
        form.country.set("CA")
        assert list(form.shipping_options) == ["standard", "express"]
        form.country.set("DE")
        assert list(form.shipping_options) == ["standard"]

    def test_shipping_gates_payment_options(self) -> None:
        form = CheckoutForm(cart_cents=5000)
        form.country.set("CA")
        form.shipping.set("standard")
        assert list(form.payment_options) == ["card"]
        form.shipping.set("express")
        assert list(form.payment_options) == ["card", "cod"]

    def test_total_includes_the_chosen_lane(self) -> None:
        form = CheckoutForm(cart_cents=5000)
        form.country.set("US")
        form.shipping.set("express")
        assert form.total_cents == 5000 + 1900

    def test_full_selection_enables_submit(self) -> None:
        form = CheckoutForm(cart_cents=5000)
        form.country.set("CA")
        form.shipping.set("express")
        form.payment.set("cod")
        assert form.submit_enabled

    def test_country_change_cascades_and_resets_dependents(self) -> None:
        form = CheckoutForm(cart_cents=5000)
        form.country.set("CA")
        form.shipping.set("express")
        form.payment.set("cod")
        form.country.set("DE")  # DE has no express lane
        assert form.shipping.value == ""
        assert form.payment.value == ""
        assert not form.submit_enabled
        assert form.total_cents == 5000  # no lane selected, no shipping cost

    def test_recovery_after_cascade(self) -> None:
        form = CheckoutForm(cart_cents=5000)
        form.country.set("CA")
        form.shipping.set("express")
        form.payment.set("cod")
        form.country.set("DE")
        form.shipping.set("standard")
        form.payment.set("card")
        assert form.submit_enabled
        assert form.total_cents == 5000 + 1100
