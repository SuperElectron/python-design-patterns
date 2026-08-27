# Bridge — fundamentals

## Intent

Decouple an abstraction from its implementation so the two can vary
independently. When one family of things (notifiers, shapes, reports) must
work over another family (transports, renderers, backends), inheritance
multiplies the axes into one hierarchy; the bridge keeps them as two, joined
by a single reference.

## Participants

| Role | Classic (GoF) form | Python form |
|---|---|---|
| Abstraction | Base class holding an implementor reference | A dataclass holding an injected dependency |
| RefinedAbstraction | Subclasses adding behavior | More dataclasses on the same bridge |
| Implementor | Abstract implementation interface | A `Protocol` — `Transport` in [`pattern/bridge.py`](../pattern/bridge.py) |
| ConcreteImplementor | Subclasses per backend | Any object satisfying the Protocol |

## Mechanism

1. Name the two axes explicitly (what varies about *what you do* vs *how it
   is carried out*).
2. Type the implementor axis as a small interface the abstraction calls.
3. The abstraction holds one implementor, received at construction.
4. Each axis now grows without touching the other: M abstractions + N
   implementors give M × N combinations from M + N classes.

## The classic form, and what Python absorbs

The textbook bridge builds two parallel class hierarchies and an abstract
base on each side:

```python
class Renderer(ABC):  # Implementor interface
    @abstractmethod
    def render_circle(self, radius: float) -> str: ...


class VectorRenderer(Renderer): ...  # one subclass per backend


class RasterRenderer(Renderer): ...


class Shape(ABC):  # Abstraction holds the bridge
    def __init__(self, renderer: Renderer) -> None:
        self.renderer = renderer


class Circle(Shape):
    def draw(self) -> str:
        return self.renderer.render_circle(self.radius)
```

Python absorbs nearly all of it: the implementor interface becomes a
`Protocol` (no base class for backends to inherit), the abstraction becomes a
frozen dataclass, and "connect abstraction to implementation" is just an
injected attribute. What survives is the design move, not the class diagram:
**name the two axes and join them with one reference** instead of subclassing
across both.

## When to use it

- Two independent dimensions are multiplying subclasses
  (`VectorCircle`, `RasterCircle`, `VectorSquare`…).
- A stable front must run over swappable backends, and both sides are still
  growing.

## When not to use it

- Only one axis actually varies — plain composition already covers it, no
  naming ceremony needed.
- The "implementations" are one function each — pass callables, skip the
  Protocol.

## Verdict: prefer an alternative

Composition with an injected dependency *is* the bridge in Python. Keep the
lesson (two named axes, one reference), skip the four-role taxonomy.
