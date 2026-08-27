# Builder — fundamentals

## Intent

Separate the construction of a complex object from its representation, so a
staged assembly process can be reused, validated step by step, and finished
into a product the caller cannot half-build.

## Participants

| Role | Classic (GoF) form | Python form |
|---|---|---|
| Builder contract | Abstract class of build steps | The builder's method surface — no interface needed |
| Concrete builder | One subclass per representation | A small mutable class — [`SelectBuilder`](../pattern/query.py) |
| Director | A class that walks the steps | The caller's own code (or a plain function) |
| Product | Whatever was accumulated | A frozen dataclass — `Query` |

## Mechanism

1. The builder starts from the one thing every product needs (here: a table).
2. Each step accumulates state, validates what a one-shot constructor could
   not express (placeholder counts, positive limits), and returns the builder
   for chaining.
3. `build()` snapshots the state into an immutable product. Mutating the
   builder afterwards cannot touch products already built.

## The classic form, and what Python absorbs

The textbook shape is a four-part ceremony — abstract builder, concrete
builders, and a Director that walks the steps:

```python
class HouseBuilder(ABC):
    @abstractmethod
    def build_walls(self) -> None: ...
    @abstractmethod
    def build_roof(self) -> None: ...


class StoneHouseBuilder(HouseBuilder): ...


class WoodHouseBuilder(HouseBuilder): ...


class Director:
    def construct(self, builder: HouseBuilder) -> House:
        builder.build_walls()
        builder.build_roof()
        return builder.house
```

Python dissolves most of it. Keyword arguments with defaults already kill the
telescoping constructor the pattern was invented for, and "same process,
different representation" is just passing a different callable — no abstract
interface, no Director class. What survives (the guide's own verdict) is the
**convenience builder**: a friendly mutable surface in front of an immutable
product, matplotlib's `pyplot` being the canonical ecosystem example.

## When to use it

- Construction is genuinely staged: parts arrive over time, or under
  conditions (`if product is not None: builder.where(...)`).
- Steps need validation *as they happen*, with errors at the faulty call.
- You want a mutable assembly surface but an immutable product.

## When not to use it

- All arguments are known at once → keyword arguments with defaults. A
  builder here is ceremony imported from another language.
- Different representations from the same steps → pass a different callable
  or family (see the abstract_factory unit), not a Director.

## Verdict: use with care

Reach for keyword arguments first. Write a builder when assembly is staged
and validated — and always split the mutable builder from a frozen product,
so "under construction" and "finished" are different types.
