---
id: python/sentinel_object
name: Sentinel Object
aliases: [sentinel, missing-marker, null-object]
guide_url: https://python-patterns.guide/python/sentinel-object/
problem: "Mark 'no value here' unambiguously when None itself is a legitimate value."
symptoms: ["None is a valid value", "distinguish missing from null", "default argument that could be None", "str.find returns -1"]
verdict: pythonic
caveats:
  - "A sentinel must be compared with `is`, never `==` — its identity is its meaning."
  - "Sentinel *values* like -1 (str.find) live inside the value's own type and eventually collide; a fresh object() cannot."
  - "Fowler's Null Object pattern — a do-nothing stand-in with real methods — is the neighboring cure when callers would otherwise be littered with None checks."
stdlib_sightings: [dataclasses.MISSING, iter(callable, sentinel), str.find]
---

# Sentinel Object

## Problem

A cache stores `None` as a legitimate value; a keyword argument treats `None`
as meaningful. Now "the value is None" and "there is no value" collide, and
`get(...) or default` bugs follow.

## Naive solution

`naive.py` shows both classic failures: the in-band sentinel *value*
(`str.find`-style `-1` that arithmetic happily consumes), and `None`-as-missing
in a cache that stores `None`.

## Pythonic solution

A fresh `_MISSING = object()` is unforgeable: it lives in no domain, equals
nothing but itself, and is checked by identity. `pythonic.py` uses it for a
cache and a default argument, and includes a small Null Object — a real
do-nothing logger — for the case where callers shouldn't branch at all.

## In the wild

`dataclasses.MISSING` distinguishes "no default" from "default is None";
two-argument `iter(read, b"")` takes an explicit sentinel that terminates
iteration; `str.find`'s `-1` survives as a cautionary in-band sentinel value.

## Verdict

**Pythonic.** One module-private `object()` per meaning, compared with `is`.
