# Chain of Responsibility — fundamentals

## Intent

Avoid coupling the sender of a request to its receiver by giving more than one
handler a chance to act. The request travels an ordered chain until one handler
takes it; the sender never knows — and never needs to know — which one will.

## Participants

| Role | Classic (GoF) form | Python form |
|---|---|---|
| Handler contract | Abstract class with a successor pointer | Any callable `(request) -> answer \| None` — `None` means "decline, try the next" |
| Concrete handlers | Subclasses overriding an `_attempt` hook | Plain functions (or any callable) |
| The chain itself | Implicit in the successor links | An explicit ordered collection — `Chain` in [`pattern/chain.py`](../pattern/chain.py) |
| Client | Talks to the head of the chain | Calls `chain.handle(request)` |

## Mechanism

1. Handlers are placed in a deliberate order.
2. A request is offered to each handler in turn.
3. A handler either returns an answer (the chain stops) or declines by
   returning `None` (the chain continues).
4. If every handler declines, the *caller's* chosen policy applies — raise
   (`handle`) or fall back to a default (`handle_or`). GoF leaves this case
   undefined; making it explicit is the one improvement you should always add.

## The classic form, and what Python absorbs

The textbook implementation threads a successor pointer through handler
*objects* — each one both does its work and forwards to the next:

```python
class Handler(ABC):
    def __init__(self, successor: Handler | None = None) -> None:
        self.successor = successor  # every handler carries the wiring

    def handle(self, severity: int) -> str:
        answer = self._attempt(severity)
        if answer is not None:
            return answer
        if self.successor is None:
            return "unhandled"  # the fall-off-the-end case, buried
        return self.successor.handle(severity)

    @abstractmethod
    def _attempt(self, severity: int) -> str | None: ...


class Helpdesk(Handler): ...


class Engineer(Handler): ...


class Management(Handler): ...


chain = Helpdesk(Engineer(Management()))  # order hidden in nesting
```

Three classes, an ABC, and pointer bookkeeping — because 1994 languages had no
first-class functions. In Python the same design collapses: handlers are
functions, the chain is a list, dispatch is a loop. That collapse *is* the
pattern's Python lesson: what survives is not the class diagram but the two
ideas — **decline by convention** and **order as policy**.

## When to use it

- Several handlers could serve a request and the right one is known only at
  runtime (escalation tiers, fallback strategies, middleware).
- You want to add, remove, or reorder handling policies without touching the
  sender.

## When not to use it

- Exactly one receiver is ever right → a plain function call or a dict lookup.
- Every handler must see the request (notification, not handling) → that is
  Observer, not a chain.
- The dispatch key is a simple value → `dict[key, handler]` beats scanning.

## Verdict: prefer an alternative

A list of callables and a loop is the whole pattern (this module's `Chain` is
that loop with a name and an explicit unhandled policy). Reach for
successor-pointer objects only when handlers are already stateful objects that
own their forwarding decision.
