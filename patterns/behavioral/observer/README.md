---
id: behavioral/observer
name: Observer
aliases: [publish-subscribe, listener, event-handler]
guide_url: null
problem: "Notify interested parties when something changes, without the subject knowing who they are."
symptoms: ["react to changes", "event listeners", "pub/sub", "on_change callbacks", "model updates views"]
verdict: pythonic
caveats:
  - "Observers are callables — an Observer ABC with one update() method is a function with extra steps."
  - "Decide the failure policy: one raising observer can silence the rest. Notify inside try/except or document that observers must not raise."
stdlib_sightings: [concurrent.futures.Future.add_done_callback, asyncio.Future]
---

# Observer

## Problem

A model changes and three views must repaint; a download finishes and
logging, metrics, and the UI all care. The subject must broadcast without
compiling a list of friends into itself.

## Naive solution

`naive.py` is the GoF form: Subject with attach/detach/notify, an Observer
ABC, concrete observers implementing `update()`.

## Pythonic solution

Observers are callables in a list; subscribing is appending. `pythonic.py`
also shows the property-setter variant — assignment to `.temperature`
triggers the callbacks — which is how observation usually hides inside
Python APIs.

## In the wild

`concurrent.futures.Future.add_done_callback` is the stdlib observer:
register any callable, it fires when the future resolves — even if it
already has.

## Verdict

**Pythonic.** Lists of callables, everywhere, deliberately.
