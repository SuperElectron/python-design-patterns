---
id: modern/context_manager
name: Context Manager
aliases: [with-statement, RAII, resource-management]
guide_url: null
problem: "Guarantee acquire/release pairing around a block of code, even when it raises."
symptoms: ["forgot to close", "cleanup on exception", "try/finally everywhere", "temporary state that must be restored"]
verdict: pythonic
caveats:
  - "@contextlib.contextmanager wants the yield inside try/finally — without it, an exception in the body skips your cleanup."
  - "Returning True from __exit__ swallows the exception; do it only on purpose."
stdlib_sightings: [open, contextlib.contextmanager, contextlib.ExitStack, tempfile.TemporaryDirectory]
---

# Context Manager

Pair acquire with release on every exit path, structurally — Python's RAII.
**Verdict: pythonic** — any acquire/release pair you write twice deserves one.

| Where | What |
|---|---|
| [`pattern/`](pattern/) | The importable code: `AtomicWrite` (protocol form), `temporarily` (generator form) |
| [`docs/`](docs/) | [Fundamentals](docs/fundamentals.md) · [Implementation guide](docs/implementation.md) · [External examples](docs/examples.md) |
| [`examples/atomic_deploy/`](examples/atomic_deploy/) | Mini-project: all-or-nothing config deployment via `ExitStack` |
| [`tests/`](tests/) | Behavioral tests for both managers and the mini-project |

```bash
uv run python -m patterns.modern.context_manager.examples.atomic_deploy.main
```
