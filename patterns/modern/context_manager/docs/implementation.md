# Context Manager — implementation guide

## The smell that calls for it

The same `try/finally` shape appears at more than one call site; a code
review comment says "don't forget to close/unlock/restore this"; a bug
report shows cleanup skipped on the exception path.

## Introducing it, step by step

1. **Name the pair.** What exactly is acquired, and what must run on exit?
   If you cannot state the release in one sentence, the block is doing too
   much to manage.
2. **Pick the form** (see [fundamentals](fundamentals.md)): branching exit
   logic → protocol class; one unconditional cleanup → generator form;
   a runtime-sized set of cleanups → `ExitStack`.
3. **Write the exception path first.** The manager exists for the failure
   case: decide what a mid-block exception means (discard? restore? both?)
   and test that before the happy path.
4. **Keep `__enter__` cheap and `__exit__` unconditional.** Acquisition
   failures should raise *before* the body runs; release must not depend on
   how far the body got.
5. **Replace the call sites** with `with`, deleting their hand-rolled
   `try/finally`. The diff should only remove lines.

## Idioms

- Generator form: the `yield` inside `try/finally`, always — the unit's
  first caveat exists because the failure is silent otherwise.
- `ExitStack.callback(undo, ...)` per step, then `pop_all()` on success:
  transactional multi-step work where the commit is "don't run the undos"
  (shown in [atomic_deploy](../examples/atomic_deploy/deploy.py)).
- A context manager that is also a decorator: subclass
  `contextlib.ContextDecorator`, or stack `@contextmanager` functions.
- `contextlib.suppress(SomeError)` instead of `try/except: pass` — the
  intent gets a name.

## Pitfalls

- **`yield` outside `try/finally`** in a generator manager: cleanup runs
  only on the success path. The most common real-world defect in this
  pattern.
- **Returning `True` from `__exit__`** (or swallowing in `finally`):
  exceptions vanish. Only `contextlib.suppress`-style managers should ever
  do it, and loudly.
- **Doing work in `__init__`.** Acquire in `__enter__`, or the manager
  cannot be reused and fails before the `with` can protect it.
- **One giant manager** for several unrelated resources — compose small
  ones with `ExitStack` instead; each stays testable alone.
