---
id: modern/context_manager
name: Context Manager
aliases: [with-statement, RAII, resource-management]
guide_url: null
problem: "Guarantee acquire/release pairing around a block of code, even when it raises."
symptoms: ["forgot to close", "cleanup on exception", "try/finally everywhere", "temporary state that must be restored"]
verdict: pythonic
caveats:
  - "@contextlib.contextmanager wants the yield inside try/finally — without it, an exception in the body skips your cleanup."
  - "Returning True from __exit__ swallows the exception; do it only on purpose."
stdlib_sightings: [open, contextlib.contextmanager, contextlib.ExitStack, tempfile.TemporaryDirectory]
---

# Context Manager

## Problem

Every acquired resource — file, lock, connection, temporary state — must be
released on *every* exit path. Hand-written `try/finally` scattered through a
codebase is where cleanup bugs live.

## Naive solution

`naive.py` is the try/finally discipline done by hand, including the nested
two-resource version that shows why it doesn't scale.

## Pythonic solution

The `with` statement makes the pairing structural: `pythonic.py` implements
the protocol both ways — a class with `__enter__`/`__exit__`, and the
generator form via `@contextmanager` where the `yield` splits acquire from
release.

## In the wild

`open`, locks, and sqlite transactions are all context managers;
`contextlib.ExitStack` manages a *dynamic* number of them, unwinding in
reverse on the way out — shown in `real_world.py`.

## Verdict

**Pythonic.** Python's own RAII; any acquire/release pair you write twice
deserves one.
