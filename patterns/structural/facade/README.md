---
id: structural/facade
name: Facade
aliases: [front-door, simplified-interface]
guide_url: null
problem: "Give a complicated subsystem one simple entry point for the common case."
symptoms: ["five-step setup for one common task", "callers copy-paste the same subsystem dance", "wrap this messy API"]
verdict: pythonic
caveats:
  - "In Python a facade is usually a module-level function — a class with one method is a function wearing a costume."
  - "A facade simplifies; it must not imprison. Leave the subsystem importable for callers who need the full controls."
stdlib_sightings: [subprocess.run, shutil.make_archive, urllib.request.urlopen]
---

# Facade

## Problem

Doing the common thing takes five coordinated calls into a subsystem, and
every caller performs the same dance. One misordered step, one leaked
resource, and the copy-paste bill comes due.

## Naive solution

`naive.py` is the class-shaped version: subsystem classes plus a
`HomeTheaterFacade` whose one method runs the sequence.

## Pythonic solution

Modules are namespaces and functions are entry points, so the natural Python
facade is a *function*: `pythonic.py` wraps a fiddly multi-step text
pipeline behind one call with sensible defaults — full controls still
importable beside it.

## In the wild

`subprocess.run` is a facade over `Popen`'s wiring; `shutil.make_archive`
fronts `zipfile`/`tarfile`; `urllib.request.urlopen` hides openers and
handlers. Each leaves the machinery public underneath.

## Verdict

**Pythonic.** Ship the one-call common case; keep the subsystem's door open.
