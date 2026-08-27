"""Demo: a scripted checkout interaction, including the cascade."""

from __future__ import annotations

from patterns.behavioral.mediator.examples.checkout_form.form import CheckoutForm


def main() -> None:
    form = CheckoutForm(cart_cents=5000)
    print(f"start: options={form.shipping_options}, submit={form.submit_enabled}")

    form.country.set("CA")
    form.shipping.set("express")
    form.payment.set("cod")
    print(f"CA/express/cod: total={form.total_cents}, submit={form.submit_enabled}")

    form.country.set("DE")  # express vanishes; dependent fields reset
    print(
        f"switch to DE: shipping={form.shipping.value!r}, "
        f"payment={form.payment.value!r}, submit={form.submit_enabled}"
    )

    form.shipping.set("standard")
    form.payment.set("card")
    print(f"DE/standard/card: total={form.total_cents}, submit={form.submit_enabled}")


if __name__ == "__main__":
    main()
