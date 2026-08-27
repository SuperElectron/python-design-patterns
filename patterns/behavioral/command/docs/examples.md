# Command — where it lives outside this repo

Cited, real implementations to study (or point an agent at) when designing or
reviewing command-shaped code.

## Python standard library

- **`functools.partial`** — the execute-only half of the pattern as a
  builtin: a call and its arguments packaged into one object.
  [docs.python.org/3/library/functools.html#functools.partial](https://docs.python.org/3/library/functools.html#functools.partial)
- **`sched.scheduler`** — queues `Event` records (time, priority, sequence,
  action, argument, kwargs) — commands with metadata — and its run loop is
  the invoker.
  [docs.python.org/3/library/sched.html](https://docs.python.org/3/library/sched.html)
- **`unittest.mock.call`** — recorded invocations as inspectable, comparable
  objects: the audit-log face of the pattern.
  [docs.python.org/3/library/unittest.mock.html#unittest.mock.call](https://docs.python.org/3/library/unittest.mock.html#unittest.mock.call)

## Major ecosystems

- **Django migration operations.** Each operation implements
  `database_forwards` *and* `database_backwards` — execute plus undo — and
  the migration executor is an invoker replaying them in order, either way.
  [docs.djangoproject.com/en/stable/ref/migration-operations/](https://docs.djangoproject.com/en/stable/ref/migration-operations/)
- **Qt's `QUndoCommand` / `QUndoStack`** (exposed by PyQt/PySide) — the
  canonical GUI undo architecture: commands with `redo()`/`undo()`, an
  invoker stack with exactly the clear-redo-on-push contract this module's
  `UndoStack` implements. [doc.qt.io/qt-6/qundocommand.html](https://doc.qt.io/qt-6/qundocommand.html) *(unverified)*
- **Celery tasks.** A task invocation serialized onto a broker queue is the
  pattern at distributed scale: the worker (invoker) executes requests it
  never saw created. [docs.celeryq.dev](https://docs.celeryq.dev/) *(unverified)*

## What to notice across all of them

The dividing line is always the same: plain callables until requests need to
be *stored, inspected, or reversed*, objects after. Django's migrations and
Qt's undo stack both pay the class-per-operation cost precisely because they
need the backwards direction — and neither uses a command class where a
forward-only callback would do.
