---
id: behavioral/chain_of_responsibility
name: Chain of Responsibility
aliases: [chain, handler-chain]
guide_url: null
problem: "Pass a request along a line of handlers until one of them takes it."
symptoms: ["escalation levels", "middleware chain", "first handler that can, does", "fallback handlers"]
verdict: prefer-alternative
caveats:
  - "In Python the chain is a list of callables and a loop — successor pointers threaded through objects add nothing but pointer bookkeeping."
  - "Decide up front what an unhandled request means (exception? default?) — the GoF pattern is silent about falling off the end."
stdlib_sightings: [logging propagation, urllib.request opener chain]
---

# Chain of Responsibility

Pass a request along an ordered line of handlers until one takes it — without
the sender knowing which. **Verdict: prefer an alternative** — in Python the
chain is callables in a list, not objects with successor pointers.

| Where | What |
|---|---|
| [`pattern/`](pattern/) | The importable code: `Chain`, `Handler`, `UnhandledRequestError` |
| [`docs/`](docs/) | [Fundamentals](docs/fundamentals.md) · [Implementation guide](docs/implementation.md) · [External examples](docs/examples.md) |
| [`examples/ticket_escalation/`](examples/ticket_escalation/) | Mini-project: support-ticket routing built on `pattern/` |
| [`tests/`](tests/) | Behavioral tests for the pattern and the mini-project |

```bash
uv run python -m patterns.behavioral.chain_of_responsibility.examples.ticket_escalation.main
```
