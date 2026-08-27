---
id: structural/composite
name: Composite
aliases: [tree, part-whole]
guide_url: https://python-patterns.guide/gang-of-four/composite/
problem: "Let callers treat a single object and a whole tree of objects through one interface."
symptoms: ["tree structure", "files and directories", "nested groups", "recursive totals", "uniform leaf and container API"]
verdict: pythonic
caveats:
  - "Don't force leaves to carry child-management methods (add/remove) just to match the container — the guide sides with interface honesty over uniformity."
  - "With duck typing you don't need a shared base class at all; share one only when it earns its keep."
stdlib_sightings: [pathlib.Path, xml.etree.ElementTree.Element]
---

# Composite

## Problem

File systems, GUI widget trees, org charts: structures where a container holds
items that may themselves be containers, and callers want one operation —
size, render, total — that works on any node without asking which kind it is.

## Naive solution

`naive.py` mirrors the book: an abstract `Graphic` component, a `Circle` leaf,
and a `Group` composite whose operation recurses over its children. Note the
book's contested move — putting `add`/`remove` on the *component* interface so
leaves must refuse them at runtime.

## Pythonic solution

Duck typing removes the need for the abstract base: a leaf and a container
that both offer `total()` are already substitutable. `pythonic.py` keeps a
`Protocol` for the type checker only, and leaves child management where it
honestly belongs — on the container.

## In the wild

`pathlib.Path` is the classic: files and directories share one interface, and
`iterdir()`/`rglob()` recurse the composite. `xml.etree.ElementTree.Element`
is a composite of elements all the way down.

## Verdict

**Pythonic.** Trees are everywhere and this is the right shape for them; just
keep the leaf's interface honest.
