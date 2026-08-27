---
id: modern/registry
name: Registry
aliases: [plugin-registry, dispatch-table]
guide_url: null
problem: "Let implementations announce themselves by name, so dispatch is a lookup instead of an if/elif ladder."
symptoms: ["if/elif on a type string", "plugin system", "handlers by name", "adding a case means editing the dispatcher"]
verdict: pythonic
caveats:
  - "Registration at import time means the module defining a plugin must actually get imported — a plugin nobody imports doesn't exist."
  - "Decide the unknown-key policy (KeyError? default handler?) once, in the lookup, not at each call site."
stdlib_sightings: [codecs.register, functools.singledispatch, atexit.register]
---

# Registry

## Problem

An exporter supports "csv", "json", "xml"… and every new format edits the
same `if/elif` ladder. The dispatcher has become a bottleneck every plugin
must patch.

## Naive solution

`naive.py` is that ladder: closed for extension, growing forever.

## Pythonic solution

A dict from name to callable, filled by a `@register("csv")` decorator —
defining a handler *is* registering it. Dispatch is a lookup; the unknown-key
policy lives in exactly one place.

## In the wild

`codecs.register` is a full plugin registry (every `.encode("rot13")` is a
lookup); `functools.singledispatch` is a registry keyed by type;
`atexit.register` collects callables to run at shutdown.

## Verdict

**Pythonic.** The standard cure for if/elif dispatch.
