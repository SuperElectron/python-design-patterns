# Prebound Method — putting it into a system

## The smell it fixes

Module functions guarding a loose global, or a "helper instance" every caller
must construct and thread:

```python
_registry: dict[str, Handler] = {}  # state ...


def register(name, handler): ...  # ... and its functions, drifting apart
```

## Steps

1. **Write the class first.** State in `__init__`, behavior in methods, its
   own unit tests. If the class is not worth testing alone, the pattern is
   overkill — keep plain functions.
2. **Build one module-private instance** (`_collector = MetricsCollector()`).
   The construction runs at import: it must be cheap, pure, and I/O-free.
3. **Prebind the public surface**, one line per name:

   ```python
   increment = _collector.increment
   timing = _collector.timing
   snapshot = _collector.snapshot
   ```

   Bind only what callers need — the instance's full surface stays behind
   the underscore.
4. **Keep the class exported.** The isolation escape hatch is half the
   pattern; tests and libraries build their own instance instead of fighting
   the shared one.
5. **Give tests a seam.** Either prebind a `reset()` (as the metrics example
   does) or have fixtures instantiate a fresh class — never let tests depend
   on the shared instance's accumulated state.

## Python idioms that keep it small

- A bound method is just an object: assignment is the whole mechanism, no
  wrapper functions, no `functools`.
- `shares_instance(f, g)` (in this unit's `pattern/`) proves the wiring in a
  test: every prebound name carries the same `__self__`.
- Docstring the *module*, not each prebound name — the class's docstrings
  already travel with the bound methods.

## Pitfalls

- **Import-time construction that grows up.** The instance starts cheap; a
  refactor adds a config read and suddenly every import does I/O. Guard it
  with a test, or switch to `Lazy` from `python/global_object`.
- **Hiding the class.** Making `Counter` private forces monkeypatching where
  instantiation would have done — the escape hatch is load-bearing.
- **Shared state leaking across tests.** The prebound API is process-global
  by design; tests that use it must reset it (or use their own instance).
- **Prebinding mutable attributes** instead of methods — attribute access
  copies the reference once; later rebinding on the instance is invisible to
  importers.

## Worked example

[`examples/metrics/`](../examples/metrics/) ships a process-wide metrics API
(`increment`/`timing`/`snapshot`/`reset`) prebound from a hidden
`MetricsCollector`, with the class public for isolated collectors. Run it:

```bash
uv run python -m patterns.python.prebound_method.examples.metrics
```
