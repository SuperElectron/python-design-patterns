---
id: behavioral/strategy
name: Strategy
aliases: [policy]
guide_url: null
problem: "Make an algorithm interchangeable at runtime without the caller knowing which variant it got."
symptoms: ["swap algorithm at runtime", "pricing rules", "pluggable policy", "if/elif chain choosing behavior"]
verdict: prefer-alternative
caveats:
  - "In Python a strategy is just a function passed as an argument — the class-per-algorithm hierarchy is Java's workaround for lacking first-class functions."
  - "Reach for the class form only when a strategy carries its own state or several related methods."
stdlib_sightings: [sorted, list.sort, functools.cmp_to_key]
---

# Strategy

Swap the algorithm without touching the caller. **Verdict: prefer an
alternative** — in Python a strategy is a function passed as an argument;
the registry below is for families that grow.

| Where | What |
|---|---|
| [`pattern/`](pattern/) | The importable code: `StrategyRegistry`, `UnknownStrategyError` |
| [`docs/`](docs/) | [Fundamentals](docs/fundamentals.md) · [Implementation guide](docs/implementation.md) · [External examples](docs/examples.md) |
| [`examples/promotions/`](examples/promotions/) | Mini-project: checkout pricing rules built on `pattern/` |
| [`tests/`](tests/) | Behavioral tests for the pattern and the mini-project |

```bash
uv run python -m patterns.behavioral.strategy.examples.promotions.main
```
