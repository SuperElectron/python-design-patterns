# Prebound Method — where it lives outside this repo

Cited, real implementations to study (or point an agent at) when designing or
reviewing module-API code.

## Python standard library

- **`random`.** The flagship: `random.random`, `random.seed`, and friends are
  bound methods of one hidden `Random()` built at import, and `random.Random`
  stays public for isolated streams.
  [docs.python.org/3/library/random.html](https://docs.python.org/3/library/random.html) ·
  [source](https://github.com/python/cpython/blob/main/Lib/random.py)
- **`secrets`.** `token_hex`, `token_bytes`, `choice` come from a module-level
  `SystemRandom` instance — the same wiring with a different engine.
  [docs.python.org/3/library/secrets.html](https://docs.python.org/3/library/secrets.html)
- **`calendar`.** Module functions like `calendar.month` delegate to a
  module-level `TextCalendar` instance.
  [source](https://github.com/python/cpython/blob/main/Lib/calendar.py)

## The chapter

- The naming conventions, the import-time-cost warning, and the
  keep-the-class-public rule this unit encodes:
  [python-patterns.guide/python/prebound-methods](https://python-patterns.guide/python/prebound-methods/)

## What to notice across all of them

Every stdlib example keeps **both doors open**: the convenient module
functions for the common case, the public class for isolation. When reviewing
a module-level API over shared state, check for the second door — its absence
is tomorrow's monkeypatch.
