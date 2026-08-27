# Strategy — fundamentals

## Intent

Define a family of algorithms, encapsulate each one, and make them
interchangeable — so the algorithm can vary independently of the code that
uses it. A checkout applies one of several promotion rules; a sorter orders by
one of several keys; the caller neither knows nor cares which variant it got.

## Participants

| Role | Classic (GoF) form | Python form |
|---|---|---|
| Strategy contract | An interface with one method | Any callable `(argument) -> result` — a type alias documents it |
| Concrete strategies | One class per algorithm | Plain functions |
| Context | An object holding a strategy reference | An argument: `sorted(data, key=...)` |
| Open families | Manual wiring in the client | A registry — `StrategyRegistry` in [`pattern/registry.py`](../pattern/registry.py) |

## Mechanism

1. Name the strategy signature (what goes in, what comes out).
2. Write each algorithm to that signature.
3. Pass the chosen one where the work happens — or register the whole family
   so callers can look one up, run them all, or take the best.

## The classic form, and what Python absorbs

The textbook implementation builds a class hierarchy because 1994 languages
had no first-class functions:

```python
class Promotion(ABC):
    """The strategy interface."""

    @abstractmethod
    def discount(self, order: Order) -> float: ...


class BulkItemPromo(Promotion):
    def discount(self, order: Order) -> float:
        return sum(item.total() * 0.1 for item in order.cart if item.quantity >= 20)


class LargeOrderPromo(Promotion): ...


class Order:  # the context, holding one interchangeable strategy
    def __init__(self, cart: list[LineItem], promotion: Promotion | None = None) -> None:
        self.promotion = promotion
```

One interface, one class per algorithm, a context that stores one — all to
pass behavior as a value. Python passes behavior as a value natively:
`sorted(words, key=str.casefold)` **is** the Strategy pattern, in four
characters of ceremony. What survives translation is the *intent* (a named,
swappable family of algorithms behind one signature), not the class diagram.

## When to use it

- The same operation has several legitimate algorithms chosen at runtime
  (pricing rules, retry policies, sort orders, auth schemes).
- The set of algorithms is open — new ones should slot in without editing the
  code that runs them (that is what the registry adds).

## When not to use it

- Only one algorithm exists → just write the function.
- The variants differ by *data*, not logic → a parameter or a config value.
- A strategy needs state or several cooperating methods → a class is then the
  right form; that is the surviving use of the classic shape.

## Verdict: prefer an alternative

The alternative is a plain function passed as an argument. Use
`StrategyRegistry` when the family is open and discoverable-by-name matters;
reach for strategy *classes* only when a strategy owns state of its own.
