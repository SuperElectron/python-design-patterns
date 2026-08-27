---
id: behavioral/state
name: State
aliases: [state-machine, finite-state-machine]
guide_url: null
problem: "Change an object's behavior when its internal state changes, without an if-forest over a mode flag."
symptoms: ["mode flag with branches everywhere", "state machine", "turnstile/order lifecycle", "behavior depends on current phase"]
verdict: use-with-care
caveats:
  - "For small machines, an Enum plus a transition table beats a class per state — the whole machine fits on one screen."
  - "A generator is often the best state machine of all: the suspension point is the state, and the interpreter maintains it for you."
stdlib_sightings: [enum.Enum, generators]
---

# State

## Problem

A turnstile behaves differently locked vs unlocked; an order moves through a
lifecycle. Branching on a mode flag in every method scatters the machine
across the class.

## Naive solution

`naive.py` is the GoF form: a class per state, the context delegating to the
current state object, transitions swapping the object.

## Pythonic solution

Two idioms in `pythonic.py`: an `Enum` + transition-table machine (data, not
classes — the whole machine visible in one dict), and a **generator** machine
where the paused frame *is* the state.

## In the wild

Generators are the language's own state machines — every coroutine and every
`itertools`-style pipeline stage relies on frame suspension keeping state.
`real_world.py` shows a protocol scanner built on exactly that.

## Verdict

**Use with care.** Class-per-state pays off only for large machines with
state-specific data; tables and generators cover the rest.
