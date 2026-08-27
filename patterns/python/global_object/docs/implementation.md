# Global Object — putting it into a system

## The smell it fixes

The same value rebuilt everywhere, or threaded through every call chain as
noise:

```python
def handler(request, config, slug_re, zone_table):  # everyone carries the bags
    ...
def other_handler(request):
    zone_table = load_zone_table()  # ... or rebuilds them
```

## Steps

1. **Sort your globals into the three kinds.** Constant? Cheap-and-pure
   prebuilt? Expensive? The kind decides the treatment; nothing else does.
2. **Assign constants and cheap prebuilt objects at module level.** Name them
   in CAPS; make them immutable types (`frozenset`, `tuple`, compiled regex)
   so mutation is impossible rather than discouraged.
3. **Wrap every expensive construction in `Lazy`.**
   `TABLE: Lazy[dict[str, int]] = Lazy(_build_table)` — importing stays free,
   the first `TABLE.get()` pays once.
4. **Give tests the reset seam.** A fixture calling `TABLE.reset()` restores
   order-independence; a counter in the factory lets a test *prove* import
   does no work (see the worked example's `FACTORY_RUNS`).
5. **Audit for the two misuses.** Anything mutable at module level needs a
   sentence of justification; any import-time I/O is a bug, full stop.

```python
from patterns.python.global_object import Lazy

PRICES: Lazy[dict[str, int]] = Lazy(_load_prices)  # import: free
PRICES.get()["basic"]  # first use: built once
```

## Python idioms that keep it small

- `frozenset`/`tuple`/`re.compile` make constants self-enforcing.
- The module *is* the singleton — resist wrapping globals in a class whose
  only job is to hold them.
- A `_private` name plus a public accessor (`get_settings()`) is the escape
  hatch when construction later needs parameters; `Lazy` gives you that
  accessor for free.

## Pitfalls

- **Import-time I/O** — the cardinal sin: every importer pays, test runs
  touch disk/network, and import order starts to matter.
- **The convenience mutable global.** `CACHE: dict = {}` at module level
  couples every caller; if shared mutation is not the documented job, inject
  the object instead.
- **Lazy globals that capture config.** If the factory reads other globals,
  a test that tweaks config after first use sees stale state — reset in the
  fixture, or pass config explicitly.
- **Hidden identity assumptions.** Two modules importing the name share one
  object; if a consumer mutates a "constant" list, everyone sees it. Immutable
  types close the hole.

## Worked example

[`examples/settings_module/`](../examples/settings_module/) ships one global
of each kind — constant, prebuilt regex, lazy zone table — and a test that
proves import does no work. Run it:

```bash
uv run python -m patterns.python.global_object.examples.settings_module
```
