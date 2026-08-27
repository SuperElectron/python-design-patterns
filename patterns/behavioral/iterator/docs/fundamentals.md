# Iterator — fundamentals

## Intent

Traverse a collection's elements — possibly lazily, possibly remote —
without exposing how the collection stores them. Callers say "next";
the cursor's bookkeeping is someone else's problem.

## Participants

| Role | Classic (GoF) form | Python form |
|---|---|---|
| Iterator | An object with `next()`/`done()` | Anything with `__next__` — in practice, a generator's frame |
| Concrete iterator | A class holding cursor state | The paused generator frame holds it for free |
| Aggregate | `createIterator()` factory method | `__iter__`, usually written *as* a generator |
| Client | Calls `next()` in a loop | `for`, comprehensions, unpacking — the protocol is the language |

## Mechanism

1. The iterable's `__iter__` returns a fresh iterator (so two loops don't
   share a cursor).
2. The iterator's `__next__` returns items and raises `StopIteration` when
   done; its own `__iter__` returns itself.
3. A generator function implements all of it: each `yield` suspends the
   frame, and the frame *is* the cursor state.

## The classic form, and what Python absorbs

The protocol implemented by hand, the way the guide teaches it:

```python
from __future__ import annotations  # OddIterator is named before it exists


class OddNumbers:  # the aggregate
    def __init__(self, maximum: int) -> None:
        self.maximum = maximum

    def __iter__(self) -> OddIterator:
        return OddIterator(self)  # fresh cursor per loop


class OddIterator:  # the cursor object
    def __init__(self, container: OddNumbers) -> None:
        self.container = container
        self.n = -1  # cursor state, managed by hand

    def __next__(self) -> int:
        self.n += 2
        if self.n > self.container.maximum:
            raise StopIteration
        return self.n

    def __iter__(self) -> OddIterator:
        return self
```

Python absorbed this pattern deeper than any other. The same behavior as a
generator is four lines — the cursor class vanishes into the paused frame:

```python
from collections.abc import Iterator


def odd_numbers(maximum: int) -> Iterator[int]:
    n = 1
    while n <= maximum:
        yield n
        n += 2
```

What survives as a *design* move is hiding a non-trivial traversal (pages,
cursors, chunked reads) behind one generator — this module's
[`iterate_pages`](../pattern/paging.py).

## When to use it

- Custom or lazy traversal over your own types: write `__iter__` as a
  generator.
- Chunked/remote sources (paginated APIs, cursored queries): expose one
  generator; keep pages out of caller code.

## When not to use it

- Hand-writing `__next__` — a generator implements the protocol correctly
  for you; the manual form is for understanding, not production.
- Materializing everything into a list "to be safe" — you just deleted the
  laziness that justified the pattern.

## Verdict: pythonic

The pattern is the language. Know the manual protocol (it is the machinery
underneath); write generators in practice. Guide chapter:
[python-patterns.guide/gang-of-four/iterator/](https://python-patterns.guide/gang-of-four/iterator/)
