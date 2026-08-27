# Factory Method — fundamentals

## Intent

A class needs a helper object mid-work — an HTTP connection needs a response
object — but which helper class is the right one must stay open: subclasses,
configuration, or tests substitute their own without rewriting the containing
class.

## Participants

| Role | Classic (GoF) form | Python form |
|---|---|---|
| Creator | Abstract class with an abstract `factory_method()` | The class that needs the helper — creation is a **class attribute** holding any callable |
| Concrete creators | One subclass per helper choice | A one-line subclass, or a constructor argument per instance. Class-level slots hold a class bare, or any other callable via `factory_slot` — a bare *function* in a class body binds `self` and raises `TypeError` when called |
| Product | Abstract product interface | Whatever the factory callable returns |
| Concrete products | Subclasses of the product | Any objects; no shared base required |

## Mechanism

1. The creator does its work and, at the moment it needs a helper, calls its
   factory instead of naming a class.
2. Who decides what the factory builds is the variation point: the class
   default, a subclass, an instance, or the caller.
3. In Python any callable is a factory — a class *is* one, so is a function or
   a `functools.partial`.

## The classic form, and what Python absorbs

The textbook version makes the variation point an abstract method, which costs
a subclass per configuration:

```python
class Store(ABC):
    @abstractmethod
    def make_shipment(self) -> Shipment: ...  # the deferred decision

    def ship(self) -> str:
        return f"shipping via {self.make_shipment().kind}"


class ExpressStore(Store):  # one subclass...
    def make_shipment(self) -> Shipment:
        return Express()


class StandardStore(Store):  # ...per choice
    def make_shipment(self) -> Shipment:
        return Standard()
```

The design exists because 1994 languages could not pass a class or function as
a value. Python can, so the guide's dodges rank ahead of it, best first — the
[`examples/feed_client/`](../examples/feed_client/) mini-project shows all
three on one framework class:

1. **Dependency injection** (`FeedClient(transport)`) — if the helper can
   exist up front, pass the object and skip the factory entirely.
2. **Class-attribute factory** (`FeedClient.response_class`) — creation stays
   inside the class; a subclass overrides the slot in one line. A class is
   safe to assign bare; wrap any other callable in `factory_slot` (from
   [`pattern/`](../pattern/)) so it does not bind as a method.
3. **Instance-attribute factory** — a constructor argument shadows the class
   attribute for one object; tests love this.

## When to use it

- A framework class must build objects the application is allowed to replace
  (`response_class`-style hooks).
- Creation must happen *inside* the worker (mid-protocol, in a loop), so you
  cannot simply pass the finished object in.

## When not to use it

- The helper can be built before the worker starts → inject the object.
- The choice is data, not code → a `dict[str, Factory]` lookup.
- One abstract method + parallel subclass trees are growing → you are paying
  Java's cost without Java's constraint.

## Verdict: prefer an alternative

Inject the dependency; failing that, a class-attribute factory. The
abstract-method form survives here only as the classic listing above.
