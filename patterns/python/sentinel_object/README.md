---
id: python/sentinel_object
name: Sentinel Object
aliases: [sentinel, missing-marker]
guide_url: https://python-patterns.guide/python/sentinel-object/
problem: "Mark 'no value here' unambiguously when None itself is a legitimate value."
symptoms: ["None is a valid value", "distinguish missing from null", "default argument that could be None", "str.find returns -1"]
verdict: pythonic
caveats:
  - "A sentinel must be compared with `is`, never `==` — its identity is its meaning."
  - "Sentinel *values* like -1 (str.find) live inside the value's own type and eventually collide; a fresh object() cannot."
  - "Fowler's Null Object pattern — a do-nothing stand-in with real methods — is the neighboring cure when callers would otherwise be littered with None checks."
stdlib_sightings: [dataclasses.MISSING, iter(callable, sentinel)]
---

# Sentinel Object

Mark "no value here" with an unforgeable object, so a legitimate `None` and
a genuine absence stop colliding. **Verdict: pythonic** — one named marker
per meaning, compared with `is`.

| Where | What |
|---|---|
| [`pattern/`](pattern/) | The importable code: `Sentinel` (named marker) and `MISSING` |
| [`docs/`](docs/) | [Fundamentals](docs/fundamentals.md) · [Implementation guide](docs/implementation.md) · [External examples](docs/examples.md) |
| [`examples/layered_config/`](examples/layered_config/) | Mini-project: CLI ← file ← defaults config where `None` means "explicitly disabled", plus a `NullNotifier` |
| [`tests/`](tests/) | Behavioral tests for the pattern and the mini-project |

```bash
uv run python -m patterns.python.sentinel_object.examples.layered_config
```
