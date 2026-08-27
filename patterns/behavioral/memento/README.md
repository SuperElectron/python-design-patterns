---
id: behavioral/memento
name: Memento
aliases: [snapshot, undo-token]
guide_url: null
problem: "Capture an object's state so it can be restored later, without exposing its internals."
symptoms: ["undo", "checkpoint and rollback", "save game", "restore previous state"]
verdict: use-with-care
caveats:
  - "Immutable state makes the pattern nearly free: a snapshot is just keeping the old object. Design the state to be frozen and mementos fall out."
  - "pickle.loads executes code while deserializing — only unpickle snapshots your own process produced; use JSON for anything crossing a trust boundary."
  - "Deep-copying big mutable graphs per keystroke is the obvious-first-attempt cost; snapshot the smallest state that matters."
stdlib_sightings: [copy.deepcopy, pickle.dumps, dataclasses.replace]
---

# Memento

Keep "how it was" so you can go back — undo, checkpoints, rollback — without
letting the keeper read what it keeps. **Verdict: use with care** — freeze the
state and the pattern is nearly free.

| Where | What |
|---|---|
| [`pattern/`](pattern/) | The importable code: `History`, `NoSnapshotError` |
| [`docs/`](docs/) | [Fundamentals](docs/fundamentals.md) · [Implementation guide](docs/implementation.md) · [External examples](docs/examples.md) |
| [`examples/config_checkpoints/`](examples/config_checkpoints/) | Mini-project: validate-or-rollback config editing built on `pattern/` |
| [`tests/`](tests/) | Behavioral tests for the pattern and the mini-project |

```bash
uv run python -m patterns.behavioral.memento.examples.config_checkpoints.main
```
