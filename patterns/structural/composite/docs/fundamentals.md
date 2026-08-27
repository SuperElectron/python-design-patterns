# Composite — fundamentals

## Intent

Compose objects into part-whole trees, and let clients treat a single object
and a whole composition through one interface. A caller holding "something
with a size" should never need to ask whether it holds a file or a directory
of ten thousand of them.

## Participants

| Role | Classic (GoF) form | Python form |
|---|---|---|
| Component | Abstract base declaring the operation — and, contentiously, child management | A `Protocol` with just the operation (`HasTotal` in [`pattern/tree.py`](../pattern/tree.py)) — or nothing at all, duck typing suffices |
| Leaf | Subclass that must *refuse* `add()` at runtime | A plain frozen dataclass with the operation and no child API |
| Composite | Subclass holding children, recursing the operation | `Composite`: children + `add`/`remove` + the same operation |
| Client | Calls the component interface | Same — never asks a node which kind it is |

## Mechanism

1. Leaves and containers share one operation (`total()`).
2. A container's implementation combines its children's results; children may
   themselves be containers, so the recursion walks the whole tree.
3. Child management (`add`/`remove`) exists only on containers.
4. The client holds "a node" and calls the operation — uniformly at every
   depth.

## The classic form, and what Python absorbs

The textbook version declares the operation *and child management* on the
abstract component, so leaves must refuse children at runtime:

```python
class Graphic(ABC):
    @abstractmethod
    def render(self, indent: int = 0) -> str: ...

    def add(self, child: Graphic) -> None:  # on EVERY node...
        raise TypeError("cannot hold children")  # ...so leaves must refuse


class Circle(Graphic):  # leaf: inherits the trap
    def render(self, indent: int = 0) -> str: ...


class Group(Graphic):  # composite: overrides add()
    ...
```

Python absorbs the base class entirely: a leaf and a container that both
offer `total()` are already substitutable, so the shared ABC becomes at most
a `Protocol` for the type checker. That also dissolves the book's dilemma —
python-patterns.guide argues for **interface honesty over uniformity**
([guide chapter](https://python-patterns.guide/gang-of-four/composite/)):
with no forced base class, `add()` simply lives where it's true, on the
container, and a `TypeError`-at-runtime trap never exists.

## When to use it

- Genuine part-whole trees: file systems, org charts, GUI widget trees,
  nested groupings — anywhere "a thing or a group of things" recurses.
- Callers need one aggregate operation over arbitrary nesting.

## When not to use it

- The structure is flat — a list and a `sum()` need no pattern.
- Nodes need many unrelated operations — consider keeping the tree as data
  and writing traversals separately (see the Visitor unit's verdict).

## Verdict: pythonic

Trees are everywhere and this is the right shape for them. Keep the leaf's
interface honest, and share a base type only when it earns its keep.
