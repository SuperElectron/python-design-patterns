---
id: behavioral/command
name: Command
aliases: [action, transaction]
guide_url: null
problem: "Package a request as an object so it can be queued, logged, undone, or executed later by code that doesn't know its details."
symptoms: ["undo/redo", "task queue", "macro recording", "button callbacks", "audit log of operations"]
verdict: use-with-care
caveats:
  - "If you only need 'execute later', a plain callable or functools.partial is the whole pattern — don't build a class hierarchy for a deferred call."
  - "The class form earns its keep exactly when commands carry extra behavior: undo(), serialization, or metadata."
stdlib_sightings: [functools.partial, sched.scheduler, unittest.mock.call]
---

# Command

## Problem

A menu button, a job queue, or an undo stack must trigger operations without
knowing what they do. Reify the request: an object carrying everything needed
to perform (and possibly reverse) it.

## Naive solution

`naive.py` is the classic remote-control shape: a `Command` interface with
`execute`/`undo`, concrete commands closing over a receiver, and an invoker
that runs them and keeps a history for undo.

## Pythonic solution

Functions are first-class, so *a command is just a callable*. `pythonic.py`
queues `functools.partial` objects for the execute-only case, and uses a pair
of callables (do, undo) where reversibility matters — no interface, no
hierarchy.

## In the wild

Every callback API is the Command pattern: `sched.scheduler.enter` takes the
action as a callable, Tkinter buttons take `command=`, `atexit.register`
queues commands to run at shutdown.

## Verdict

**Use with care.** Callables for deferral, the class form only once commands
need undo, serialization, or introspection beyond "run me".
