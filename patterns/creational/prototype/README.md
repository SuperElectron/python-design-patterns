---
id: creational/prototype
name: Prototype
aliases: [clone]
guide_url: https://python-patterns.guide/gang-of-four/prototype/
problem: "Create new objects by copying a pre-configured exemplar instead of constructing from scratch."
symptoms: ["expensive construction", "objects that start from a template", "registry of preconfigured instances", "clone this object"]
verdict: prefer-alternative
caveats:
  - "The pattern targets a 1990s problem: languages where classes weren't first-class values. In Python you just pass the class, or a functools.partial, or a bound copy call."
  - "If you do copy, know your depth: copy.copy shares nested mutable state; copy.deepcopy does not."
stdlib_sightings: [copy.copy, copy.deepcopy, functools.partial]
---

# Prototype

## Problem

A framework needs to stamp out new objects without knowing how to construct
them — the classic case is a menu of pre-configured instances the user picks
from. The GoF answer: store an exemplar ("prototype") and `clone()` it.

## Naive solution

`naive.py` follows the book: an abstract `clone()` method, concrete prototypes,
and a registry mapping names to exemplars that get cloned on demand.

## Pythonic solution

Python doesn't need the interface, because *callables* are the interface. A
registry can hold classes, `functools.partial` objects pre-loading the
arguments, or bound methods — anything you can call to get a fresh instance.
`pythonic.py` shows the guide's recommendation: a registry of zero-argument
factories.

## In the wild

`copy.copy` and `copy.deepcopy` are the stdlib's clone operation, complete
with the `__copy__`/`__deepcopy__` protocol for classes that need custom
cloning — that protocol *is* the Prototype pattern, absorbed into the language.

## Verdict

**Prefer an alternative.** Store callables, not exemplars. Reach for
`copy.deepcopy` only when instances are genuinely expensive or awkward to
rebuild from arguments.
