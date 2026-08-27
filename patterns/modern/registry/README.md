---
id: modern/registry
name: Registry
aliases: [plugin-registry, dispatch-table]
guide_url: null
problem: "Let implementations announce themselves by name, so dispatch is a lookup instead of an if/elif ladder."
symptoms: ["if/elif on a type string", "plugin system", "handlers by name", "adding a case means editing the dispatcher"]
verdict: pythonic
caveats:
  - "Registration at import time means the module defining a plugin must actually get imported — a plugin nobody imports doesn't exist."
  - "Decide the unknown-key policy (KeyError? default handler?) once, in the lookup, not at each call site."
stdlib_sightings: [codecs.register, functools.singledispatch, atexit.register]
---

# Registry

Implementations announce themselves by name; dispatch is a lookup, and adding
a case is writing one new function. **Verdict: pythonic** — the standard cure
for `if/elif` dispatch.

| Where | What |
|---|---|
| [`pattern/`](pattern/) | The importable code: `Registry`, `UnknownKeyError` |
| [`docs/`](docs/) | [Fundamentals](docs/fundamentals.md) · [Implementation guide](docs/implementation.md) · [External examples](docs/examples.md) |
| [`examples/export_plugins/`](examples/export_plugins/) | Mini-project: self-registering exporters, one in a separate plugin module |
| [`tests/`](tests/) | Behavioral tests for the pattern and the mini-project |

```bash
uv run python -m patterns.modern.registry.examples.export_plugins
```
