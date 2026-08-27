# Context Manager — fundamentals

## Intent

Guarantee that acquire and release are paired around a block of code on
*every* exit path — normal return, early return, exception. The `with`
statement (PEP 343) makes the pairing structural instead of disciplinary:
cleanup lives with the acquisition, written once, not re-written correctly
at every call site.

## Participants

| Role | Form | Where |
|---|---|---|
| The protocol | `__enter__` / `__exit__` on a class | `AtomicWrite` in [`pattern/managers.py`](../pattern/managers.py) |
| The generator form | `@contextlib.contextmanager` around a `yield` | `temporarily` in the same module |
| Composition | `contextlib.ExitStack` — a dynamic pile of managers | the [atomic_deploy example](../examples/atomic_deploy/) |
| Client | `with manager as value:` | any block needing the guarantee |

## Mechanism

1. `with` calls `__enter__`; its return value binds to `as`.
2. The body runs.
3. `__exit__` runs *no matter how the body ended*, receiving the exception
   triple (or three `None`s). Returning falsy re-raises; returning `True`
   swallows the exception — do that only on purpose.
4. In the generator form, the `yield` is the seam: code before it is
   `__enter__`, code after it is `__exit__` — which is why the `yield` must
   sit inside `try/finally`, or an exception in the body skips the cleanup.

## The classic form, and what Python absorbs

Before `with`, the guarantee was hand-written `try/finally` at every call
site — correct, and unscalable:

```python
def use_two(log: list[str]) -> None:
    first = Resource("a", log)
    try:
        second = Resource("b", log)  # every extra resource nests a level
        try:
            log.append("work")
        finally:
            second.close()
    finally:
        first.close()
```

The `with` statement absorbs the nesting and the discipline; `contextlib`
absorbs the boilerplate of writing managers; `ExitStack` absorbs the
"unknown number of resources" case. What remains — the pattern — is spotting
the acquire/release pair and choosing the right construction form for it.

## Choosing the form

- **Protocol class** when exit logic branches (commit vs discard, like
  `AtomicWrite`), when the manager has state worth naming, or when it must
  be re-entered.
- **Generator form** when cleanup is one unconditional restore
  (`temporarily`) — three lines instead of a class.
- **`ExitStack`** when how many managers you need is a runtime fact, or
  when you want callbacks-as-cleanup with `pop_all()` as the commit.

## When not to use it

- No release side exists — a plain function is enough.
- The "cleanup" must survive the process (a saga, a queued compensation) —
  that is workflow logic, not block scoping.

## Verdict: pythonic

This *is* Python's RAII, made explicit. Any acquire/release pair you write
twice deserves a context manager; the two caveats (yield inside
`try/finally`; returning `True` from `__exit__` swallows) are the only
sharp edges.
