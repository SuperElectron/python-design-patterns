---
id: structural/flyweight
name: Flyweight
aliases: [interning, shared-instances]
guide_url: https://python-patterns.guide/gang-of-four/flyweight/
problem: "Support huge numbers of fine-grained objects by sharing immutable instances instead of duplicating them."
symptoms: ["millions of small objects", "memory pressure from duplicates", "interning", "shared immutable state"]
verdict: use-with-care
caveats:
  - "Flyweights must be immutable — a mutated shared instance corrupts every holder at once."
  - "The guide notes Python's twist: hide the sharing in the constructor via __new__, or expose it as a factory function; the factory is easier to reason about."
  - "Measure first: CPython already interns small ints and many strings, so your duplicates may not exist."
stdlib_sightings: [sys.intern, functools.lru_cache, int]
---

# Flyweight

## Problem

A text editor holds a million character objects; a card game deals thousands
of hands from 52 distinct cards. Building a fresh object per occurrence wastes
memory on identical state. Share one immutable instance per distinct value.

## Naive solution

`naive.py` uses the book's shape — a factory that checks a pool before
constructing — for playing cards: ask for `9♥` twice, get the same object.

## Pythonic solution

Two idiomatic forms in `pythonic.py`: a `functools.lru_cache`-decorated
factory (the pool is the cache), and the guide's `__new__` variant where the
class itself makes `Card(9, "♥") is Card(9, "♥")` true.

## In the wild

CPython interns small integers (`-5..256`) and identifier-like strings on its
own, and `sys.intern` lets you intern strings explicitly to speed up
comparisons — the interpreter running Flyweight underneath you.

## Verdict

**Use with care.** Great when profiling shows real duplication of immutable
values; pointless ceremony otherwise. Keep flyweights frozen.
