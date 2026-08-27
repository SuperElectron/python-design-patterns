---
id: structural/proxy
name: Proxy
aliases: [surrogate, virtual-proxy, protection-proxy]
guide_url: null
problem: "Stand in for another object to control access to it — deferring, guarding, or instrumenting the real thing."
symptoms: ["lazy expensive construction", "access control around an object", "remote object stand-in", "count or log attribute access"]
verdict: use-with-care
caveats:
  - "A proxy is not the object: isinstance checks, identity comparisons, and dunder lookups (which bypass __getattr__) all see through the disguise."
  - "For 'compute this attribute lazily once', functools.cached_property is the pattern at the right size — no proxy class needed."
stdlib_sightings: [weakref.proxy, functools.cached_property, unittest.mock.Mock]
---

# Proxy

## Problem

You want the *interface* of an object but not (yet, or not directly) the
object: constructing it is expensive, touching it needs a permission check,
or you want to observe every access.

## Naive solution

`naive.py` is the GoF virtual proxy: same interface as the real subject,
constructing it only on first use.

## Pythonic solution

`__getattr__` builds a generic lazy proxy in a dozen lines — no shared
interface needed, any attribute access triggers construction and then
forwards. And when the real goal is one lazily-computed attribute,
`functools.cached_property` replaces the whole apparatus.

## In the wild

`weakref.proxy` returns an object that forwards everything to its referent
without keeping it alive — and raises once the referent is gone.
`unittest.mock.Mock` is a proxy you interrogate afterwards.

## Verdict

**Use with care.** Powerful where laziness or mediation is real; remember the
disguise is skin-deep (identity, isinstance, dunders).
