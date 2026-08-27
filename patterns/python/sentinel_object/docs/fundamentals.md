# Sentinel Object — fundamentals

## Intent

Mark "no value here" unambiguously when `None` itself is a legitimate value.
A fresh object exists in no domain: it equals nothing but itself, cannot be
forged, and is checked by identity — so "the value is None" and "there is no
value" stop colliding. Source chapter:
[python-patterns.guide/python/sentinel-object](https://python-patterns.guide/python/sentinel-object/).

## Participants

| Role | What it is |
|---|---|
| The sentinel | One module-level marker — `Sentinel`/`MISSING` in [`pattern/sentinel.py`](../pattern/sentinel.py) |
| The APIs | Functions/containers that accept or return it in place of "absent" |
| The identity check | `value is MISSING` — identity *is* the meaning |
| The Null Object | The neighboring cure (Fowler/Woolf): a do-nothing stand-in with real methods, for when callers should not branch at all |

## Mechanism

1. Create one marker per distinct meaning, module-level, named:
   `MISSING = Sentinel("MISSING")`.
2. Use it wherever "absent" must be distinguishable from every legal value —
   dict lookups (`d.get(k, MISSING)`), default arguments, cache slots.
3. Check with `is`, never `==` — equality can be overloaded; identity cannot.
4. Where absence would make every caller branch, upgrade to a Null Object: an
   implementation of the real interface that intentionally does nothing.

## The failure modes it replaces

```python
# Failure 1: the in-band sentinel VALUE. str.find's -1 is a legal integer,
# so forgetting the check produces plausible garbage, not an error:
position = text.find(needle)  # -1 when absent ...
return text[position - 1]  # ... silently becomes text[-2]

# Failure 2: None-as-missing where None is storable. A cache holding a
# legitimate None cannot tell a hit from a miss:
value = self._data.get(key)
if value is None:  # ... but None might BE the cached value!
    value = compute()
```

An in-band sentinel lives inside the value's own type and eventually
collides; `None` is just the most common in-band sentinel of all. A fresh
`object()` closes both holes — which is why the problem earned a PEP
([PEP 661](https://peps.python.org/pep-0661/)).

## When to use it

- `None` (or `-1`, or `""`) is a legitimate stored/passed value and "not
  provided" must remain distinct.
- Default arguments where "caller passed None" and "caller passed nothing"
  behave differently.

## When not to use it

- `None` genuinely means absent and nothing stores it → `None` is simpler
  and idiomatic; do not invent markers for their own sake.
- Callers branch on the sentinel everywhere → that is the Null Object's job;
  hand back a do-nothing implementation instead.

## Verdict: pythonic

One module-private marker per meaning, compared with `is`. The stdlib ships
it as `dataclasses.MISSING`, `inspect.Parameter.empty`, and two-argument
`iter`.
