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

## Problem

Callers want to walk a collection's elements — possibly lazily, possibly in a
custom order — without coupling to its storage. The GoF answer is a separate
cursor object with a "give me the next one" method.

## Naive solution

`naive.py` implements the protocol by hand, the way the guide teaches it:
an iterable whose `__iter__` returns a fresh iterator object, and an iterator
with `__next__` (raising `StopIteration`) plus `__iter__` returning itself so
it can be used directly in a `for` loop.

## Pythonic solution

Python absorbed this pattern deeper than any other — `for`, unpacking, and
comprehensions all speak the protocol natively, and **generators** write the
iterator for you: a function with `yield` returns an object implementing
`__iter__` and `__next__` correctly, with all cursor state kept in the frame.
`pythonic.py` re-does `naive.py` in a fraction of the code.

## In the wild

`itertools` is an entire stdlib module of composable iterators; files iterate
by line; `dict` yields keys. `real_world.py` composes `itertools.islice` and
`itertools.count` into a lazy, infinite-but-bounded pipeline.

## Verdict

**Pythonic.** Know the manual protocol (it's the machinery underneath), write
generators in practice.
