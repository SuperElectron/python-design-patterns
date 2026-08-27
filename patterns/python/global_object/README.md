---
id: python/global_object
name: Global Object
aliases: [module-global, constant-pattern]
guide_url: https://python-patterns.guide/python/module-globals/
problem: "Give a whole program shared access to a constant or a pre-built object by assigning it at module level."
symptoms: ["shared constants", "one shared instance", "config everyone imports", "what Singleton actually wants to be"]
verdict: use-with-care
caveats:
  - "Mutable globals couple everything that touches them and make tests order-dependent — prefer constants, or objects whose mutation is their documented job (like os.environ)."
  - "Never do I/O at import time: importing must be cheap and safe, or every consumer pays (and test runs touch the network/disk)."
stdlib_sightings: [os.environ, calendar.day_name, math.pi]
---

# Global Object

## Problem

Many parts of a program need the same value — a constant table, a compiled
regex, a configured client. Passing it through every call chain is noise;
building it repeatedly is waste.

## Naive solution

`naive.py` shows the two classic misuses: hidden *mutable* module state that
couples callers together, and import-time I/O that makes `import` slow,
fragile, and untestable.

## Pythonic solution

`pythonic.py` shows the pattern done well: immutable constants computed at
import time (cheap, deterministic), a pre-built global object whose
construction is pure, and lazy initialization for anything expensive —
so importing the module never costs more than defining functions.

## In the wild

`math.pi` is the Constant Pattern; `calendar.day_name` is an import-time
computed global object; `os.environ` is the rare *documented* mutable global,
mutation being its entire purpose.

## Verdict

**Use with care.** Constants and immutable pre-built objects: freely. Mutable
globals: only when shared mutation is the feature, not an accident.
