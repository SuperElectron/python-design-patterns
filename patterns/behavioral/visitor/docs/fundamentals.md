# Visitor — fundamentals

## Intent

Run an operation over every node of an object structure — render, measure,
lint — without adding a method to every node class for every new operation.
The pattern separates *what the tree is* from *what you do to it*.

## Participants

| Role | Classic (GoF) form | Python form |
|---|---|---|
| Node contract | `accept(visitor)` on an Element interface | Nothing — nodes are plain (frozen) dataclasses |
| Concrete nodes | Each implements `accept` calling `visitor.visit_X(self)` | Just data |
| Visitor contract | An interface with one `visit_X` per node type | A dispatch family — `Operation` in [`pattern/dispatch.py`](../pattern/dispatch.py) |
| Concrete visitors | One class per operation | One `Operation` per operation; one small function per node type |
| Dispatch | Hand-written double dispatch via `accept` | `functools.singledispatch` on the node's type |

## Mechanism

1. Define the node types as plain data (a union type names the family).
2. For each operation, create an `Operation` and register one case per node
   type; composite cases recurse by calling the operation on children.
3. Apply the operation to the root. An unregistered node type raises
   `UnhandledNodeError` naming what *is* handled — the strict default the
   stdlib's `singledispatch` leaves to you.

## The classic form, and what Python absorbs

The textbook implementation threads dispatch plumbing through every class on
both sides:

```python
class Node(ABC):
    @abstractmethod
    def accept(self, visitor: Visitor) -> str: ...


class Number(Node):
    def accept(self, visitor: Visitor) -> str:
        return visitor.visit_number(self)  # plumbing, per node class


class Add(Node):
    def accept(self, visitor: Visitor) -> str:
        return visitor.visit_add(self)  # ...and again


class Visitor(ABC):
    @abstractmethod
    def visit_number(self, node: Number) -> str: ...

    @abstractmethod
    def visit_add(self, node: Add) -> str: ...
```

The `accept`/`visit_X` pair exists to fake **double dispatch** in languages
whose method calls dispatch only on the receiver. `functools.singledispatch`
dispatches on the argument's type directly, so the entire plumbing layer —
`accept` methods, the visitor interface, the node base class — evaporates.
What survives is the separation itself: operations live outside the node
classes, and a new operation touches zero of them.

## When to use it

- A stable node family needs an *open* set of operations (exporters,
  analyzers, metrics) — the pattern trades easy-new-operation for
  hard-new-node-type.
- You're walking a tree someone else defined and must not modify.

## When not to use it

- The *node family* grows more often than the operations → put methods on the
  nodes; every new type would force edits to every dispatch family anyway.
- One operation, once → a plain recursive function needs no registry.
- The tree is Python source → the stdlib already hands you the classic form:
  `ast.NodeVisitor`. Take it.

## Verdict: prefer an alternative

The alternative is `singledispatch` (what `Operation` packages, with a strict
default). The classic subclass form survives exactly where a framework hands
it to you — `ast.NodeVisitor` being the canonical case.
