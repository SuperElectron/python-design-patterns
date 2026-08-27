---
id: behavioral/strategy
name: Strategy
aliases: [policy]
guide_url: null
problem: "Make an algorithm interchangeable at runtime without the caller knowing which variant it got."
symptoms: ["swap algorithm at runtime", "pricing rules", "pluggable policy", "if/elif chain choosing behavior"]
verdict: prefer-alternative
caveats:
  - "In Python a strategy is just a function passed as an argument — the class-per-algorithm hierarchy is Java's workaround for lacking first-class functions."
  - "Reach for the class form only when a strategy carries its own state or several related methods."
stdlib_sightings: [sorted, list.sort, functools.cmp_to_key]
---

# Strategy

## Problem

A checkout applies one of several promotion rules; a sorter orders by one of
several keys. The algorithm must vary independently of the code that uses it.

## Naive solution

`naive.py` is the book's shape: a `Promotion` interface, one class per
algorithm, and a context object holding the chosen strategy. (Fluent Python
fans will recognize the running example.)

## Pythonic solution

Functions *are* strategies. `pythonic.py` passes plain functions, and adds the
decorator-registry twist: `@promotion` collects every rule into a list so
`best_promo` can try them all — new rules register themselves by existing.
This also fixes the legacy repo's bug, where a misplaced `return` inside the
loop made `bulk_item` score only the first cart line.

## In the wild

`sorted(data, key=...)` is the Strategy pattern as an argument: the key
function is an interchangeable ordering algorithm, and `functools.cmp_to_key`
adapts old-style comparator strategies into key strategies.

## Verdict

**Prefer an alternative** — the alternative being a plain function. The
pattern's *intent* is everywhere in Python; the class ceremony almost never is.
