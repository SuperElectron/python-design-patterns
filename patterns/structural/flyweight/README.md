---
id: structural/flyweight
name: Flyweight
aliases: [interning, shared-instances]
guide_url: https://python-patterns.guide/gang-of-four/flyweight/
problem: "Support huge numbers of fine-grained objects by sharing immutable instances instead of duplicating them."
symptoms: ["millions of small objects", "memory pressure from duplicates", "interning", "shared immutable state"]
verdict: use-with-care
caveats:
  - "Flyweights must be immutable — a mutated shared instance corrupts every holder at once."
  - "The guide notes Python's twist: hide the sharing in the constructor via __new__, or expose it as a factory function; the factory is easier to reason about."
  - "Measure first: CPython already interns small ints and many strings, so your duplicates may not exist."
stdlib_sightings: [sys.intern, functools.lru_cache, int]
---

# Flyweight

Share one immutable instance per distinct value instead of building millions
of duplicates. **Verdict: use with care** — measure first, keep flyweights
frozen, prefer an explicit factory over `__new__` tricks.

| Where | What |
|---|---|
| [`pattern/`](pattern/) | The importable code: `InternPool` (keyed sharing with an immutability guard) |
| [`docs/`](docs/) | [Fundamentals](docs/fundamentals.md) · [Implementation guide](docs/implementation.md) · [External examples](docs/examples.md) |
| [`examples/glyph_styles/`](examples/glyph_styles/) | Mini-project: a text buffer holding thousands of glyphs on a handful of shared styles |
| [`tests/`](tests/) | Behavioral tests for the pattern and the mini-project |

```bash
uv run python -m patterns.structural.flyweight.examples.glyph_styles.main
```
