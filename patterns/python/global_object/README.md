---
id: python/global_object
name: Global Object
aliases: [module-global, constant-pattern]
guide_url: https://python-patterns.guide/python/module-globals/
problem: "Give a whole program shared access to a constant or a pre-built object by assigning it at module level."
symptoms: ["shared constants", "one shared instance", "config everyone imports", "what Singleton actually wants to be"]
verdict: use-with-care
caveats:
  - "Mutable globals couple everything that touches them and make tests order-dependent — prefer constants, or objects whose mutation is their documented job (like os.environ)."
  - "Never do I/O at import time: importing must be cheap and safe, or every consumer pays (and test runs touch the network/disk)."
stdlib_sightings: [os.environ, calendar.day_name, math.pi]
---

# Global Object

Share a constant or a pre-built object program-wide by assigning it at module
level — Python's native singleton. **Verdict: use with care** — constants
freely, expensive things lazily, mutation only where it is the documented job.

| Where | What |
|---|---|
| [`pattern/`](pattern/) | The importable code: `Lazy` (deferred construction + test-reset seam) |
| [`docs/`](docs/) | [Fundamentals](docs/fundamentals.md) · [Implementation guide](docs/implementation.md) · [External examples](docs/examples.md) |
| [`examples/settings_module/`](examples/settings_module/) | Mini-project: an app settings module with all three kinds of global |
| [`tests/`](tests/) | Behavioral tests for the pattern and the mini-project |

```bash
uv run python -m patterns.python.global_object.examples.settings_module.main
```
