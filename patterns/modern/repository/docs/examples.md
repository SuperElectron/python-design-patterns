# Repository — where it lives outside this repo

Cited, real implementations to study (or point an agent at) when designing or
reviewing repository-shaped code.

## Canonical references

- **Fowler, PoEAA — Repository.** The original catalog entry: a
  collection-like interface mediating between domain and data mapping.
  [martinfowler.com/eaaCatalog/repository.html](https://martinfowler.com/eaaCatalog/repository.html)
- **Percival & Gregory, *Architecture Patterns with Python*, ch. 2.** The
  canonical Python worked example — `AbstractRepository`, a fake, SQLAlchemy
  adapter, and the argument for contract tests. This unit is that chapter
  in miniature, with `Protocol` instead of an ABC.
  [cosmicpython.com/book/chapter_02_repository.html](https://www.cosmicpython.com/book/chapter_02_repository.html)

## Python standard library

- **`sqlite3`.** The stdlib backend a real adapter wraps — the mini-project's
  `SqliteInvoices` is the standard hand-rolled form.
  [docs.python.org/3/library/sqlite3.html](https://docs.python.org/3/library/sqlite3.html)
- **`shelve`.** A ready-made key→object repository over `dbm`: the smallest
  possible repository surface (`__getitem__`/`__setitem__`), useful for
  calibrating how little a port can be.
  [docs.python.org/3/library/shelve.html](https://docs.python.org/3/library/shelve.html)

## Major ecosystems — and a contrast

- **Django `Manager`/`QuerySet`.** The *active-record* flavor: storage API
  attached to the model class itself (`Invoice.objects.filter(...)`).
  Convenient, and exactly what repository is **not** — the domain type and
  the query surface are welded together, so there is no port to fake.
  Knowing the difference is most of knowing when you need this pattern.
  [docs.djangoproject.com/en/stable/topics/db/managers/](https://docs.djangoproject.com/en/stable/topics/db/managers/)
- **SQLAlchemy `Session`.** The data-mapper half the pattern assumes: domain
  objects stay plain, the session maps them — a repository is a thin,
  domain-vocabulary port over it.
  [docs.sqlalchemy.org/en/latest/orm/session_basics.html](https://docs.sqlalchemy.org/en/latest/orm/session_basics.html)

## What to notice across all of them

The dividing line is always *who owns the interface*: repository puts the
domain in charge of a small port; active record puts the framework in charge
of a wide one. When reviewing, ask for the fake — if an in-memory
implementation would be laborious to write, the port has grown past the
domain's actual needs.
