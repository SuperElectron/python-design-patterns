# Memento — where it lives outside this repo

Cited, real implementations to study (or point an agent at) when designing or
reviewing snapshot/rollback code.

## Python standard library

- **`dataclasses.replace` + frozen dataclasses.** Immutability makes
  snapshots free: `replace` builds the next state, the previous object *is*
  the memento. The foundation this module's `History` assumes.
  [docs.python.org/3/library/dataclasses.html#dataclasses.replace](https://docs.python.org/3/library/dataclasses.html#dataclasses.replace)
- **`pickle` / `copy.deepcopy`.** `pickle.dumps` produces an opaque snapshot
  restorable with `loads`, even in another process; `deepcopy` is the
  in-memory equivalent for state you can't freeze. **Security (CWE-502):**
  `pickle.loads` executes code while deserializing — only unpickle snapshots
  your own process produced and stored where untrusted input cannot reach;
  use JSON for anything crossing a trust boundary.
  [docs.python.org/3/library/pickle.html#module-pickle](https://docs.python.org/3/library/pickle.html#module-pickle)

## Databases

- **SQLAlchemy `Session.begin_nested()`** — a SAVEPOINT as a memento:
  checkpoint mid-transaction, roll back to it on failure while the outer
  transaction survives. The validate-or-rollback flow of the mini-project,
  at database scale.
  [docs.sqlalchemy.org/en/latest/orm/session_transaction.html#using-savepoint](https://docs.sqlalchemy.org/en/latest/orm/session_transaction.html#using-savepoint)
- **SQLite `SAVEPOINT`** — the same idea in the database the stdlib ships.
  [sqlite.org/lang_savepoint.html](https://sqlite.org/lang_savepoint.html)

## Everyday tools

- **Editor undo persistence** — Vim's undo files (`:help undo-persistence`)
  are mementos written to disk: state snapshots that outlive the process.
  *(unverified)*

## What to notice across all of them

Each one keeps the caretaker ignorant: the SAVEPOINT name, the pickle bytes,
the undo file are all opaque handles. The moment restoring requires
*interpreting* the snapshot, you are maintaining two copies of the object's
logic — the pattern's encapsulation promise is the part worth defending.
