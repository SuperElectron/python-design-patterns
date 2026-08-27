# Flyweight — fundamentals

## Intent

Support huge numbers of fine-grained objects by sharing one immutable
instance per distinct value instead of duplicating it. Split state into
**intrinsic** (shared, in the flyweight) and **extrinsic** (per occurrence,
carried by the holder).

## Participants

| Role | Classic (GoF) form | Python form |
|---|---|---|
| Flyweight | Interface for objects carrying intrinsic state | Any immutable value — a frozen dataclass, a tuple |
| Flyweight factory | Checks a pool before constructing | [`InternPool`](../pattern/pool.py), or `functools.lru_cache` on a factory |
| Client | Supplies extrinsic state on each use | The holder keeps `(char, style)`, not a fat per-char object |

## Mechanism

1. Identify the duplicated immutable core of your many objects.
2. Front construction with a pool keyed by that core: first request builds,
   later requests share.
3. Keep everything per-occurrence *outside* the shared object.
4. Never mutate a flyweight — a shared instance mutated once is corrupted
   everywhere.

## The classic form, and what Python absorbs

The book's mechanism is a factory checking a pool — recognizable verbatim in
Python:

```python
class CardFactory:
    def __init__(self) -> None:
        self._pool: dict[tuple[str, str], Card] = {}

    def get(self, rank: str, suit: str) -> Card:
        key = (rank, suit)
        if key not in self._pool:  # check the pool...
            self._pool[key] = Card(rank, suit)
        return self._pool[key]  # ...share the instance
```

Python absorbs this twice over. `functools.lru_cache` on a plain factory
function *is* the pool. And the guide's `__new__` variant moves the pool
inside the class so `Card('9','♥') is Card('9','♥')` holds with plain
construction syntax — clever, but the sharing becomes invisible at the call
site, which is why the guide (and this unit) prefer the explicit factory:
[python-patterns.guide/gang-of-four/flyweight](https://python-patterns.guide/gang-of-four/flyweight/).

Most humbling: CPython already interns small integers and identifier-like
strings. Your duplicates may not exist — measure first.

## When to use it

- Profiling shows real memory pressure from many identical immutable values
  (glyph styles, map tiles, token metadata).
- Identity comparison (`is`) as a fast path is worth engineering for.

## When not to use it

- The objects are mutable — sharing mutable state is a bug generator, not an
  optimization.
- The population is small; a pool managing 52 cards saves nothing worth the
  indirection unless the *lesson* is the point.
- You haven't measured; interning by reflex is ceremony.

## Verdict: use with care

Great when profiling shows genuine duplication of immutable values;
pointless ceremony otherwise. Keep flyweights frozen — the pool's
`strict=True` guard exists because that rule gets broken quietly.
