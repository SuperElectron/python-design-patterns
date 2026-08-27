---
id: python/prebound_method
name: Prebound Method
aliases: [bound-method-global]
guide_url: https://python-patterns.guide/python/prebound-methods/
problem: "Offer module-level functions that share state, by binding the methods of one hidden instance to module globals."
symptoms: ["module-level API over shared state", "random.random-style interface", "convenience functions plus an instantiable class"]
verdict: pythonic
caveats:
  - "Build the hidden instance cheaply and without I/O — it is constructed at import time."
  - "Keep the class public too, so users needing isolated state can instantiate their own (exactly as random.Random allows)."
stdlib_sightings: [random.random, random.seed, secrets.choice]
---

# Prebound Method

A `random.random()`-style module API: one hidden instance built at import,
its bound methods published as module functions, the class kept public for
isolation. **Verdict: pythonic** — the stdlib's own favorite move.

| Where | What |
|---|---|
| [`pattern/`](pattern/) | The importable code: canonical `Counter` + prebound `increment`/`peek`, and `shares_instance` (proves the wiring) |
| [`docs/`](docs/) | [Fundamentals](docs/fundamentals.md) · [Implementation guide](docs/implementation.md) · [External examples](docs/examples.md) |
| [`examples/metrics/`](examples/metrics/) | Mini-project: process-wide metrics API prebound from a hidden collector |
| [`tests/`](tests/) | Behavioral tests for the pattern and the mini-project |

```bash
uv run python -m patterns.python.prebound_method.examples.metrics.main
```
