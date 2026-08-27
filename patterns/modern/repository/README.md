---
id: modern/repository
name: Repository
aliases: [data-access-layer, persistence-port]
guide_url: null
problem: "Keep domain logic ignorant of how objects are stored, behind a collection-like interface."
symptoms: ["SQL scattered through business logic", "tests need a database", "swap sqlite for postgres", "collection-like storage API"]
verdict: use-with-care
caveats:
  - "The payoff is the in-memory fake: if your tests still hit a database, the repository isn't earning its keep."
  - "Don't build a generic Repository[T] for one entity — write the three methods you need and stop."
stdlib_sightings: [sqlite3, shelve]
---

# Repository

## Problem

Pricing rules shouldn't know SQL. When persistence details soak into domain
logic, every business test drags a database behind it and every storage
change touches everything.

## Naive solution

`naive.py` inlines sqlite calls in the domain function — compact, and
welded shut.

## Pythonic solution

A `Protocol` names the collection-like operations the domain needs (`add`,
`get`, `list`); an in-memory dict repo serves tests, a sqlite repo serves
production, and the domain function accepts either.

## In the wild

`shelve` is a ready-made key-object repository over `dbm`; `sqlite3` with a
thin class over it is the standard hand-rolled form (shown in
`real_world.py`).

## Verdict

**Use with care.** Earn it with a real second implementation (the in-memory
fake counts); skip it for scripts that just need a query.
