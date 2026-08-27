# Composition Over Inheritance — fundamentals

## Intent

Vary independent behaviors without one subclass per combination of them.
"Favor object composition over class inheritance" is the second principle in
the GoF introduction — the soil the structural and behavioral patterns grow
from. Each independent axis of variation becomes its own small object,
injected where needed; M + N pieces cover M × N behaviors. Source chapter:
[python-patterns.guide/gang-of-four/composition-over-inheritance](https://python-patterns.guide/gang-of-four/composition-over-inheritance/).

## Participants

| Role | What it is |
|---|---|
| Axes of variation | The independent behaviors (what to accept, how to shape, where to send) |
| One small piece per axis | A callable or tiny class per behavior — `Filter`/`Transform`/`Sink` in [`pattern/compose.py`](../pattern/compose.py) |
| The composition point | The one class that holds a piece per axis and wires them — `Pipeline` in [`pattern/compose.py`](../pattern/compose.py); `Logger` and the example's `Notifier` are `Pipeline` put to work |
| Clients | Pick pieces and construct; a new combination is a constructor call |

## Mechanism

1. Name the axes. If a class name wants two adjectives
   (`FilteredSocketLogger`), there are at least two.
2. Give each axis its own minimal interface — in Python usually just a
   callable signature.
3. Write one composition-point class holding one piece per axis; its methods
   delegate in a fixed, readable order.
4. Combinations are now data: constructed, passed, and tested — never
   subclassed into existence.

## The subclass explosion, and what composition replaces

The classic route bolts each behavior on by subclassing — and then needs a
class *per combination*:

```python
class Logger: ...  # base


class FilteredLogger(Logger): ...  # axis 1 bolted on


class UppercaseLogger(Logger): ...  # axis 2 bolted on


class FilteredUppercaseLogger(FilteredLogger):  # the explosion begins:
    """One class PER COMBINATION."""  # M x N x P classes coming
```

Two axes already cost four classes; each new filter or destination
*multiplies* the count. The dodges — multiple inheritance, mixins,
dynamically built classes — postpone the explosion rather than end it. The
composed form keeps one class per *piece* plus one composition point, and
the arithmetic turns from multiplication into addition.

## When to use it

- Two or more behaviors vary independently (filtering × formatting ×
  destination; retry × serialization × transport).
- Subclass names are growing adjectives, or a mixin diamond is forming.

## When not to use it

- One axis, two variants, stable → a single `if` or a subclass is honest and
  smaller; composition machinery would be ceremony.
- The "axes" are not independent (one behavior's output feeds another's
  contract) → model the coupling explicitly; forced composition hides it.

## Verdict: pythonic

The single most load-bearing idea behind the rest of this catalog — the
stdlib's `logging` (Logger/Handler/Filter/Formatter) is this principle
shipped at scale, with no `FilteredRotatingSyslogLogger` in sight.
