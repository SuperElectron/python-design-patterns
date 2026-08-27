---
id: structural/decorator
name: Decorator
aliases: [wrapper]
guide_url: https://python-patterns.guide/gang-of-four/decorator-pattern/
problem: "Add behavior around an object or callable without editing it or subclassing it."
symptoms: ["logging every call", "caching results", "retry wrapper", "timing calls", "add behavior without subclassing"]
verdict: pythonic
caveats:
  - "The GoF pattern (wrapping objects) and Python's @decorator syntax (wrapping callables) are cousins, not the same thing — this unit shows both."
  - "Always apply functools.wraps to function wrappers, or you destroy the wrapped function's name, docstring, and introspection."
  - "The guide's caveat: an object wrapper doesn't survive isinstance checks or identity comparisons — wrapping doesn't actually make you the wrapped thing."
stdlib_sightings: [functools.wraps, functools.lru_cache, contextlib.contextmanager]
---

# Decorator

## Problem

You want cross-cutting behavior — logging, caching, retries, access control —
around existing behavior, without editing the original and without a subclass
per combination.

## Naive solution

`naive.py` is the GoF object wrapper: a class that holds the wrapped object,
adds its twist, and forwards everything else. Faithful, and it carries the
book's real cost — you must forward *every* method, and the wrapper still
fails `isinstance` checks against the original.

## Pythonic solution

For callables, the language absorbed the pattern into `@decorator` syntax.
`pythonic.py` builds a proper function decorator (with `functools.wraps`) and
a parameterized one — the three-layer form that trips everyone up once.

## In the wild

`functools.lru_cache` is a decorator adding caching; `functools.wraps` is a
decorator that fixes decorators; `contextlib.contextmanager` turns a generator
into a context manager. You use this pattern daily whether you notice or not.

## Verdict

**Pythonic** — for callables, idiomatically so. GoF-style object wrapping is
rarer; when you need it, `__getattr__` forwarding (shown in `naive.py`) keeps
it tolerable.
