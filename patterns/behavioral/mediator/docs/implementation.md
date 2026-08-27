# Mediator — putting it into a system

## The smell it fixes

Widgets (or services) updating each other directly: the country dropdown
pokes the shipping selector, which pokes payment, which pokes the total —
and adding one field means auditing every other field's handlers.

## Steps

1. **Inventory the cross-component rules** — write each as a sentence
   ("cash-on-delivery is only offered on express"). These sentences become
   one method's body, so their number tells you the mediator's size.
2. **Dumb the components down** to value + change notification.
   [`Field`](../pattern/form.py) is that reduced form; subclass
   [`Form`](../pattern/form.py) and create each one with `add_field`, so
   every change notifies the one mediator.
3. **Write one `recheck` that re-derives everything** from current values:
   recompute options, reset invalidated selections, update totals, gate
   submission. Deriving the *whole* state each time is what makes cascades
   (country → shipping → payment) fall out for free.
4. **Keep the rules as data where they are data.** Tables like
   `SHIPPING_BY_COUNTRY` stay dicts the mediator consults — don't encode
   them as conditionals.
5. **Test the mediator headlessly.** The rules never needed a UI: set
   values, assert derived state — including the cascade paths.

```python
form = CheckoutForm(cart_cents=5000)
form.country.set("CA")
form.shipping.set("express")
assert form.payment_options == ("card", "cod")
```

## Python idioms that keep it small

- The notify wire is **just a bound method** (`add_field` wires each
  `Field` to `self.recheck`) — no observer framework, no signals library.
- Recompute-everything beats surgical updates until profiling says
  otherwise: correctness first, the rules stay declarative.
- Components that are values-with-validation can be **dataclasses**; the
  mediator subclass composes its fields in `__init__` via `add_field` and
  ends with one initial `recheck()` so derived state starts coherent.

## Pitfalls

- **God-object drift** — the mediator's budget is *interaction* rules; the
  moment domain logic (pricing, tax) moves in, split it: mediator
  coordinates, domain objects compute.
- **Notification loops.** `recheck` writing `field.value` directly (not via
  `set`) is deliberate here — calling `set` from inside the mediator would
  re-enter it. Keep one direction: components notify in, mediator writes out.
- **Hidden ordering dependencies** between rules in `recheck` — derive
  facts in dependency order (options before validity before gating) and
  test the cascade explicitly.
- **A queue would do.** If your "rules" are only "pass work along",
  `queue.Queue` is the whole mediator.

## Worked example

[`examples/checkout_form/`](../examples/checkout_form/) applies every step —
country/shipping/payment with cascading resets and submit gating:

```bash
uv run python -m patterns.behavioral.mediator.examples.checkout_form.main
```
