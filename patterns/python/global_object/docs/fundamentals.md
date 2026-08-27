# Global Object — fundamentals

## Intent

Give a whole program shared access to a constant or a pre-built object by
assigning it once at module level. A Python module is created once and cached
in `sys.modules`, so a module-level name **is** the language's native shared
instance — this pattern is what Singleton actually wants to be in Python.
Source chapter: [python-patterns.guide/python/module-globals](https://python-patterns.guide/python/module-globals/).

## Participants

| Role | What it is |
|---|---|
| The module | The shared namespace, constructed exactly once per process |
| Constants | Immutable values named at module level (`RETRY_LIMIT = 3`) |
| Prebuilt objects | Cheap, pure import-time construction (a compiled regex, a parsed table) |
| The lazy global | Expensive construction deferred to first use — `Lazy` in [`pattern/lazy.py`](../pattern/lazy.py) |
| Importers | Every consumer; they share the one instance by importing the name |

## Mechanism

1. Truly constant values are assigned at module level and never mutated.
2. Objects that are cheap and *pure* to build (no I/O, deterministic) may be
   built at import time.
3. Anything expensive — file parses, network, big tables — goes behind a lazy
   accessor: importing costs nothing, the first `get()` pays once, and
   `reset()` restores test order-independence.
4. Mutable module globals are reserved for objects whose mutation is their
   documented job (`os.environ`), never an accident of convenience.

## The classic misuses, and the discipline that replaces them

The pattern is defined as much by what it forbids as what it allows. The two
classic misuses:

```python
# Misuse 1: hidden mutable state — every caller is coupled to every other.
_counts: dict[str, int] = {}


def tally(word: str) -> int:
    _counts[word] = _counts.get(word, 0) + 1  # tests now order-dependent
    return _counts[word]


# Misuse 2: work at import time — every importer pays, before anyone asks.
CATALOG = json.load(open("catalog.json"))  # I/O on import: slow, fragile
```

The first couples strangers through invisible state and makes test order
matter. The second makes `import` slow, order-dependent, and untestable — the
guide's hardest rule is **never do I/O at import time**. The discipline:
constants freely, pure-and-cheap prebuilt objects freely, everything else
lazily, mutation only where mutation is the documented contract.

## When to use it

- A value many modules need, whose identity should be shared (config, a
  compiled regex, a lookup table, a client object).
- You are about to write a Singleton class — a module global is the same
  guarantee without the ceremony.

## When not to use it

- The value differs per request/test/tenant → pass it explicitly (see
  `modern/dependency_injection`).
- Callers need to mutate it and mutation is not the object's documented
  purpose → the coupling will outlive whoever wrote it.

## Verdict: use with care

Constants and immutable prebuilt objects: freely. Expensive things: behind
`Lazy`. Mutable globals: only when shared mutation is the feature — and the
docs say so.
