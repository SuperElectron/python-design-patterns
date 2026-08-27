# Proxy — fundamentals

## Intent

Provide a surrogate for another object to control access to it. The proxy
offers the subject's interface but mediates: deferring construction
(virtual), guarding operations (protection), observing traffic (smart
reference), or standing in for something remote.

## Participants

| Role | Classic (GoF) form | Python form |
|---|---|---|
| Subject | Abstract interface proxy and real object share | No interface needed — `__getattr__` forwards anything |
| Real subject | The expensive/guarded/remote object | Same |
| Proxy | Implements the interface, holds the real subject | A dozen-line forwarding class — see [`pattern/proxies.py`](../pattern/proxies.py) |

## Mechanism

1. The proxy holds (or knows how to build) the subject.
2. Attribute access hits the proxy first; it applies its one mediation.
3. Then it forwards to the subject with plain `getattr`.
4. Proxies are objects too, so mediations stack — metering over protection
   over laziness is three small classes composed, not one class with flags.

## The classic form, and what Python absorbs

The book's virtual proxy shares an abstract interface with its subject and
re-implements every method as a forwarding stub:

```python
class Report(ABC):
    @abstractmethod
    def summary(self) -> str: ...


class ReportProxy(Report):  # same interface, by inheritance
    def __init__(self) -> None:
        self._real: ExpensiveReport | None = None

    def summary(self) -> str:  # one stub per subject method
        if self._real is None:
            self._real = ExpensiveReport()
        return self._real.summary()
```

Python absorbs the ceremony twice. `__getattr__` — called only when normal
lookup fails — forwards the *entire* surface in one method, no shared
interface required. And when the real goal is "compute this one attribute
lazily", `functools.cached_property` is the whole pattern at the right size.
What Python does **not** absorb is the disguise: `isinstance` checks,
identity comparisons, and dunder lookups (which bypass `__getattr__`
entirely) all see through the proxy. That caveat leads this unit.

## When to use it

- Construction is genuinely expensive and often unnecessary (virtual).
- Operations need per-caller mediation — permissions, quotas, audit
  (protection / smart reference).
- Several mediations must compose over one subject — the case a single
  `cached_property` can't cover.

## When not to use it

- One lazily computed attribute → `functools.cached_property`.
- The mediation is per-*call* on known functions → that's a decorator; see
  `structural/decorator`.
- Code downstream relies on `isinstance`/identity of the subject — the
  disguise will leak, and dunder-dependent protocols (`len`, iteration,
  context managers) won't forward.

## Verdict: use with care

Powerful where laziness or mediation is real; the skin-deep disguise is the
tax. Production-grade generic proxies (`wrapt`) exist precisely because the
dunder problem is hard — reach for them before hand-rolling cleverness.
