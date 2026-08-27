# Abstract Factory — where it lives outside this repo

Cited, real implementations to study (or point an agent at) when designing or
reviewing family-of-factories code.

## Python standard library

- **`json.load(fp, parse_float=Decimal, parse_int=...)`.** The parser builds
  every number through the callables you hand it — the collapsed, pass-a-
  callable form of the pattern, straight from the stdlib. Swap `float` for
  `Decimal` and the whole document changes family.
  [docs.python.org/3/library/json.html](https://docs.python.org/3/library/json.html)
- **`unittest.mock`.** A factory for stand-ins of anything: patching swaps a
  whole family of collaborators for consistent doubles during a test.
  [docs.python.org/3/library/unittest.mock.html](https://docs.python.org/3/library/unittest.mock.html)

## Major ecosystems

- **Django database backends.** Each backend's `DatabaseWrapper` bundles a
  consistent family — creation, operations, introspection, client classes —
  so the ORM never names a vendor class. Swapping `ENGINE` swaps the family.
  [github.com/django/django/tree/main/django/db/backends](https://github.com/django/django/tree/main/django/db/backends)
- **SQLAlchemy dialects.** A dialect is a family of compiler, type, and
  execution classes that must agree with each other per database; the core
  programs against the dialect interface only.
  [docs.sqlalchemy.org/en/20/dialects/](https://docs.sqlalchemy.org/en/20/dialects/)

## The guide chapter

python-patterns.guide's treatment — why first-class callables dissolve the
class ceremony, and what a factory object is still for:
[python-patterns.guide/gang-of-four/abstract-factory/](https://python-patterns.guide/gang-of-four/abstract-factory/)

## What to notice across all of them

The bundle earns its place exactly when members must stay **consistent**
(Django's creation/introspection pair, a dialect's compiler/types). Where no
consistency is needed, real APIs pass callables individually (`parse_float=`).
When reviewing, ask which case you are in — the answer picks the shape.
