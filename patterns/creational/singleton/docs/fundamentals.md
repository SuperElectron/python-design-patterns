# Singleton — fundamentals

## Intent

Guarantee a class has exactly one instance and give the whole program access
to it — a configuration object, a connection pool, a process-wide registry.

## Participants

| Role | Classic (GoF) form | Python form |
|---|---|---|
| The single instance | Cached on the class by an overridden `__new__` | An ordinary object at module level, or behind `Shared` in [`pattern/shared.py`](../pattern/shared.py) |
| Global access point | Calling the constructor (`Logger()`) — which lies | `import` the object, or call a small accessor (`get_settings()`) |
| Laziness | The `__new__` cache check | The accessor builds on first call |
| Test isolation | None — the hidden instance leaks between tests | An explicit `reset()` seam |

## Mechanism

1. The instance lives in exactly one place the process agrees on.
2. Everyone reaches it the same way — import or accessor — instead of
   constructing their own.
3. Python already runs this mechanism for you: a module is created once,
   cached in `sys.modules`, and every `import` returns the same object. The
   Global Object pattern rides that.

## The classic form, and what Python absorbs

The textbook version intercepts construction:

```python
class Logger:
    _instance: ClassVar[Self | None] = None

    def __new__(cls) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        # __init__ still runs on EVERY Logger() call — without this
        # guard, a second call wipes the state.
        if not hasattr(self, "lines"):
            self.lines: list[str] = []
```

Note the two warts Python forces on it: callers still *look* like they're
constructing, and `__init__` re-runs per call, so the class must defend its
own state. All of that machinery buys what a module-level assignment already
has:

```python
logger = Logger()  # the Global Object: built once, import it
```

## When to use it

- One process-wide resource genuinely wanted by everything (settings, a
  metrics sink) → module global or `Shared` accessor.
- Construction must be deferred (reads env/files, needs configuration first)
  → the accessor form, which is also where a lock goes if threads race.

## When not to use it

- The "global" is only shared by a few collaborators → pass it (dependency
  injection); globals are a convenience, not an architecture.
- You want swappable implementations in tests → inject, or at minimum keep
  the reset seam; a hidden class-cached instance makes tests order-dependent.
- Interpreter-level uniqueness (`None`-style sentinels) → see the
  sentinel_object unit; that's a different job.

## Verdict: prefer an alternative

A module is already a singleton. Write a module-level instance, or `Shared`
when construction must wait — and keep the reset seam, because the classic
form's real cost lands in your test suite.
