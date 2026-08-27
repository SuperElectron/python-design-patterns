# Factory Method — putting it into a system

## The smell it fixes

A class that hard-codes a constructor call deep inside its work:

```python
class FeedClient:
    def fetch(self, url):
        raw = self._transport(url)
        return FeedResponse(raw)  # nobody can substitute their own type
```

Every consumer who needs a different response type must fork or wrap the
class. The fix is not an abstract creator hierarchy — it is making that one
constructor call a *slot*.

## Steps

1. **Find the buried constructor call** — the `SomeClass(...)` inside a method
   that callers wish they could change.
2. **Ask first: can the object be passed in?** If the helper can exist before
   the work starts, add a constructor parameter and inject it. Done — no
   factory needed.
3. **Otherwise, lift the call into a class attribute**:
   `response_class: Callable[[str], FeedResponse] = FeedResponse`. The method
   body becomes `self.response_class(raw)`.
4. **Type the slot with `Callable`, not a class.** `type[FeedResponse]` rejects
   functions and partials; `Callable[[str], FeedResponse]` accepts every
   factory shape mypy can hold.
5. **Add the per-instance override** — an optional constructor argument that
   assigns over the class attribute. Tests then swap doubles in without
   subclassing.

```python
from patterns.creational.factory_method import factory_slot
from patterns.creational.factory_method.examples.feed_client import (
    FeedClient,
    parse_strictly,
)

FeedClient(transport, response_class=parse_strictly)  # per-instance


class StrictClient(FeedClient):  # or per-subclass; factory_slot because
    response_class = factory_slot(parse_strictly)  # a bare function would bind
```

## Python idioms that keep it small

- **`factory_slot` (a `staticmethod` wrapper) around non-class defaults** on
  the class attribute — without it, Python would bind a plain function as a
  method and pass `self`.
- **`functools.partial` is a configured factory**: `partial(FeedResponse, ...)`
  slots in wherever the factory shape is expected — wrapped in `factory_slot`
  when assigned in a class body.
- Class attributes are inherited: a subclass overrides *only* the factory and
  inherits the whole workflow — that is the entire GoF promise, one line long.

## Pitfalls

- **Forgetting `staticmethod`** on a function-valued class attribute — the
  classic surprise `TypeError` when `self` sneaks into the call.
- **Typing the slot as a concrete class** shuts out functions, partials, and
  lambdas — the flexibility was the point.
- **Deferring what never varies.** A slot nobody overrides is indirection
  debt; inline it until a second builder actually exists.
- **Doing real work in the factory.** Factories build; if the slot starts
  validating or fetching, it has become a strategy — name it as one.

## Worked example

[`examples/feed_client/`](../examples/feed_client/) is a miniature
`http.client`: a framework class whose `response_class` slot is overridden by
subclass, by instance, and by a test double — run it with:

```bash
uv run python -m patterns.creational.factory_method.examples.feed_client.main
```
