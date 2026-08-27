# State — fundamentals

## Intent

Let an object alter its behavior when its internal state changes — the object
appears to change class — instead of branching on a mode flag in every method.

## Participants

| Role | Classic (GoF) form | Python form |
|---|---|---|
| Context | Holds a state object, delegates every operation to it | The domain object holding a `StateMachine` (or just an `Enum` field) |
| State interface | An ABC, one method per operation | An `Enum` of states + a table of `(state, event)` pairs |
| Concrete states | A class per state, each owning its transitions | Rows in the table — data, not classes ([`pattern/machine.py`](../pattern/machine.py)) |

## Mechanism

1. Enumerate the states and the events that move between them.
2. Write the machine as a **table**: `(current, event) -> next`. What is
   absent is illegal — the table is a whitelist.
3. Fire events through one choke point (`trigger`), which either moves the
   machine or raises `IllegalTransitionError`; there is no half-move.
4. **Guards** veto listed transitions using data the table can't see
   ("refund only if money was taken"); the **log** records every step.

## The classic form, and what Python absorbs

The textbook version spends a class per state and swaps objects to transition:

```python
class TurnstileState(ABC):
    @abstractmethod
    def coin(self, turnstile: Turnstile) -> str: ...
    @abstractmethod
    def push(self, turnstile: Turnstile) -> str: ...


class Locked(TurnstileState):
    def coin(self, turnstile: Turnstile) -> str:
        turnstile.state = Unlocked()  # transition = object swap
        return "unlocked"


class Unlocked(TurnstileState): ...


class Turnstile:  # the context
    def coin(self) -> str:
        return self.state.coin(self)  # every call delegates
```

Four classes to say four facts. As a table, the same machine is one dict —
whole, on one screen, diffable in review:

```python
TRANSITIONS = {
    (State.LOCKED, "coin"): (State.UNLOCKED, "unlocked"),
    (State.LOCKED, "push"): (State.LOCKED, "locked: push refused"),
    (State.UNLOCKED, "coin"): (State.UNLOCKED, "already unlocked"),
    (State.UNLOCKED, "push"): (State.LOCKED, "pushed through, locking"),
}
```

Python has a second, deeper absorption: a **generator** is a state machine
maintained by the interpreter — the suspension point *is* the state:

```python
def turnstile() -> Generator[str, str, None]:
    while True:
        event = yield "ready"
        if event == "coin":
            event = yield "unlocked"  # the UNLOCKED state lives HERE,
            ...  # in where the frame is paused
```

Every coroutine and parsing loop in the stdlib runs on this: no state field
exists because the position in the code carries it.

## When to use it

- A lifecycle with rules: orders, documents, connections, jobs — anywhere
  "what may happen next" depends on "where we are".
- The moment a second `if self.mode == ...` appears in a second method.

## When not to use it

- Two states, one branch → keep the `if`; a machine is ceremony.
- The "states" are just data values with no transition rules → a plain field.
- The flow is linear consumption of a stream → write the generator directly.

## Verdict: use with care

The table form covers most machines and stays reviewable. A class per state
pays only when each state carries its own data *and* behavior bundle;
generators win when the machine is really a paused program.
