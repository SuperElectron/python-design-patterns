# Mediator — fundamentals

## Intent

Stop a web of objects from referencing each other by routing all their
interaction through one coordinator. N components with pairwise rules is N²
couplings; a mediator makes it N spokes and one hub that owns every rule.

## Participants

| Role | Classic (GoF) form | Python form |
|---|---|---|
| Mediator | An interface, then a ConcreteMediator | One class holding every rule — often a single `_recheck` method |
| Colleagues | A `Widget` base class holding a mediator reference | Plain value holders wired with a `notify` callable — [`Field`](../pattern/form.py) |
| Interaction protocol | `mediator.widget_changed(widget)` | Any change calls `notify()`; the mediator re-derives the whole state |

## Mechanism

1. Components hold values and report changes; they contain zero rules.
2. On any change, the mediator recomputes every derived fact and cascades:
   invalidated selections reset, dependent options update, gating re-checks.
3. Rules are readable in one place — and testable without any UI.

## The classic form, and what Python absorbs

The textbook dialog threads a Colleague hierarchy through a mediator
interface:

```python
class Widget:
    def __init__(self, mediator: SignupDialog, name: str) -> None:
        self.mediator = mediator  # every widget carries the wiring
        self.name = name

    def changed(self) -> None:
        self.mediator.widget_changed(self)


class TextField(Widget): ...  # subclasses per widget kind


class Button(Widget): ...


class SignupDialog:  # the mediator
    def widget_changed(self, _widget: Widget) -> None:
        self.submit.enabled = bool(self.username.text) and len(self.password.text) >= 8
```

Python needs none of the hierarchy: a widget is a value holder plus a
`notify` callable, and the mediator is whoever handed out that callable.
What survives is the *discipline*, not the class diagram: *widgets dumb,
rules in one place*. For pipeline-shaped decoupling, the language absorbs
the pattern further still — `queue.Queue` is a degenerate mediator where
the only rule is "hand items across".

## When to use it

- Interaction rules genuinely tangle: field A restricts B, B gates C, C
  changes a total — and the set must stay coherent after every change.
- You are deleting pairwise references: each component should know the hub,
  never a sibling.

## When not to use it

- Two components, one rule → a direct callback is honest and shorter.
- Broadcast with no cross-rules ("tell everyone it changed") → Observer.
- Producer/consumer decoupling → a queue *is* the mediator; don't wrap one.

## Verdict: use with care

The mediator earns its keep by the references it deletes. If it grows into a
god object that knows every domain rule in the app, you traded a web for a
blob — split it by interaction cluster.
