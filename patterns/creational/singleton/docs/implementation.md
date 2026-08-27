# Singleton — putting it into a system

## The smell it fixes

Every module constructing its own copy of a process-wide resource — or the
opposite failure, a class enforcing oneness through `__new__` gymnastics that
break in review and in tests:

```python
class Config:
    _instance = None

    def __new__(cls):  # clever, hidden, test-hostile
        ...
```

## Steps

1. **Write the class as if it were ordinary.** Nothing about `Settings`
   should know it will be shared — that keeps it constructible in tests.
2. **Choose eager or lazy.** Cheap and configuration-free → build it at
   module level (`logger = Logger()`) and import it; done. Reads env/files or
   must be configured first → step 3.
3. **Put the instance behind `Shared(factory)`** and export a small accessor
   (`get_settings()`); the factory runs on first use only, keeping import
   side-effect-free.
4. **Export the reset seam** (`reset_settings()`), and call it in test
   setup/teardown — shared state between tests is the pattern's real tax.
5. **Keep construction injectable**: the factory reads from a *mapping
   parameter* defaulting to `os.environ`, so tests build `Settings` from a
   dict without patching globals.

```python
from patterns.creational.singleton import Shared

_shared: Shared[Settings] = Shared(load_settings)


def get_settings() -> Settings:
    return _shared.get()


def reset_settings() -> None:
    _shared.reset()
```

## Python idioms that keep it small

- **The module is the singleton.** `sys.modules` is the instance cache you
  were about to write.
- **A frozen dataclass as the shared object** removes the "who mutated the
  global?" class of bug outright.
- **`functools.partial(load_settings, canned_env)`** makes a `Shared` for
  tests without touching the real one.

## Pitfalls

- **Thread races on first build.** `Shared.get` is not locked; two threads
  can each run the factory once. Fine for value objects — wrap a lock around
  construction that opens sockets or writes files.
- **The `__new__` dance's hidden cost**: `__init__` still runs on every call,
  so state needs a guard — and everyone forgets the guard.
- **Import-time construction that does I/O** turns every importer into a
  side effect; laziness (step 3) is the fix, not deeper caching.
- **No reset seam** makes test order matter; the accessor pattern without
  `reset()` is only half the pattern.
- **Reaching for a global at all** when only two collaborators share the
  object — pass it as an argument and skip this page.

## Worked example

[`examples/app_config/`](../examples/app_config/) is process-wide settings
with lazy build, cached reads, env re-read after reset, and an injected
mapping for tests — run it with:

```bash
uv run python -m patterns.creational.singleton.examples.app_config.main
```
