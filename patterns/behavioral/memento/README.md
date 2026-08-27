---
id: behavioral/memento
name: Memento
aliases: [snapshot, undo-token]
guide_url: null
problem: "Capture an object's state so it can be restored later, without exposing its internals."
symptoms: ["undo", "checkpoint and rollback", "save game", "restore previous state"]
verdict: use-with-care
caveats:
  - "Immutable state makes the pattern nearly free: a snapshot is just keeping the old object. Design the state to be frozen and mementos fall out."
  - "pickle.loads executes code while deserializing — only unpickle snapshots your own process produced; use JSON for anything crossing a trust boundary."
  - "Deep-copying big mutable graphs per keystroke is the naive cost; snapshot the smallest state that matters."
stdlib_sightings: [copy.deepcopy, pickle.dumps, dataclasses.replace]
---

# Memento

## Problem

An editor needs undo; a migration needs rollback. Something outside the
object must hold "how it was" without being allowed to poke around inside.

## Naive solution

`naive.py` is the GoF trio: Originator produces opaque mementos, a
Caretaker stacks them, restore hands one back. The memento's fields are
private by convention — Python has no way to truly seal them.

## Pythonic solution

Make the state an immutable dataclass and the whole pattern collapses:
a snapshot *is* the current state object, history is a list of them, undo is
popping. `dataclasses.replace` produces each next state.

## In the wild

`pickle.dumps` is a memento serializer: the bytes are an opaque snapshot
restorable with `loads`, even in another process. `copy.deepcopy` is the
in-memory equivalent for mutable state you can't freeze.

## Verdict

**Use with care** — and tilt the design toward immutable state, where the
pattern costs nothing.
