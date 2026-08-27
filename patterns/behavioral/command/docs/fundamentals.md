# Command — fundamentals

## Intent

Package a request as an object carrying everything needed to perform it, so
code that triggers requests (menus, queues, schedulers) need not know what
they do — and so requests can be queued, logged, undone, or replayed.

## Participants

| Role | Classic (GoF) form | Python form |
|---|---|---|
| Command contract | Interface with `execute()` (and often `undo()`) | Any callable for execute-only; [`Undoable`](../pattern/commands.py) — a (do, undo) pair — when reversible |
| Concrete commands | One class per operation, binding a Receiver | A closure or `functools.partial` capturing its arguments |
| Invoker | Runs commands, may keep history | [`UndoStack`](../pattern/commands.py): push / undo / redo / log |
| Receiver | The object acted upon | Any object the callables close over |

## Mechanism

1. The moment a request is *created*, everything it needs is captured in it.
2. The invoker executes commands without inspecting them.
3. Because executed commands are objects, history is a list: undo pops and
   reverses; a log is a projection; a queue is deferral.
4. Pushing a new command after undoing clears the redo branch — history is
   linear, and that is a deliberate contract, not an accident.

## The classic form, and what Python absorbs

The textbook shape is an interface and a class per operation:

```python
class Command(ABC):
    @abstractmethod
    def execute(self) -> None: ...
    @abstractmethod
    def undo(self) -> None: ...


class AppendText(Command):  # one class per operation
    def __init__(self, doc: Document, text: str) -> None:
        self.doc, self.text = doc, text

    def execute(self) -> None:
        self.doc.text += self.text

    def undo(self) -> None:
        self.doc.text = self.doc.text[: -len(self.text)]
```

Python absorbs the *deferral* half completely: functions are first-class, so
`partial(log.append, "line")` **is** a packaged request — no interface, no
hierarchy. What survives is the *reversibility* half: a bare callable cannot
carry its own inverse or its own label, so the moment you need undo, audit
logs, or serialization, the request must become data again. That is the
line this module draws: `Action` (a plain callable) below it, `Undoable`
above it.

## When to use it

- Undo/redo — the canonical justification.
- Audit trails and macro recording: executed operations must be inspectable.
- Queues and schedulers where requests outlive the code that created them.

## When not to use it

- "Call this later" with no undo, no log, no metadata → a callable or
  `functools.partial` is the whole pattern; a class hierarchy is ceremony.
- One-off callbacks → pass the function.

## Verdict: use with care

Callables for deferral; the (do, undo) pair exactly when commands need to be
reversed, logged, or stored. See the unit's [caveats](../README.md).
