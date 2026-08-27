---
id: structural/decorator
name: Decorator
aliases: [wrapper]
guide_url: https://python-patterns.guide/gang-of-four/decorator-pattern/
problem: "Add behavior around an object or callable without editing it or subclassing it."
symptoms: ["logging every call", "caching results", "retry wrapper", "timing calls", "add behavior without subclassing"]
verdict: pythonic
caveats:
  - "The GoF pattern (wrapping objects) and Python's @decorator syntax (wrapping callables) are cousins, not the same thing — this unit shows both."
  - "Always apply functools.wraps to function wrappers, or you destroy the wrapped function's name, docstring, and introspection."
  - "The guide's caveat: an object wrapper doesn't survive isinstance checks or identity comparisons — wrapping doesn't actually make you the wrapped thing."
stdlib_sightings: [functools.wraps, functools.lru_cache, contextlib.contextmanager]
---

# Decorator

Add one cross-cutting concern at a time — logging, timing, retries, limits —
by wrapping, then stack the wrappers. **Verdict: pythonic** — for callables the
language absorbed the pattern into `@decorator` syntax.

| Where | What |
|---|---|
| [`pattern/`](pattern/) | The importable code: `logged`, `timed`, `retry`, `rate_limited` |
| [`docs/`](docs/) | [Fundamentals](docs/fundamentals.md) · [Implementation guide](docs/implementation.md) · [External examples](docs/examples.md) |
| [`examples/resilient_client/`](examples/resilient_client/) | Mini-project: a flaky API client hardened by stacking `pattern/` decorators |
| [`tests/`](tests/) | Behavioral tests for the pattern and the mini-project |

```bash
uv run python -m patterns.structural.decorator.examples.resilient_client
```
