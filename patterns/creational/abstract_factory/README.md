---
id: creational/abstract_factory
name: Abstract Factory
aliases: [kit, factory-of-factories]
guide_url: https://python-patterns.guide/gang-of-four/abstract-factory/
problem: "Let code build families of related objects without naming their concrete classes."
symptoms: ["swap whole family of implementations", "test doubles for created objects", "library must not hardcode which class it builds"]
verdict: prefer-alternative
caveats:
  - "The pattern exists because 1990s languages could not pass classes or functions as values — Python can, so a factory is usually just a callable argument."
  - "Reach for a factory *object* only when the family of factories is large enough that bundling them beats passing them individually."
stdlib_sightings: [json.load parse_float, decimal.Decimal, unittest.mock]
---

# Abstract Factory

Build families of related objects without naming their concrete classes.
**Verdict: prefer an alternative** — in Python a factory is a callable
argument; bundle callables into a family object only when they must stay
consistent with each other.

| Where | What |
|---|---|
| [`pattern/`](pattern/) | The importable code: `DocumentFamily`, `HTML`, `MARKDOWN` |
| [`docs/`](docs/) | [Fundamentals](docs/fundamentals.md) · [Implementation guide](docs/implementation.md) · [External examples](docs/examples.md) |
| [`examples/report_renderer/`](examples/report_renderer/) | Mini-project: one quarterly report through two document families |
| [`tests/`](tests/) | Behavioral tests for the pattern and the mini-project |

```bash
uv run python -m patterns.creational.abstract_factory.examples.report_renderer
```
