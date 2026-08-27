---
id: structural/bridge
name: Bridge
aliases: [abstraction-implementor]
guide_url: null
problem: "Let an abstraction and its implementation vary independently, instead of multiplying subclasses across both axes."
symptoms: ["two hierarchies multiplying", "shapes times renderers", "device times remote", "backend swappable under a stable front"]
verdict: prefer-alternative
caveats:
  - "In Python the Bridge collapses into ordinary composition with dependency injection — hold the implementor as an attribute, pass it in."
  - "The pattern's real lesson survives: name the two axes, give each its own small hierarchy (or set of callables), and connect them with one reference."
stdlib_sightings: [logging.Logger with logging.Handler]
---

# Bridge

## Problem

Shapes (circle, square) need rendering backends (vector, raster). Inheriting
`VectorCircle`, `RasterCircle`, `VectorSquare`… multiplies the two axes into
one hierarchy — the same explosion Composition-Over-Inheritance warns about,
seen from the structural side.

## Naive solution

`naive.py` is the book's shape: an abstraction hierarchy (`Shape`) holding a
reference to an implementor hierarchy (`Renderer`), each extensible without
touching the other.

## Pythonic solution

Strip the ceremony and the Bridge is *composition with an injected
dependency* — which is why the verdict points there. `pythonic.py` keeps the
two axes but needs no abstract bases: the renderer is a `Protocol`, shapes
are dataclasses holding one.

## In the wild

`logging` is a Bridge you already use: `Logger` (the abstraction callers see)
delegates to interchangeable `Handler` implementations, and both sides grow
independently.

## Verdict

**Prefer an alternative** — plain composition/DI *is* the bridge. Keep the
lesson (name your axes), skip the taxonomy.
