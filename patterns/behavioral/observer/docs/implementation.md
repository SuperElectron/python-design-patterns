# Observer — putting it into a system

## The smell it fixes

The subject hard-codes its audience:

```python
def mark_shipped(self, order):
    order.status = "shipped"
    email.send_shipped_notice(order)  # the pipeline now imports email,
    metrics.incr("orders.shipped")  # metrics, audit ... and grows a
    audit.record(order, "shipped")  # new import per interested party
```

Every new reaction edits the pipeline. Inverted, the pipeline emits one
event and reactions subscribe from their own modules.

## Steps

1. **Make the event a value.** A small frozen dataclass carrying what
   subscribers need — not the subject itself (that re-couples them).
2. **Give the subject a `Signal`.** One per event kind beats one bus with
   string topics; the type parameter documents the payload.
3. **Choose the failure policy at construction.** The default propagates —
   right for tests and for subscribers that are truly part of the operation.
   Pass `on_error` to isolate: log to a dead-letter list, keep notifying.
   Never decide this by accident.
4. **Subscribe at the edges.** Wiring (`signal.subscribe(...)`) belongs in
   composition code — the app's startup, a fixture — not inside the subject.
5. **Pin order only if it means something.** Subscribers run in subscription
   order; if a test doesn't assert an ordering requirement, you don't have one.

```python
from patterns.behavioral.observer import Signal


class OrderPipeline:
    def __init__(self) -> None:
        self.events: Signal[OrderEvent] = Signal(on_error=self._quarantine)

    def advance(self, order_id: str, status: str, total: float) -> None:
        self.events.emit(OrderEvent(order_id, status, total))
```

## Python idioms that keep it small

- Subscribers are **plain callables**: `seen.append` subscribes a list's own
  method; a lambda subscribes a filter; a class with `__call__` subscribes
  stateful behavior.
- `signal.subscribe` as a **decorator** registers a handler at definition
  site — the shape Django's `@receiver` and Flask's hooks made familiar.
- Hide the emit behind a **property setter** when the "event" is really an
  attribute change — callers write plain assignment.

## Pitfalls

- **One raising subscriber silencing the rest** — the load-bearing caveat.
  `Signal`'s default is honest (it propagates loudly); switch to `on_error`
  isolation the moment subscribers belong to different owners.
- **Mutating the subscriber list mid-broadcast.** `emit` iterates a copy so
  self-unsubscribing handlers are safe — preserve that if you hand-roll.
- **Fat events.** Passing the mutable subject as the event invites
  subscribers to write to it; broadcast immutable facts.
- **Hidden ordering contracts.** If metrics must run before email, that is
  pipeline logic, not observation — make it one subscriber or one explicit
  sequence.
- **Expecting delivery guarantees.** In-process observers give none: no
  retry, no persistence, gone on crash. Needing those means a queue, not
  this pattern.

## Worked example

[`examples/order_events/`](../examples/order_events/) applies every step:
one pipeline, four independent subscribers, a down webhook quarantined to a
dead-letter list while the rest keep working. Run it with:

```bash
uv run python -m patterns.behavioral.observer.examples.order_events
```
