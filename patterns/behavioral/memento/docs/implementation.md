# Memento — putting it into a system

## The smell it fixes

Ad-hoc "remember the old values" code smeared through an object:

```python
def risky_update(self, changes):
    old_workers = self.workers  # hand-rolled, per-field,
    old_timeout = self.timeout  # and always one field short
    try:
        ...
    except Exception:
        self.workers = old_workers  # partial restore, subtle drift
        self.timeout = old_timeout
```

Every new field must remember to join the backup ritual. A memento replaces
the ritual with one move: keep the whole old state.

## Steps

1. **Freeze the state.** Move the object's data into a `@dataclass(frozen=True)`.
   The identity (the editor, the service) stays mutable; its *state* doesn't.
2. **Give the originator a `History`.** `History[YourState]()` — the type
   parameter is the whole caretaker contract: it stores and returns, nothing else.
3. **Snapshot before commit.** Each mutation builds a candidate with
   `dataclasses.replace`, validates it, then `history.save(self.state)` and
   adopt the candidate. Order matters: save only what was *valid and live*.
4. **Choose your restore vocabulary.** LIFO `undo()` for editing flows; named
   `checkpoint(name)` / `rollback_to(name)` for operational flows
   ("before-upgrade"). Decide whether a rollback is itself undoable.
5. **Bound the history** if edits are unbounded — a deque with `maxlen`, or
   checkpoint-only retention. Unbounded undo is a slow memory leak.

```python
from patterns.behavioral.memento import History


class ConfigEditor:
    def __init__(self) -> None:
        self.config = ServiceConfig()
        self._history: History[ServiceConfig] = History()

    def apply(self, changes: Mapping[str, Any]) -> ServiceConfig:
        candidate = replace(self.config, **changes)
        validate(candidate)  # reject BEFORE touching history
        self._history.save(self.config)
        self.config = candidate
        return self.config
```

## Python idioms that keep it small

- `dataclasses.replace` is the snapshot-friendly mutation: it forces
  "new value, old value intact" as the default motion.
- Frozen dataclasses with `frozenset`/`tuple` fields keep immutability
  *deep* — a frozen shell over a mutable `list` is a snapshot that lies.
- For state you genuinely cannot freeze, `copy.deepcopy` at the snapshot
  point is the honest fallback; pay the cost visibly, at one call site.

## Pitfalls

- **The shallow snapshot.** Freezing the top object while a field is a
  mutable list shares that list across "snapshots" — undo silently undoes
  nothing. Freeze all the way down.
- **Saving the invalid candidate.** Snapshot the last *good* state, then
  validate the candidate — the demo's rejected batch leaves both the live
  config and the history untouched.
- **A caretaker that peeks.** The moment history code reads snapshot fields,
  restore semantics couple to state internals. `History` is generic
  precisely so it can't.
- **Unpickling as restore.** Restoring from bytes means `pickle.loads`, and
  that executes code during deserialization (CWE-502): only unpickle
  snapshots your own process produced; use JSON for anything that crosses a
  trust boundary.

## Worked example

[`examples/config_checkpoints/`](../examples/config_checkpoints/) applies
every step: atomic validate-or-reject batches, LIFO undo, and a named
"before-upgrade" checkpoint. Run it with:

```bash
uv run python -m patterns.behavioral.memento.examples.config_checkpoints
```
