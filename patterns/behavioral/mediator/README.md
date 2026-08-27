---
id: behavioral/mediator
name: Mediator
aliases: [coordinator, hub]
guide_url: null
problem: "Stop a web of objects from referencing each other by routing their interactions through one coordinator."
symptoms: ["widgets updating each other", "N-squared object references", "form fields with interdependent rules", "components need decoupling"]
verdict: use-with-care
caveats:
  - "The mediator earns its keep by deleting pairwise references; if it grows into a god object that knows everything, you traded a web for a blob."
  - "For pipeline-shaped decoupling, a queue between producers and consumers is the simpler mediator."
stdlib_sightings: [queue.Queue, asyncio.Queue]
---

# Mediator

## Problem

A signup form: the submit button enables only when username and password
fields validate, the password strength meter watches the password field…
Let the widgets reference each other and you get N² couplings that no one
can safely change.

## Naive solution

`naive.py` is the GoF dialog: colleagues report every change to the mediator
and *only* the mediator decides who reacts.

## Pythonic solution

The mediator doesn't need a Colleague base class — widgets accept a
`notify` callable, and the mediator is a small coordinator holding the
interaction rules in one readable place.

## In the wild

`queue.Queue` mediates producers and consumers: neither side knows the
other exists, and the coupling that used to be pairwise lives in one
thread-safe object.

## Verdict

**Use with care.** Excellent for genuinely tangled interaction rules; watch
for god-object drift.
