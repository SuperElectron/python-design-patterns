# Composition Over Inheritance — putting it into a system

## The smell it fixes

Class names collecting adjectives, and a new requirement meaning a new
subclass:

```python
class JsonFileNotifier(FileNotifier): ...


class DedupJsonFileNotifier(JsonFileNotifier): ...


class DedupJsonWebhookNotifier(...): ...  # and severity thresholds arrive Monday
```

## Steps

1. **List the axes.** Read the subclass names: each adjective is an axis
   (dedup / json / webhook = decide / reshape / act).
2. **Define one minimal interface per axis.** In Python a callable signature
   is usually enough — `Filter[T] = Callable[[T], bool]`,
   `Transform[T, U] = Callable[[T], U]`, `Sink[T] = Callable[[T], None]`
   (importable from this unit's `pattern/`).
3. **Extract each behavior into a piece.** Plain functions for stateless
   pieces; a small callable class where state is real (`Dedup`); a closure
   factory where only a parameter varies (`min_severity(4)`).
4. **Write the composition point** — one dataclass with one field per axis
   and the delegation order spelled out in one method.
5. **Delete the subclass tree.** Every leaf class becomes a constructor call;
   its tests become tests of a *combination*, which now read as configuration.

```python
from patterns.principle.composition_over_inheritance import Pipeline

# Notifier = Pipeline[Alert, str] — the domain names the composition point.
pager = Notifier(filters=(min_severity(4), Dedup()), transform=as_json, sink=webhook)
```

## Python idioms that keep it small

- **Callables are the interfaces.** No ABCs needed until an axis has multiple
  methods; `Protocol` when it does.
- **Closure factories replace parameter subclasses**: `min_severity(4)` is
  the whole class `SeverityAtLeastFourFilter`.
- **`functools.partial`** turns any configurable function into a piece.
- **Dataclasses as composition points** make the wiring visible in `repr`
  and trivially testable.

## Pitfalls

- **Rebuilding inheritance inside composition** — a piece that reaches into
  the composition point (or another piece) recreates the coupling with extra
  steps. Pieces see only their own input.
- **The god-piece.** One "filter" that also formats and delivers has eaten
  the axes; if a piece needs two verbs to describe, split it.
- **The mixin dodge.** `class DedupMixin: ...` feels cheaper today and
  reconverges on the diamond tomorrow — the guide's taxonomy of dodges is
  worth rereading when tempted.
- **Order left implicit.** The composition point owns the delegation order;
  document and test it (filters run in order and short-circuit — a stateful
  filter placed after a veto never records vetoed items).

## Worked example

[`examples/notification_router/`](../examples/notification_router/) routes
alerts through filter × format × deliver pieces — console plain-text at
severity ≥ 2, deduped JSON to a webhook at severity ≥ 4 — one `Notifier`
class, zero combination subclasses. Run it:

```bash
uv run python -m patterns.principle.composition_over_inheritance.examples.notification_router
```
