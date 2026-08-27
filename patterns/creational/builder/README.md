---
id: creational/builder
name: Builder
aliases: [fluent-builder]
guide_url: https://python-patterns.guide/gang-of-four/builder/
problem: "Assemble a complex object step by step, so the assembly process is reusable and readable."
symptoms: ["constructor with ten arguments", "object needs staged assembly", "fluent chained construction", "same steps, different representations"]
verdict: use-with-care
caveats:
  - "Python's keyword arguments with defaults already solve the 'telescoping constructor' problem the GoF Builder exists for."
  - "The guide's verdict: the Builder survives in Python mainly as a convenience for callers (e.g. matplotlib's pyplot), not as a construction ceremony."
stdlib_sightings: [email.message.EmailMessage, configparser.ConfigParser]
---

# Builder

Assemble a complex object step by step, with validation at each step and an
immutable result. **Verdict: use with care** — keyword arguments already
solve one-shot construction; a builder earns its keep only when assembly is
genuinely staged.

| Where | What |
|---|---|
| [`pattern/`](pattern/) | The importable code: `SelectBuilder` (mutable, fluent) → `Query` (frozen) |
| [`docs/`](docs/) | [Fundamentals](docs/fundamentals.md) · [Implementation guide](docs/implementation.md) · [External examples](docs/examples.md) |
| [`examples/sql_select_builder/`](examples/sql_select_builder/) | Mini-project: order analytics on sqlite, every query builder-staged |
| [`tests/`](tests/) | Behavioral tests for the pattern and the mini-project |

```bash
uv run python -m patterns.creational.builder.examples.sql_select_builder
```
