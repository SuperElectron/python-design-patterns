# Observer — fundamentals

## Intent

Define a one-to-many dependency so that when one object changes state, all
its dependents are notified automatically — without the subject compiling a
list of friends into itself.

## Participants

| Role | Classic (GoF) form | Python form |
|---|---|---|
| Subject | `attach` / `detach` / `notify` methods | `Signal` in [`pattern/signal.py`](../pattern/signal.py) — or any list of callables |
| Observer contract | An ABC with one `update()` method | Any callable `(event) -> None` |
| Concrete observers | Subclasses implementing `update()` | Plain functions, bound methods, callable objects |

## Mechanism

1. Interested parties subscribe — in Python, appending a callable.
2. The subject changes and emits: each subscriber is called, in order, with
   the event.
3. The subject knows *that* it has subscribers, never *who* they are —
   adding a fourth listener touches zero subject code.
4. A failure policy governs what a raising subscriber does to the rest —
   the decision GoF never mentions and production code lives or dies by.

## The classic form, and what Python absorbs

The textbook version builds an inheritance seam for what is, in Python, an
argument slot:

```python
class Observer(ABC):
    @abstractmethod
    def update(self, temperature: float) -> None: ...


class Display(Observer):
    def update(self, temperature: float) -> None: ...


class WeatherStation:  # the subject
    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def set_temperature(self, value: float) -> None:
        self._temperature = value
        for observer in self._observers:
            observer.update(value)  # one-method interface = a function
```

An ABC with a single `update` method *is* a function with extra steps: the
callable protocol already expresses "something invokable with an event."
Subscribing collapses to `list.append`; the subject's whole machinery is a
loop. What survives is the dependency direction — the subject broadcasts to
strangers — and the two decisions the class diagram hides: **notification
order** and **failure policy**.

A second Python absorption: observation often hides behind a `@property`
setter, so plain attribute assignment (`station.temperature = 35.0`)
triggers the broadcast. That is how observing APIs usually *feel* in Python
even when a `Signal` sits underneath.

## When to use it

- Several independent reactions to one change (email + metrics + audit), and
  the emitter must not know them.
- Plug-in points: subscribers registered from modules the subject never imports.

## When not to use it

- Exactly one, known receiver → call it. Indirection without fan-out is noise.
- The reaction must happen *before* the change commits → that is validation,
  not observation; observers can't veto.
- Cross-process or durable events → a message queue; in-process observers
  silently die with the process.

## Verdict: pythonic

Lists of callables, everywhere, deliberately — `Signal` only adds the two
policies (order, failure) that a bare list leaves implicit.
