# Sentinel Object — where it lives outside this repo

Cited, real implementations to study (or point an agent at) when designing or
reviewing absence-handling code.

## Python standard library

- **`dataclasses.MISSING`.** The stdlib's public missing-marker: it lets
  introspection distinguish "no default" from "default is None".
  [docs.python.org/3/library/dataclasses.html](https://docs.python.org/3/library/dataclasses.html)
- **`inspect.Parameter.empty`.** The sentinel for "no default / no
  annotation" in signature introspection.
  [docs.python.org/3/library/inspect.html](https://docs.python.org/3/library/inspect.html)
- **`unittest.mock.sentinel` and `mock.DEFAULT`.** Named sentinels offered
  *as* API — mint-a-marker as a service.
  [docs.python.org/3/library/unittest.mock.html](https://docs.python.org/3/library/unittest.mock.html)
- **Two-argument `iter(callable, sentinel)`.** A sentinel baked into a
  builtin's signature: iteration stops when the sentinel appears.
  [docs.python.org/3/library/functions.html#iter](https://docs.python.org/3/library/functions.html#iter)
- **`str.find`'s `-1`.** The cautionary in-band sentinel *value* — legal
  integer, silently consumable by arithmetic.

## Language evolution

- **PEP 661 — Sentinel Values.** The problem is real enough to have a PEP:
  naming, repr, and copy/pickle semantics for sentinels.
  [peps.python.org/pep-0661](https://peps.python.org/pep-0661/)
- **The guide chapter** — sentinel values vs the sentinel object vs the Null
  Object, with history.
  [python-patterns.guide/python/sentinel-object](https://python-patterns.guide/python/sentinel-object/)

## What to notice across all of them

The healthy examples are all **out-of-band** (a fresh object no domain can
produce) and **named** (debuggable). The stdlib's one in-band survivor,
`str.find`, is the pattern's standing warning label.
