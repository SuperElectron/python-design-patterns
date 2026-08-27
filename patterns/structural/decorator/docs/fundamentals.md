# Decorator — fundamentals

## Intent

Attach responsibilities to an object or callable dynamically, without editing
the original and without a subclass per combination. Wrapping composes:
logging-around-retry-around-caching is three small pieces, not one class named
`LoggingRetryingCachingClient`.

## Participants

| Role | Classic (GoF) form | Python form |
|---|---|---|
| Component | Abstract interface both sides implement | Any callable (or any object, for the wrapping form) |
| Concrete component | The real object | The function being decorated |
| Decorator | Abstract wrapper holding a component | A factory returning a closure — see [`pattern/decorators.py`](../pattern/decorators.py) |
| Concrete decorators | One subclass per added concern | `logged`, `timed`, `retry`, `rate_limited` |

## Mechanism

1. A decorator takes the component, returns something with the same interface.
2. The wrapper adds its one concern before/after delegating inward.
3. Wrappers stack; order is meaningful and chosen at composition time.
4. `functools.wraps` copies identity (`__name__`, `__doc__`, signature) so the
   stack stays introspectable.

## The classic form, and what Python absorbs

Two related shapes share the name. The GoF book wraps *objects* — a class
holding the wrapped instance, augmenting some methods, forwarding the rest:

```python
class LoggingWriter:
    """Wraps a file-like object; counts writes, forwards the rest."""

    def __init__(self, wrapped: TextIO) -> None:
        self._wrapped = wrapped
        self.writes = 0

    def write(self, text: str) -> int:  # the augmented method
        self.writes += 1
        return self._wrapped.write(text)

    def __getattr__(self, name: str) -> Any:  # wholesale forwarding
        return getattr(self._wrapped, name)
```

`__getattr__` already softens the book's forward-every-method tax — but the
wrapper still fails `isinstance` against the wrapped type (the guide's
caveat: wrapping doesn't make you the wrapped thing).

For *callables*, Python absorbed the pattern into syntax: `@decorator` above a
`def` is the whole class diagram in one line. This module's
[`pattern/`](../pattern/) ships that form, because it is the one you compose
daily. See the guide chapter:
[python-patterns.guide/gang-of-four/decorator-pattern](https://python-patterns.guide/gang-of-four/decorator-pattern/).

## When to use it

- A cross-cutting concern (logging, retries, caching, limits, auth) recurs
  around many call sites.
- You need concerns in different combinations per call site — stacking beats
  a subclass lattice.

## When not to use it

- The behavior belongs to the function itself → just write it in the function.
- You need to intercept *every* attribute of a rich object → that's a Proxy
  problem; see `structural/proxy`.
- One lazily computed value → `functools.cached_property`.

## Verdict: pythonic

For callables the pattern is idiomatic Python — the syntax exists for it.
Always apply `functools.wraps`; without it the stack destroys the wrapped
function's identity. Object wrapping is rarer: reach for it only when the
wrapped surface is wide and `__getattr__` forwarding keeps it honest.
