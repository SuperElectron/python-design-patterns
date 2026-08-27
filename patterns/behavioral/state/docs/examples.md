# State — where it lives outside this repo

Cited, real implementations to study (or point an agent at) when designing or
reviewing state-machine code.

## Python standard library

- **`enum.Enum`** — states as first-class, finite, typo-proof values; the
  foundation the table form assumes.
  [docs.python.org/3/library/enum.html](https://docs.python.org/3/library/enum.html)
- **Generators** — the interpreter-maintained state machine: the suspension
  point is the state. Every `yield`-based parser and pipeline stage is this
  pattern with zero state fields.
  [docs.python.org/3/reference/expressions.html#yield-expressions](https://docs.python.org/3/reference/expressions.html#yield-expressions)
- **`asyncio.Task` lifecycle** — pending → running → done/cancelled, with
  rules about which motions exist (`cancel()` on a done task is a no-op that
  returns False): a transition table in prose.
  [docs.python.org/3/library/asyncio-task.html](https://docs.python.org/3/library/asyncio-task.html)

## Libraries built on the pattern

- **transitions (pytransitions)** — the most-used Python FSM library:
  declarative tables, guards ("conditions"), callbacks, hierarchical
  machines — this module's `StateMachine` grown to production size.
  [github.com/pytransitions/transitions](https://github.com/pytransitions/transitions) *(unverified)*
- **django-fsm / viewflow.fsm** — lifecycle guards on Django model fields:
  `@transition(source, target)` decorators putting the table next to the
  model it rules. [github.com/viewflow/django-fsm](https://github.com/viewflow/django-fsm) *(unverified)*

## The classic specification

- **TCP's connection diagram (RFC 9293 §3.3.2)** — LISTEN, SYN-SENT,
  ESTABLISHED, TIME-WAIT... the state machine every networked program rides
  on, specified as exactly a transition table.
  [rfc-editor.org/rfc/rfc9293](https://www.rfc-editor.org/rfc/rfc9293) *(unverified)*

## What to notice across all of them

The serious ones publish their table (TCP's diagram, pytransitions'
declaration) rather than burying motion rules in methods — the machine you
can *read whole* is the feature. And each distinguishes state from data:
`asyncio` keeps a task's result out of its state set the same way a guard
keeps `amount_paid` out of an order's.
