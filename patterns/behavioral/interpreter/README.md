---
id: behavioral/interpreter
name: Interpreter
aliases: [little-language, expression-tree]
guide_url: null
problem: "Represent a small language's grammar as data and evaluate sentences in it."
symptoms: ["mini query language", "user-supplied formulas", "rules engine", "evaluate expressions safely"]
verdict: prefer-alternative
caveats:
  - "Before inventing a language, check whether Python is the language: ast.literal_eval for data, a vetted ast walk for arithmetic, a real parser library beyond that."
  - "Never eval() user input — the safe version of this pattern exists precisely to avoid that."
stdlib_sightings: [ast.literal_eval, ast.NodeVisitor, re]
---

# Interpreter

Represent a tiny language's grammar as data and evaluate sentences safely.
**Verdict: prefer an alternative** — Python's own parsers (`ast`, `re`) cover
most little-language needs; grammar-as-data covers the rest.

| Where | What |
|---|---|
| [`pattern/`](pattern/) | The importable code: `Interpreter` (tuple-tree evaluator), hardened `safe_eval` |
| [`docs/`](docs/) | [Fundamentals](docs/fundamentals.md) · [Implementation guide](docs/implementation.md) · [External examples](docs/examples.md) |
| [`examples/flag_rules/`](examples/flag_rules/) | Mini-project: feature-flag rules engine built on `pattern/` |
| [`tests/`](tests/) | Behavioral tests for the pattern and the mini-project |

```bash
uv run python -m patterns.behavioral.interpreter.examples.flag_rules
```
