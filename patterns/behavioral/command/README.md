---
id: behavioral/command
name: Command
aliases: [action, transaction]
guide_url: null
problem: "Package a request as an object so it can be queued, logged, undone, or executed later by code that doesn't know its details."
symptoms: ["undo/redo", "task queue", "macro recording", "button callbacks", "audit log of operations"]
verdict: use-with-care
caveats:
  - "If you only need 'execute later', a plain callable or functools.partial is the whole pattern — don't build a class hierarchy for a deferred call."
  - "The class form earns its keep exactly when commands carry extra behavior: undo(), serialization, or metadata."
stdlib_sightings: [functools.partial, sched.scheduler, unittest.mock.call]
---

# Command

Package a request as an object so it can be queued, logged, undone, or run by
code that doesn't know its details. **Verdict: use with care** — a callable is
the whole pattern until commands need undo, logs, or metadata.

| Where | What |
|---|---|
| [`pattern/`](pattern/) | The importable code: `Undoable`, `UndoStack`, `Action` |
| [`docs/`](docs/) | [Fundamentals](docs/fundamentals.md) · [Implementation guide](docs/implementation.md) · [External examples](docs/examples.md) |
| [`examples/editor_undo/`](examples/editor_undo/) | Mini-project: text-editor undo/redo built on `pattern/` |
| [`tests/`](tests/) | Behavioral tests for the pattern and the mini-project |

```bash
uv run python -m patterns.behavioral.command.examples.editor_undo
```
