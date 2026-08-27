---
id: behavioral/iterator
name: Iterator
aliases: [cursor]
guide_url: https://python-patterns.guide/gang-of-four/iterator/
problem: "Traverse a container's elements without exposing how the container stores them."
symptoms: ["custom traversal order", "lazy sequence", "for loop over my own class", "stream elements one at a time"]
verdict: pythonic
caveats:
  - "The container and its iterator are different objects with different jobs: the container's __iter__ returns a fresh iterator; the iterator's __iter__ returns itself."
  - "Writing __next__ by hand is almost always the wrong level — a generator implements the whole protocol for you."
stdlib_sightings: [iter, next, generators, itertools]
---

# Iterator

Traverse elements without exposing storage — lazily when it matters.
**Verdict: pythonic** — the pattern is the language; write generators.

| Where | What |
|---|---|
| [`pattern/`](pattern/) | The importable code: `iterate_pages` — chunked traversal behind one generator |
| [`docs/`](docs/) | [Fundamentals](docs/fundamentals.md) · [Implementation guide](docs/implementation.md) · [External examples](docs/examples.md) |
| [`examples/paginated_client/`](examples/paginated_client/) | Mini-project: observably lazy article API client built on `pattern/` |
| [`tests/`](tests/) | Behavioral tests for the pattern and the mini-project |

```bash
uv run python -m patterns.behavioral.iterator.examples.paginated_client
```
