# Memento — fundamentals

## Intent

Capture an object's internal state so it can be restored later, without
violating encapsulation: whoever stores the snapshot must not be able to read
or edit it.

## Participants

| Role | Classic (GoF) form | Python form |
|---|---|---|
| Originator | Creates mementos from its state, restores from them | The object whose state is a frozen value (dataclass) |
| Memento | An opaque snapshot class, fields private by convention | The old state object itself — immutability *makes* it opaque-safe |
| Caretaker | Stores mementos, never inspects them | `History` in [`pattern/history.py`](../pattern/history.py) — generic, so it *cannot* peek |

## Mechanism

1. The originator's mutable identity holds an **immutable state value**.
2. Before a change, the current state object is handed to the caretaker
   (`history.save(state)` or `history.checkpoint("name", state)`).
3. A change builds a *new* state value (`dataclasses.replace`) — the old one
   is untouched, which is why saving it cost nothing.
4. Undo/rollback is the caretaker handing a snapshot back and the originator
   adopting it wholesale.

## The classic form, and what Python absorbs

The textbook version writes three classes — the snapshot is its own class,
opaque only by underscore convention:

```python
class Memento:
    """Opaque by convention: only the originator reads its fields."""

    def __init__(self, text: str, cursor: int) -> None:
        self._text = text  # nothing stops a caretaker from peeking
        self._cursor = cursor


class Editor:  # the originator
    def save(self) -> Memento:
        return Memento(self.text, self.cursor)

    def restore(self, memento: Memento) -> None:
        self.text = memento._text  # privileged access, unenforced
        self.cursor = memento._cursor


class History:  # the caretaker
    def push(self, memento: Memento) -> None: ...
    def pop(self) -> Memento: ...
```

Python has no way to truly seal `Memento`'s fields — the design's central
promise is unenforceable here. Freezing the state solves it from the other
side: when state is a frozen dataclass, **the snapshot is the old state
object**. No copy, no dedicated Memento class, and the caretaker can hold it
safely because nobody can mutate it. What survives of the pattern is the
caretaker discipline: history stores snapshots *it never interprets*.

## When to use it

- Undo/redo, checkpoint-and-rollback, save slots — any "return to how it was".
- Speculative edits: try a batch, validate, restore on failure.

## When not to use it

- State is huge and mutable and cannot be frozen — deep-copying per edit is
  the cost the caveats warn about; snapshot the smallest state that matters.
- The "restore" is really replaying inputs → that is Command with an undo
  log, not a snapshot.
- Snapshots must cross a process or trust boundary → that is serialization,
  and the pickle warning in [examples](examples.md) applies.

## Verdict: use with care

Tilt the design toward immutable state, where the pattern costs nothing —
`History` plus a frozen dataclass is the whole implementation.
