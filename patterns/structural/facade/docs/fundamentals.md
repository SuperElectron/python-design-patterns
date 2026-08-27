# Facade — fundamentals

## Intent

Give a complicated subsystem one simple entry point for the common case. The
facade performs the multi-step dance callers would otherwise copy-paste —
in the right order, with the right cleanup — while the subsystem stays
public for anyone needing the full controls.

## Participants

| Role | Classic (GoF) form | Python form |
|---|---|---|
| Facade | A class whose methods run subsystem sequences | Usually a module-level *function* — see [`pattern/checkout.py`](../pattern/checkout.py) |
| Subsystem classes | The machinery being fronted | Same, and deliberately still importable |
| Client | Calls the facade for the common case | Calls `place_order(...)`; reaches past it when needed |

## Mechanism

1. Identify the sequence every caller repeats against the subsystem.
2. Put that sequence — ordering, error handling, rollback — in one callable.
3. Callers use the one door for the common case.
4. The subsystem stays public: the facade simplifies, it must not imprison.

## The classic form, and what Python absorbs

The textbook facade is a class because 1994 had nothing else to hang a
function on:

```python
class HomeTheaterFacade:
    def __init__(self) -> None:
        self.amp = Amplifier()
        self.projector = Projector()
        self.lights = Lights()

    def watch_movie(self) -> list[str]:  # the one method
        return [
            self.lights.dim(10),
            self.projector.on(),
            self.projector.wide_screen(),
            self.amp.on(),
            self.amp.set_volume(5),
        ]
```

Python has modules for namespacing and functions as first-class entry points,
so a facade with one operation *is a function* — a class with a single method
is a function wearing a costume (this unit's standing caveat). The class form
earns its keep only when the facade holds real state across calls, as the
mini-project's `Store` does for a whole trading day.

## When to use it

- Callers repeat the same multi-call sequence against a subsystem, and one
  misordered step or forgotten rollback is a real bug you have seen.
- You want a stable, small surface in front of churning machinery.

## When not to use it

- One underlying call → just call it; a pass-through layer is noise.
- Callers all need different sequences → there is no common case to front.
- You are tempted to *hide* the subsystem → that's a different (worse)
  decision; keep the machinery importable.

## Verdict: pythonic

Ship the one-call common case as a function with good defaults; keep the
subsystem's door open. `subprocess.run` over `Popen` is the stdlib's model
citizen of this shape.
