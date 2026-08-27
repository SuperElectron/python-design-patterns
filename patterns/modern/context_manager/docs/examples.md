# Context Manager — external examples

Real embodiments of the pattern outside this repo, for deeper study.

## Origin

- **PEP 343 — the `with` statement** — rationale and full semantics;
  the pattern's founding document. <https://peps.python.org/pep-0343/>

## Standard library

- **`contextlib`** — `contextmanager`, `ExitStack`, `suppress`, `closing`,
  `ContextDecorator`: every construction form in one module.
  <https://docs.python.org/3/library/contextlib.html>
- **`open`, locks, `tempfile.TemporaryDirectory`** — the everyday managers;
  a `with open(...)` is the pattern most Python code meets first.
- **`sqlite3.Connection`** — commit on clean exit, rollback on exception:
  the branching-exit shape `AtomicWrite` mirrors.
  <https://docs.python.org/3/library/sqlite3.html>

## Elsewhere

- **pytest yield fixtures** — setup/teardown expressed exactly as the
  generator form: code before the `yield` is setup, after is teardown.
  *(unverified)* <https://docs.pytest.org/en/stable/how-to/fixtures.html>
- **Django `transaction.atomic`** — one transaction seam usable as context
  manager or decorator. *(unverified)*
  <https://docs.djangoproject.com/en/stable/topics/db/transactions/>
