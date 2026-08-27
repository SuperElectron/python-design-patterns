---
id: behavioral/chain_of_responsibility
name: Chain of Responsibility
aliases: [chain, handler-chain]
guide_url: null
problem: "Pass a request along a line of handlers until one of them takes it."
symptoms: ["escalation levels", "middleware chain", "first handler that can, does", "fallback handlers"]
verdict: prefer-alternative
caveats:
  - "In Python the chain is a list of callables and a loop — successor pointers threaded through objects add nothing but pointer bookkeeping."
  - "Decide up front what an unhandled request means (exception? default?) — the GoF pattern is silent about falling off the end."
stdlib_sightings: [logging propagation, urllib.request opener chain]
---

# Chain of Responsibility

## Problem

A support ticket should be handled by the first tier able to deal with it;
an HTTP request passes middleware until something produces a response. The
sender must not know which handler will answer.

## Naive solution

`naive.py` threads successor pointers through handler objects, GoF-style:
each handler either handles or forwards to `self.successor`.

## Pythonic solution

A chain is a *list of callables* tried in order — the first non-`None` answer
wins. Registration is appending; reordering is list surgery; the
fell-off-the-end case is explicit. That's the whole pattern.

## In the wild

`logging` propagation is a chain: a record climbs the logger hierarchy,
offered to each logger's handlers on the way up. `urllib.request` passes
requests through its chain of openers/handlers until one claims the scheme.

## Verdict

**Prefer an alternative:** a list and a loop. Objects with successor
pointers, only if handlers already are stateful objects.
