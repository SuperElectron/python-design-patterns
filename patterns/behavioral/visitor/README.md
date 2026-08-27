---
id: behavioral/visitor
name: Visitor
aliases: [double-dispatch]
guide_url: null
problem: "Run a new operation over every node of an object structure without adding a method to every node class."
symptoms: ["walk an AST", "operation per node type", "double dispatch", "add behavior across a class family"]
verdict: prefer-alternative
caveats:
  - "functools.singledispatch dispatches on type without touching the node classes — the visitor with the accept() plumbing deleted."
  - "The subclass form survives where the stdlib hands it to you: ast.NodeVisitor is the right tool for walking Python source."
stdlib_sightings: [functools.singledispatch, ast.NodeVisitor]
---

# Visitor

New operations over a node structure, without editing the nodes. **Verdict:
prefer an alternative** — `singledispatch` deletes the `accept()` plumbing;
the subclass form survives at stdlib boundaries (`ast.NodeVisitor`).

| Where | What |
|---|---|
| [`pattern/`](pattern/) | The importable code: `Operation`, `UnhandledNodeError` |
| [`docs/`](docs/) | [Fundamentals](docs/fundamentals.md) · [Implementation guide](docs/implementation.md) · [External examples](docs/examples.md) |
| [`examples/doc_exporters/`](examples/doc_exporters/) | Mini-project: document exporters built on `pattern/` |
| [`tests/`](tests/) | Behavioral tests for the pattern and the mini-project |

```bash
uv run python -m patterns.behavioral.visitor.examples.doc_exporters.main
```
