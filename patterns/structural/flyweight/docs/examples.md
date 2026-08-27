# Flyweight — where it lives outside this repo

Cited, real implementations to study (or point an agent at) when designing or
reviewing sharing/interning code.

## Python standard library

- **`sys.intern`.** Explicit string interning: one shared copy, pointer-fast
  equality. The docs call out dictionary keys as the winning case.
  [docs.python.org/3/library/sys.html#sys.intern](https://docs.python.org/3/library/sys.html#sys.intern)
- **CPython small-int interning.** Integers −5..256 are pre-built singletons;
  the interpreter runs the pattern under you, which is why careless `is` checks
  on small ints "work" and then betray you at 257.
  [docs.python.org/3/c-api/long.html](https://docs.python.org/3/c-api/long.html)
- **`functools.lru_cache`.** A memoizing decorator that, applied to a
  factory, *is* the flyweight pool — the guide chapter's own recommendation.
  [docs.python.org/3/library/functools.html#functools.lru_cache](https://docs.python.org/3/library/functools.html#functools.lru_cache)

## Major ecosystems

- **spaCy `StringStore`.** Interns every vocabulary string to a 64-bit hash
  so tokens across a corpus share one copy — flyweight at NLP scale.
  [spacy.io/api/stringstore](https://spacy.io/api/stringstore)
- **Apache Arrow dictionary arrays** (pandas `Categorical`). Column-scale
  value sharing: each distinct value stored once, rows hold small indices.
  [arrow.apache.org/docs/python/data.html#dictionary-arrays](https://arrow.apache.org/docs/python/data.html#dictionary-arrays)

## What to notice across all of them

Every production flyweight shares only **immutable** values, and none of
them expose the pooled object for mutation. And each one earned its place
with a measurement — interning pays at corpus/column scale, not at 52 cards.
