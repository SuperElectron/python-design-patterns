# Composite — putting it into a system

## The smell it fixes

Type-switching every time a structure nests:

```python
def org_cost(node):
    if isinstance(node, Employee):
        return node.salary
    if isinstance(node, Department):
        total = 0
        for member in node.members:
            total += org_cost(member)  # and every new node kind edits this
        return total
```

Every aggregate operation re-implements the traversal, and every new node
kind edits every operation. The composite moves the recursion into the
container once; operations become one method both node kinds answer.

## Steps

1. **Pick the rollup value type.** One number is fine; several measures that
   should travel together become a small frozen dataclass with `__add__`
   (the org example's `OrgMetrics` carries headcount *and* cost in one pass).
2. **Make leaves plain frozen dataclasses** with the operation and nothing
   else — no child API, ever.
3. **Use `Composite` for containers** (or subclass it to add a name and
   domain methods). Pass its `combine` explicitly — `sum` with a `start`
   value is usually all you need.
4. **Keep child mutation on the container** and let `remove` raise on absent
   children — silent no-ops hide reorg bugs.
5. **Test the rollups through nesting**, not just one level: build a small
   tree in a fixture, assert totals at every depth, and assert leaves have
   no `add` (interface honesty is a testable property —
   `not hasattr(leaf, "add")`).

```python
from dataclasses import dataclass

from patterns.structural.composite import Composite


@dataclass(frozen=True)
class Task:  # a leaf: totals itself, has no child API
    hours: int

    def total(self) -> int:
        return self.hours


team = Composite(sum, [Task(3), Task(5)])
project = Composite(sum, [team, Task(8)])
assert project.total() == 16
```

## Python idioms that keep it small

- **`Protocol` instead of an ABC** — the type checker enforces the shared
  operation; nodes stay free of inheritance.
- **Frozen dataclass leaves** — hashable, comparable, safe to share between
  branches.
- **A metrics dataclass with `__add__`** rolls several measures up in one
  traversal instead of one walk per measure.
- **Generators for traversal**: `iter(composite)` walks one level; recursive
  generators (`yield from`) give you `rglob`-style deep iteration when you
  need node access rather than totals.

## Pitfalls

- **Child management on the component interface** — the classic form's trap:
  leaves inherit an `add()` they must refuse at runtime. Keep it on the
  container only.
- **Parent pointers by default.** They turn a value tree into a mutable graph
  with invalidation puzzles; add them only when navigation truly needs them.
- **Unbounded recursion trust.** Deep or user-built trees can hit recursion
  limits and cycles; if inputs are hostile, traverse iteratively and track
  visited nodes.
- **Mixing structure and presentation** (a `render()` that formats *and*
  recurses *and* sorts) — keep the tree operation minimal and format outside.

## Worked example

[`examples/org_chart/`](../examples/org_chart/) rolls headcount and annual
cost up a nested org chart — run it with:

```bash
uv run python -m patterns.structural.composite.examples.org_chart
```
