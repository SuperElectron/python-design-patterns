---
id: creational/abstract_factory
name: Abstract Factory
aliases: [kit, factory-of-factories]
guide_url: https://python-patterns.guide/gang-of-four/abstract-factory/
problem: "Let code build families of related objects without naming their concrete classes."
symptoms: ["swap whole family of implementations", "test doubles for created objects", "library must not hardcode which class it builds"]
verdict: prefer-alternative
caveats:
  - "The pattern exists because 1990s languages could not pass classes or functions as values — Python can, so a factory is usually just a callable argument."
  - "Reach for a factory *object* only when the family of factories is large enough that bundling them beats passing them individually."
stdlib_sightings: [json.load parse_float, decimal.Decimal, unittest.mock]
---

# Abstract Factory

## Problem

A JSON parser must build numbers, but which number type — `float`?
`Decimal`? The parsing code shouldn't hardcode the class, and callers should
be able to swap the whole family of built objects (numbers, lists, maps) at
once.

## Naive solution

`naive.py` is the book's shape: an abstract factory interface, one concrete
factory per family, and client code programmed against the interface.

## Pythonic solution

Classes and functions are first-class, so the guide's advice is: accept
*callables*. `pythonic.py` passes `Decimal` itself as the number factory; the
"complete" factory bundling several builders is just a small dataclass of
callables — no abstract base required.

## In the wild

`json.load(fp, parse_float=Decimal)` is the exact pattern: the stdlib parser
accepts factory callables for every family member it builds. `unittest.mock`
is a factory for stand-ins of anything.

## Verdict

**Prefer an alternative:** pass callables. Bundle them in an object only when
the family is genuinely large.
