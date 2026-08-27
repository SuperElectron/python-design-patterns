"""Behavioral tests for all three mediator variants."""

from patterns.behavioral.mediator import naive, pythonic, real_world


class TestNaive:
    def test_rules_live_in_the_mediator(self) -> None:
        dialog = naive.SignupDialog()
        dialog.username.type_text("ada")
        assert not dialog.submit.enabled
        dialog.password.type_text("correcthorse")
        assert dialog.submit.enabled

    def test_weak_password_keeps_submit_disabled(self) -> None:
        dialog = naive.SignupDialog()
        dialog.username.type_text("ada")
        dialog.password.type_text("short")
        assert not dialog.submit.enabled


class TestPythonic:
    def test_happy_path_enables_submit_and_totals(self) -> None:
        form = pythonic.CheckoutForm(cart_cents=5000)
        form.country.set("CA")
        form.shipping.set("express")
        form.payment.set("cod")
        assert form.submit_enabled
        assert form.total_cents == 5000 + 2400

    def test_country_change_cascades_through_dependent_fields(self) -> None:
        form = pythonic.CheckoutForm(cart_cents=5000)
        form.country.set("US")
        form.shipping.set("express")
        form.payment.set("cod")
        form.country.set("DE")  # DE has no express -> shipping and payment reset
        assert form.shipping.value == "" and form.payment.value == ""
        assert not form.submit_enabled
        assert form.shipping_options == ("standard",)

    def test_payment_options_follow_shipping_method(self) -> None:
        form = pythonic.CheckoutForm(cart_cents=1000)
        form.country.set("CA")
        form.shipping.set("standard")
        standard_options: tuple[str, ...] = form.payment_options
        assert standard_options == ("card",)
        form.shipping.set("express")
        express_options: tuple[str, ...] = form.payment_options
        assert express_options == ("card", "cod")

    def test_widgets_hold_no_rules(self) -> None:
        pings: list[str] = []
        widget = pythonic.Field(notify=lambda: pings.append("changed"))
        widget.set("anything")
        assert pings == ["changed"]  # reusable with any coordinator


class TestRealWorld:
    def test_queue_mediates_producer_and_consumer(self) -> None:
        assert real_world.pipeline(["a", "b", "c"]) == ["A", "B", "C"]

    def test_empty_stream(self) -> None:
        assert real_world.pipeline([]) == []
