---
id: behavioral/state
name: State
aliases: [state-machine, finite-state-machine]
guide_url: null
problem: "Change an object's behavior when its internal state changes, without an if-forest over a mode flag."
symptoms: ["mode flag with branches everywhere", "state machine", "turnstile/order lifecycle", "behavior depends on current phase"]
verdict: use-with-care
caveats:
  - "For small machines, an Enum plus a transition table beats a class per state — the whole machine fits on one screen."
  - "A generator is often the best state machine of all: the suspension point is the state, and the interpreter maintains it for you."
stdlib_sightings: [enum.Enum, generators]
---

# State

Behavior that depends on "where we are" — gathered into one readable
transition table instead of mode-flag branches in every method.
**Verdict: use with care** — tables and generators cover most machines;
class-per-state only pays at real size.

| Where | What |
|---|---|
| [`pattern/`](pattern/) | The importable code: `StateMachine`, `Step`, `IllegalTransitionError` |
| [`docs/`](docs/) | [Fundamentals](docs/fundamentals.md) · [Implementation guide](docs/implementation.md) · [External examples](docs/examples.md) |
| [`examples/order_lifecycle/`](examples/order_lifecycle/) | Mini-project: an order FSM with guards and an audit log built on `pattern/` |
| [`tests/`](tests/) | Behavioral tests for the pattern and the mini-project |

```bash
uv run python -m patterns.behavioral.state.examples.order_lifecycle.main
```
