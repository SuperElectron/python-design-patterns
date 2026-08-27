# Adapter — putting it into a system

## The smell it fixes

Vendor-specific shapes leaking through code that shouldn't care:

```python
def checkout(order, vendor, client):
    if vendor == "stripe":
        outcome = client.create_charge(order.total_cents, "usd")
        paid = outcome["status"] == "succeeded"
    elif vendor == "paypal":
        try:
            ref = client.submit_payment(f"{order.total_cents / 100:.2f}", "USD")
            paid = True
        except ValueError:
            paid = False
    ...
```

Every vendor difference — units, naming, error convention — is re-decided at
every call site. The adapter moves each vendor's translation into one class,
and the call sites shrink to a single target interface.

## Steps

1. **Define the target from the client's needs.** List the calls the client
   actually makes; type them as a `Protocol`. Do not copy either vendor's
   surface — the target belongs to *your* domain.
2. **Write one adapter per adaptee.** Translate units and argument shapes,
   and — the step most often missed — translate **failure conventions**
   (status dict vs exception) into one result type.
3. **Pick the adapter's size.** One method → a plain function or tiny class.
   A few methods over a wide surface → subclass
   `DelegatingAdapter` and define only what differs; the rest forwards.
4. **Construct at the edge.** Adapters are wired where the app is assembled
   (config, DI, factory) — client modules import the target type only.
5. **Test through the target.** One test suite, parameterized over every
   adapter, pins that all vendors behave identically from the client's seat.

```python
from patterns.structural.adapter.pattern import DelegatingAdapter


class StripeAdapter(DelegatingAdapter[StripeLikeClient]):
    def charge(self, amount_cents: int, currency: str) -> PaymentResult:
        outcome = self.adaptee.create_charge(amount_cents, currency.lower())
        ...
```

## Python idioms that keep it small

- **`Protocol` for the target** — the client gets type-checked without any
  runtime base class, and adapters satisfy it structurally.
- **A closure as the whole adapter** when the target is one callable:
  `lambda: (sensor.get_fahrenheit() - 32) * 5 / 9`.
- **`__getattr__` forwarding** for pass-through surfaces — never re-list
  methods you aren't translating.

## Pitfalls

- **Adapting the whole surface** instead of what the client calls — you end
  up maintaining a second copy of the vendor's API.
- **Leaking adaptee types** through the adapter's returns (a vendor result
  dict escaping to the client re-couples everything the adapter decoupled).
- **Unifying calls but not failures.** If one vendor raises and the other
  returns an error status, the client is still vendor-aware. Normalize both.
- **Translation with opinions.** Retry, cache, or validation logic hiding in
  an adapter belongs in a Decorator/Proxy where it is visible and reusable.

## Worked example

[`examples/payment_gateways/`](../examples/payment_gateways/) integrates two
mismatched fake vendor SDKs behind one `PaymentProcessor` — run it with:

```bash
uv run python -m patterns.structural.adapter.examples.payment_gateways.main
```
