---
id: creational/singleton
name: Singleton
aliases: [single-instance]
guide_url: https://python-patterns.guide/gang-of-four/singleton/
problem: "Guarantee a class has exactly one instance and give the whole program access to it."
symptoms: ["shared config object", "one connection pool", "global registry", "only one instance"]
verdict: prefer-alternative
caveats:
  - "You almost always want the Global Object pattern instead: build the instance at import time in a module and import it."
  - "Singleton classes make tests order-dependent — state leaks between tests through the hidden instance."
  - "The GoF __new__ dance still runs __init__ on every call in Python; a factory function avoids the trap entirely."
stdlib_sightings: [None, Ellipsis, NotImplemented]
---

# Singleton

One instance for the whole process, reachable from anywhere. **Verdict: prefer
an alternative** — a module already is a singleton; write a module-level
instance, or a `Shared` accessor when construction must wait. Keep a reset
seam for tests.

| Where | What |
|---|---|
| [`pattern/`](pattern/) | The importable code: `Shared` — lazy build, one instance, `reset()` seam |
| [`docs/`](docs/) | [Fundamentals](docs/fundamentals.md) · [Implementation guide](docs/implementation.md) · [External examples](docs/examples.md) |
| [`examples/app_config/`](examples/app_config/) | Mini-project: process-wide settings behind `get_settings()` |
| [`tests/`](tests/) | Behavioral tests for the pattern and the mini-project |

```bash
uv run python -m patterns.creational.singleton.examples.app_config.main
```
