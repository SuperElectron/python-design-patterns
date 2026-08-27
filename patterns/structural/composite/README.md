---
id: structural/composite
name: Composite
aliases: [tree, part-whole]
guide_url: https://python-patterns.guide/gang-of-four/composite/
problem: "Let callers treat a single object and a whole tree of objects through one interface."
symptoms: ["tree structure", "files and directories", "nested groups", "recursive totals", "uniform leaf and container API"]
verdict: pythonic
caveats:
  - "Don't force leaves to carry child-management methods (add/remove) just to match the container — the guide sides with interface honesty over uniformity."
  - "With duck typing you don't need a shared base class at all; share one only when it earns its keep."
stdlib_sightings: [pathlib.Path, xml.etree.ElementTree.Element]
---

# Composite

Part-whole trees where a leaf and a whole subtree answer the same operation —
and only containers manage children. **Verdict: pythonic** — the right shape
for trees; keep the leaf's interface honest.

| Where | What |
|---|---|
| [`pattern/`](pattern/) | The importable code: `Composite`, `HasTotal` |
| [`docs/`](docs/) | [Fundamentals](docs/fundamentals.md) · [Implementation guide](docs/implementation.md) · [External examples](docs/examples.md) |
| [`examples/org_chart/`](examples/org_chart/) | Mini-project: headcount/cost rollups over a nested org chart |
| [`tests/`](tests/) | Behavioral tests for the pattern and the mini-project |

```bash
uv run python -m patterns.structural.composite.examples.org_chart
```
