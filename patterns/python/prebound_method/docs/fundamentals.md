# Prebound Method — fundamentals

## Intent

Offer module-level functions that share state, by building **one instance** at
module import and binding its methods to module-global names. Callers get the
ergonomic API — `random.random()`, not
`random.get_default_generator().random()` — while the shared state rides along
inside each bound method. Source chapter:
[python-patterns.guide/python/prebound-methods](https://python-patterns.guide/python/prebound-methods/).

## Participants

| Role | What it is |
|---|---|
| The public class | An ordinary class holding the shared state (`Counter`, `random.Random`) — public so isolation stays possible |
| The hidden instance | One module-private instance, built at import (`_instance = Counter()`) |
| The prebound names | Module globals assigned from bound methods (`increment = _instance.increment`) |
| Callers | Import and call plain functions, never seeing the instance |

## Mechanism

1. Write the class as if the pattern did not exist: state in `__init__`,
   behavior in methods, fully testable in isolation.
2. At module level, build one instance — cheaply and without I/O, because
   this line runs at import time.
3. Assign the instance's bound methods to module-global names. A bound method
   carries its `__self__`, so every call reaches the same state.
4. Leave the class public. Anyone needing an isolated copy instantiates it —
   exactly as `random.Random` stays available beside `random.random`.

## The alternatives it replaces

The two shapes the guide rejects, side by side:

```python
# Alternative A: bare functions over a loose module global — the state and
# the functions guarding it drift apart, and a second counter later means
# rewriting every caller.
_count = 0


def increment() -> int:
    global _count
    _count += 1
    return _count


# Alternative B: no module API at all — every caller, everywhere, forever:
counter = Counter()
counter.increment()
```

The prebound form keeps A's ergonomics and B's design: the state lives in a
real class; only the *default instance* is module-level. Migrating to
per-caller instances later is a class already shipped, not a rewrite.

## When to use it

- A module-level convenience API over genuinely shared state: metrics,
  default RNG, a default registry, a process-wide clock.
- You are tempted by Alternative A — this is the same ergonomics without
  orphaned state.

## When not to use it

- Construction is expensive or does I/O → it would run at import; use a lazy
  accessor instead (see `python/global_object`).
- The state should not be shared by default (per-request, per-tenant) →
  instantiate explicitly or inject (see `modern/dependency_injection`).

## Verdict: pythonic

The stdlib's own favorite way to put a friendly face on shared state —
`random`, `secrets`, and `calendar` all ship it.
