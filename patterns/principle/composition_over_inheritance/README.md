---
id: principle/composition_over_inheritance
name: Composition Over Inheritance
aliases: [subclass-explosion, favor-composition]
guide_url: https://python-patterns.guide/gang-of-four/composition-over-inheritance/
problem: "Vary independent behaviors without one subclass per combination of them."
symptoms: ["subclass explosion", "FilteredSocketLogger-style names", "M x N class combinations", "mixin soup"]
verdict: pythonic
caveats:
  - "Multiple inheritance, mixins, and dynamically built classes are the guide's 'dodges' — they postpone the explosion instead of ending it."
  - "Each independent axis of variation should become its own small object, injected where needed."
stdlib_sightings: [logging.Logger, logging.Handler, logging.Filter]
---

# Composition Over Inheritance

## Problem

A logger can filter messages and can write to a file or a socket. With
inheritance, every combination costs a class: `FilteredLogger`,
`SocketLogger`, `FilteredSocketLogger`… M filters × N destinations = M×N
classes. This is the guide's opening case study.

## Naive solution

`naive.py` builds exactly that explosion, three classes deep, so you can
watch the combinatorics happen.

## Pythonic solution

Split each axis into its own object — filters decide, handlers write — and
*compose* them in one logger. M + N small classes cover all M × N behaviors,
and new combinations are constructor arguments, not new classes.

## In the wild

The stdlib `logging` module is this principle shipped at scale: `Logger`
composes `Handler`s, `Filter`s, and `Formatter`s, and no class named
`FilteredRotatingSyslogLogger` needs to exist.

## Verdict

**Pythonic** — and the single most load-bearing idea behind the other
patterns in this catalog.
