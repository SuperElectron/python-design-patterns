# Facade — putting it into a system

## The smell it fixes

The same subsystem choreography pasted at every call site:

```python
# checkout_view.py            # admin_reorder.py          # support_tool.py
warehouse.reserve(sku, n)     warehouse.reserve(sku, n)   warehouse.reserve(sku, n)
txn = gateway.charge(...)     txn = gateway.charge(...)   txn = gateway.charge(...)
label = shipping.label(...)   # forgot the rollback!      label = shipping.label(...)
```

Three copies, one missing rollback, and the bug ships. The sequence is a
policy; policies live in one place.

## Steps

1. **Find the repeated dance.** Grep for the subsystem's entry calls; the
   facade's body is whatever keeps appearing between them.
2. **Write it as a function** taking the subsystem objects as parameters
   (dependency injection keeps it testable) plus keyword-only arguments for
   the order itself.
3. **Own the failure policy inside.** Partial completion is the facade's
   whole reason to exist: reserve-then-declined must release the stock. Be
   honest about the boundary — [`pattern/checkout.py`](../pattern/checkout.py)
   marks exactly where its rollback guarantee ends.
4. **Leave the subsystem public.** Export the classes beside the facade;
   write at least one caller that legitimately bypasses it (the
   mini-project's `Store.restock`) to prove the door stays open.
5. **Route existing call sites through the facade** and delete their local
   copies of the dance. The diff is the payoff: minus signs everywhere.

## Python idioms that keep it small

- **Module-level function, keyword-only config.** The natural Python facade
  is `def place_order(...)` in a module, not a `Manager` class.
- **Take collaborators as parameters** rather than constructing them inside —
  the facade coordinates, it doesn't own; tests swap in primed fakes.
- **Grow a class only when state accumulates.** `Store` in the mini-project
  holds the subsystem for a whole batch; that's state, so a class is honest.

## Pitfalls

- **The one-method class.** `CheckoutManager.place_order()` with no other
  members is a function in costume; write the function.
- **Imprisoning the subsystem** (private modules, mangled names) turns a
  convenience into a bottleneck; every future need funnels through you.
- **Silent partial completion.** A facade that charges the card and then
  crashes without compensating has *created* a bug factory. Decide: roll
  back, or document the boundary loudly.
- **Facade sprawl.** When `place_order` sprouts eleven flag parameters, the
  callers have distinct needs — give them the subsystem, not more flags.

## Worked example

[`examples/order_checkout/`](../examples/order_checkout/) processes a batch of
orders — one declined card among them — through the single checkout door.
Unusually for this catalog, the pattern package carries the whole domain:
`place_order` *is* the facade, so the mini-project adds only the batch
processing and the full-controls bypass around it:

```bash
uv run python -m patterns.structural.facade.examples.order_checkout.main
```
