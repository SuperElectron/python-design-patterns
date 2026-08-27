# State — putting it into a system

## The smell it fixes

A mode flag branching in every method — the machine exists, but smeared:

```python
class Order:
    def cancel(self):
        if self.status in ("placed", "paid"):  # rule fragment here
            self.status = "cancelled"
        else:
            raise ValueError("too late")

    def refund(self):
        if self.status == "paid" and self.amount_paid > 0:  # fragment there
            ...
```

Nobody can read the whole lifecycle, and a new status means auditing every
method. The pattern gathers the machine into one visible table.

## Steps

1. **Name states and events as Enums.** Strings work but typos become
   runtime surprises; Enum members make the table exhaustive to the reader
   and checkable by mypy.
2. **Write the transition table** `(state, event) -> state`. Review it like
   policy, because it is policy: the absent pairs are the business rules
   ("no cancel after shipment" is a row that *does not exist*).
3. **Add guards only for data rules.** Shape rules belong in the table;
   guards (`lambda: order.amount_paid > 0`) are for decisions the current
   data must make. A guard that ignores data belongs in the table instead.
4. **Route every change through `trigger`.** The domain object keeps its
   fields; its *status* moves only via the machine, so illegal motion is an
   exception, not a silent field write.
5. **Use the log.** The machine already records `source --event--> target`
   for each step — that is the audit trail ops asks for later, free.

```python
from patterns.behavioral.state import StateMachine


def build_lifecycle(order: Order) -> StateMachine[OrderStatus, OrderAction]:
    return StateMachine(
        initial=OrderStatus.CART,
        table=LIFECYCLE,
        guards={(OrderStatus.PAID, OrderAction.REFUND): lambda: order.amount_paid > 0},
    )
```

## Python idioms that keep it small

- The table as a **module-level dict** makes the machine importable,
  testable, and rendered whole in one diff hunk.
- Guards are **closures over the domain object** — no context parameter
  threading, no subclassing.
- `machine.can(event)` drives UIs ("which buttons to show") from the same
  table that enforces the rules — one source of truth.
- When the machine is a linear consumption loop, skip the class: **write a
  generator** and let the paused frame hold the state.

## Pitfalls

- **Bypassing the machine.** One `order.status = X` assignment elsewhere and
  the table lies. Make status transitions go through `trigger` only.
- **Guards with side effects.** `can()` calls guards too — a guard that
  charges a card on inspection charges it twice. Guards decide; actions act.
- **Stringly-typed states** drift ("Paid" vs "paid") and silently add
  unreachable rows. Enums close the set.
- **The god-machine.** If the table needs sub-states of sub-states, you have
  several machines (payment, fulfillment) sharing an object — split them.
- **Machine state vs. domain data confusion.** `amount_paid` is data;
  `PAID` is state. Guards exist precisely so data can stay out of the state
  space instead of exploding it (`PAID_IN_FULL`, `PAID_PARTIALLY`, ...).

## Worked example

[`examples/order_lifecycle/`](../examples/order_lifecycle/) applies every
step: an eight-row table, two data guards, refusal of a too-late cancel, and
the audit log printed at the end. Run it with:

```bash
uv run python -m patterns.behavioral.state.examples.order_lifecycle
```
