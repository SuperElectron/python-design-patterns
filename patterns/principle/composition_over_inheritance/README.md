---
id: principle/composition_over_inheritance
name: Composition Over Inheritance
aliases: [subclass-explosion, favor-composition]
guide_url: https://python-patterns.guide/gang-of-four/composition-over-inheritance/
problem: "Vary independent behaviors without one subclass per combination of them."
symptoms: ["subclass explosion", "FilteredSocketLogger-style names", "M x N class combinations", "mixin soup"]
verdict: pythonic
caveats:
  - "Multiple inheritance, mixins, and dynamically built classes are the guide's 'dodges' — they postpone the explosion instead of ending it."
  - "Each independent axis of variation should become its own small object, injected where needed."
stdlib_sightings: [logging.Logger, logging.Handler, logging.Filter]
---

# Composition Over Inheritance

One small piece per axis of variation, composed at a single point: M + N
pieces instead of M × N subclasses. **Verdict: pythonic** — the most
load-bearing idea behind the rest of this catalog.

| Where | What |
|---|---|
| [`pattern/`](pattern/) | The importable code: `Pipeline` (the composition point), `Filter`/`Transform`/`Sink` axis aliases, and `Logger` built on it |
| [`docs/`](docs/) | [Fundamentals](docs/fundamentals.md) · [Implementation guide](docs/implementation.md) · [External examples](docs/examples.md) |
| [`examples/notification_router/`](examples/notification_router/) | Mini-project: alerts through filter × format × deliver pieces, zero combination subclasses |
| [`tests/`](tests/) | Behavioral tests for the pattern and the mini-project |

```bash
uv run python -m patterns.principle.composition_over_inheritance.examples.notification_router
```
