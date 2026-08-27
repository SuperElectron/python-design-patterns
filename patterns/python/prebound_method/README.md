---
id: python/prebound_method
name: Prebound Method
aliases: [bound-method-global]
guide_url: https://python-patterns.guide/python/prebound-methods/
problem: "Offer module-level functions that share state, by binding the methods of one hidden instance to module globals."
symptoms: ["module-level API over shared state", "random.random-style interface", "convenience functions plus an instantiable class"]
verdict: pythonic
caveats:
  - "Build the hidden instance cheaply and without I/O — it is constructed at import time."
  - "Keep the class public too, so users needing isolated state can instantiate their own (exactly as random.Random allows)."
stdlib_sightings: [random.random, random.seed, secrets.token_hex]
---

# Prebound Method

## Problem

You want the ergonomic module-level API — `random.random()`, not
`random.get_default_generator().random()` — but the functions must share
state (a seed, a counter, a connection).

## Naive solution

`naive.py` shows the alternatives the guide rejects: bare module functions
mutating a loose module global (state and behavior drift apart), or making
every caller instantiate the class themselves (ergonomics lost).

## Pythonic solution

Define a normal class, build **one instance** at module level, then assign
its bound methods to module-global names: `roll = _instance.roll`. Callers
get plain functions; the instance travels along inside each bound method.

## In the wild

`random.random`, `random.seed`, and friends are exactly this — bound methods
of a hidden `random.Random()` built at import; `random.Random` stays public
for anyone needing isolated streams.

## Verdict

**Pythonic.** The stdlib's own favorite way to put a friendly face on shared
state.
