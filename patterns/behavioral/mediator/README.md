---
id: behavioral/mediator
name: Mediator
aliases: [coordinator, hub]
guide_url: null
problem: "Stop a web of objects from referencing each other by routing their interactions through one coordinator."
symptoms: ["widgets updating each other", "N-squared object references", "form fields with interdependent rules", "components need decoupling"]
verdict: use-with-care
caveats:
  - "The mediator earns its keep by deleting pairwise references; if it grows into a god object that knows everything, you traded a web for a blob."
  - "For pipeline-shaped decoupling, a queue between producers and consumers is the simpler mediator."
stdlib_sightings: [queue.Queue, asyncio.Queue]
---

# Mediator

Route component interactions through one coordinator that owns every rule.
**Verdict: use with care** — excellent for genuinely tangled rules; watch
for god-object drift.

| Where | What |
|---|---|
| [`pattern/`](pattern/) | The importable code: `Field` — a dumb value holder with change notification |
| [`docs/`](docs/) | [Fundamentals](docs/fundamentals.md) · [Implementation guide](docs/implementation.md) · [External examples](docs/examples.md) |
| [`examples/checkout_form/`](examples/checkout_form/) | Mini-project: cascading checkout rules built on `pattern/` |
| [`tests/`](tests/) | Behavioral tests for the pattern and the mini-project |

```bash
uv run python -m patterns.behavioral.mediator.examples.checkout_form
```
