---
id: modern/dependency_injection
name: Dependency Injection
aliases: [DI, constructor-injection, inversion-of-control]
guide_url: null
problem: "Hand an object its collaborators instead of letting it construct them, so they can be swapped — above all in tests."
symptoms: ["can't test without the real database", "class news up its own client", "mock the clock", "swap implementation per environment"]
verdict: pythonic
caveats:
  - "In Python DI needs no framework: a keyword argument with a production default is the entire mechanism."
  - "Inject at the boundary that varies (clock, storage, transport) — injecting everything turns constructors into wiring diagrams."
stdlib_sightings: [json.dumps cls=, sorted key=, unittest.mock]
---

# Dependency Injection

## Problem

A class that builds its own collaborators — its clock, its store, its HTTP
client — can only ever be tested with the real things. The hidden `new` is
the coupling.

## Naive solution

`naive.py` hard-wires `datetime.now` and a concrete store inside the class.
Watch the test problem appear: the greeting depends on the actual wall
clock.

## Pythonic solution

Pass the collaborators in. `pythonic.py` is an overdue-invoice reminder
service with three seams — the clock, the invoice source, the mail transport —
each a `Protocol` or callable with a production default. Tests hand in a
frozen date and a capturing mailbox and become fully deterministic. No
container, no framework, no decorators.

## In the wild

Every `key=` argument is DI (`sorted`, `min`, `max`); `json.dumps(cls=...)`
injects the encoder; `unittest.mock` exists to be injected. The stdlib does
DI by keyword argument, and so should you.

## Verdict

**Pythonic.** The default-argument seam is the pattern, entire.
