---
id: creational/singleton
name: Singleton
aliases: [single-instance]
guide_url: https://python-patterns.guide/gang-of-four/singleton/
problem: "Guarantee a class has exactly one instance and give the whole program access to it."
symptoms: ["shared config object", "one connection pool", "global registry", "only one instance"]
verdict: prefer-alternative
caveats:
  - "You almost always want the Global Object pattern instead: build the instance at import time in a module and import it."
  - "Singleton classes make tests order-dependent — state leaks between tests through the hidden instance."
  - "The GoF __new__ dance still runs __init__ on every call in Python; a factory function avoids the trap entirely."
stdlib_sightings: [None, Ellipsis, NotImplemented]
---

# Singleton

## Problem

Some resources must exist exactly once: a configuration object, a connection
pool, a process-wide registry. The Gang of Four answer is a class that
intercepts construction and always hands back the same instance.

## Naive solution

`naive.py` is the classic implementation: override `__new__`, cache the
instance on the class. It works, but note what Python forces on you — callers
still *look* like they're constructing (`Logger()`), `__init__` re-runs on
every call unless you guard it, and subclassing gets weird fast.

## Pythonic solution

Python already has singletons: **modules**. A module is created once, cached in
`sys.modules`, and every `import` returns the same object. `pythonic.py` shows
the Global Object pattern — instantiate a plain class once at module level (or
lazily behind a function) and import that. No metaclass, no `__new__`, nothing
to explain in review.

## In the wild

`None`, `Ellipsis`, and `NotImplemented` are the interpreter's own singletons —
that's why `is` comparison against them is correct. Every imported module is
one too: `real_world.py` proves it.

## Verdict

**Prefer an alternative.** The naive form exists here for study; if you're
reaching for it, write a module-level instance instead. The exceptions are rare
enough that you'll know them when you hit them (lazy construction that must be
thread-safe, C-extension interop).
