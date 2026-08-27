# Registry — putting it into a system

## The smell it fixes

A dispatcher that every new case must edit:

```python
def export(rows, fmt):
    if fmt == "csv":
        ...
    elif fmt == "json":
        ...
    elif fmt == "xml":
        ...  # this week's edit
    else:
        raise ValueError(...)
```

The ladder couples every format to one function, and the unknown-name policy
gets re-decided (differently) at every ladder in the codebase.

## Steps

1. **Name the contract.** A type alias for what the registry stores
   (`Exporter = Callable[[Rows], str]`) turns "any function" into a checkable
   promise.
2. **Create one registry instance in the module that owns dispatch** —
   `EXPORTERS: Registry[Exporter] = Registry(kind="format")`. The `kind`
   string buys readable errors for free.
3. **Convert each ladder arm into a decorated function.** Its condition
   becomes its name: `@EXPORTERS.register("csv")`.
4. **Route all dispatch through one lookup.** `EXPORTERS.get(fmt)(rows)` —
   the unknown-name policy now lives in the registry, once.
5. **Guarantee plugins are imported.** Registration is an import-time side
   effect, so some module must import each plugin. The package `__init__` is
   the honest place — with a comment saying the import is load-bearing.

```python
from collections.abc import Callable

from patterns.modern.registry import Registry

Rows = list[dict[str, str]]
Exporter = Callable[[Rows], str]

EXPORTERS: Registry[Exporter] = Registry(kind="format")


@EXPORTERS.register("csv")
def to_csv(rows: Rows) -> str: ...
```

## Python idioms that keep it small

- **The decorator returns its target unchanged**, so a registered function is
  still an ordinary, individually-testable function.
- **Keep registries module-level and typed.** A registry passed around as a
  parameter is usually dependency injection wearing the wrong hat.
- **For type-keyed dispatch, don't rebuild this** — `functools.singledispatch`
  already is the registry, with MRO-aware lookup.

## Pitfalls

- **The plugin nobody imports.** The registry only knows what has run.
  Symptom: works in the app (which imports everything), fails in a test that
  imports one module. Fix: import plugins in the package `__init__`, or use
  entry points for cross-package discovery.
- **Silent duplicate registration.** With a bare dict, two plugins claiming
  `"csv"` is a last-import-wins race. `Registry` makes it an error;
  `replace=True` makes an intentional override visible in the diff.
- **Unknown-name policy at call sites.** If callers wrap `get` in their own
  `try/except KeyError` with their own fallbacks, the policy has leaked back
  out — decide it once.
- **Registration with heavier side effects.** The decorator should record the
  entry, nothing more; a plugin that opens connections at import time turns
  every importer into an integration test.

## Worked example

[`examples/export_plugins/`](../examples/export_plugins/) applies every step,
including a plugin in its own module whose `__init__` import is the
documented fix for the import-time caveat:

```bash
uv run python -m patterns.modern.registry.examples.export_plugins
```
