# Registry — fundamentals

## Intent

Let implementations announce themselves by name so dispatch becomes a lookup
instead of an `if/elif` ladder — and adding a case means writing one new
function, not editing the dispatcher.

## Participants

| Role | Ladder form | Python form |
|---|---|---|
| Dispatcher | One growing `if/elif` function | A mapping — `Registry` in [`pattern/registry.py`](../pattern/registry.py) |
| Cases | Arms of the ladder | Independent callables, possibly in other modules |
| Registration | Editing the ladder | A `@registry.register("name")` decorator at definition site |
| Lookup policy | The trailing `else`, per call site | `registry.get(name)` — one place, one decision |

## Mechanism

1. A module owns a `Registry` instance typed by what it stores
   (`Registry[Exporter]`).
2. Each implementation registers itself where it is defined — the decorator
   makes *defining* a handler and *announcing* it the same act.
3. Dispatch asks the registry by name. Unknown names raise `UnknownKeyError`
   listing what is known; duplicate registrations are an error unless
   explicitly replaced.
4. Because registration runs at import time, a plugin exists only once its
   module has been imported — the pattern's one genuine sharp edge.

## The classic form, and what Python absorbs

The pre-pattern shape is the ladder every plugin must patch:

```python
def export(rows, fmt):
    if fmt == "csv":
        ...  # arm 1
    elif fmt == "keyvalue":
        ...  # arm 2
    else:
        raise ValueError(...)  # the unknown-name policy, re-decided per ladder
```

Closed for extension: format N+1 edits this function, and every parallel
ladder (validate, describe, …) drifts out of sync. Python absorbs the
machinery a plugin framework would add — a dict is the registry, a decorator
is the registration API, first-class functions are the plugins. What survives
is two policies the folk pattern leaves implicit: **what happens on an
unknown name**, and **what happens on a duplicate**.

## When to use it

- Open-ended families keyed by a value: exporters by format, handlers by
  event name, commands by verb.
- Plugins live in modules the dispatcher must not know about.

## When not to use it

- The key is a *type* — `functools.singledispatch` is that registry, built in.
- The set of cases is small, closed, and local — a literal dict (or `match`)
  says so more plainly.
- Cross-package plugins — reach for entry points, which solve the import-time
  problem the plain registry cannot.

## Verdict: pythonic

The standard cure for `if/elif` dispatch; the stdlib itself ships registries
(`codecs.register`, `atexit.register`, `singledispatch.register`).
