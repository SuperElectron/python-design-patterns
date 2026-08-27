# Sentinel Object — putting it into a system

## The smell it fixes

`get(...) or default` bugs, and absence checks that quietly eat legal values:

```python
timeout = config.get("timeout") or 30  # a configured 0 becomes 30
if cached is None:  # a cached None recomputes forever
    cached = expensive()
```

## Steps

1. **Find the collision.** Which legal value is doubling as "absent"?
   (`None`, `0`, `""`, `-1` are the usual suspects.)
2. **Mint one named sentinel per meaning** — `MISSING = Sentinel("MISSING")`
   from this unit's `pattern/`, or a bare `_MISSING = object()` when a repr
   does not matter. One marker per *meaning*, not per call site.
3. **Thread it through the boundary**: `layer.get(key, MISSING)` inside,
   a clean `Value` type outside. The sentinel should not leak into public
   return types — resolve it (raise, or apply the caller's default) before
   returning.
4. **Check by identity** — `value is MISSING`, the rule the pattern lives
   by: equality is overloadable, and a type check (`isinstance(value,
   Sentinel)`) would swallow any *other* sentinel stored as a legitimate
   value. Under `mypy --strict` a `cast` at the return keeps the public
   type clean; identity remains the semantic guard.
5. **Upgrade chronic branching to a Null Object.** If many callers test the
   sentinel just to skip work, return a do-nothing implementation of the real
   interface instead (`NullNotifier` in the worked example).

```python
from patterns.python.sentinel_object import MISSING, Sentinel


def get(self, key: str, default: Value | Sentinel = MISSING) -> Value:
    for layer in self._layers:
        value = layer.get(key, MISSING)
        if value is not MISSING:
            return cast("Value", value)  # a stored None wins here
    if default is MISSING:
        raise KeyError(key)
    return cast("Value", default)
```

## Python idioms that keep it small

- `dict.get(key, MISSING)` turns "key present?" plus "value None?" into one
  identity check.
- A keyword default of `MISSING` distinguishes "not passed" from "passed
  None" without `**kwargs` games.
- `__slots__` and a `__repr__` on a tiny `Sentinel` class cost three lines
  and make debugger output say `<MISSING>` instead of `<object object at …>`.

## Pitfalls

- **`==` instead of `is`.** Equality is overloadable; identity is the
  contract. `value == MISSING` invites a `__eq__` to lie.
- **Sentinels escaping the API.** A public function returning `MISSING`
  forces every caller to import your marker — resolve absence at the
  boundary.
- **Pickle/copy round-trips.** A copied sentinel is a different object;
  identity checks fail across process boundaries. Keep sentinels inside one
  process's logic (PEP 661 discusses the fix).
- **In-band "improvements".** Replacing the sentinel with `-1`/`""` to avoid
  the import reintroduces the original bug one type away.

## Worked example

[`examples/layered_config/`](../examples/layered_config/) resolves settings
CLI ← file ← defaults where a stored `None` means "explicitly disabled", and
hands back a `NullNotifier` so callers never branch. Run it:

```bash
uv run python -m patterns.python.sentinel_object.examples.layered_config
```
