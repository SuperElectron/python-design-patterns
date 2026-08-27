# Global Object — where it lives outside this repo

Cited, real implementations to study (or point an agent at) when designing or
reviewing module-global code.

## Python standard library

- **`math.pi`, `calendar.day_name`.** The Constant Pattern and the prebuilt
  global object: computed at import, immutable in practice, shared by every
  importer. [docs.python.org/3/library/calendar.html](https://docs.python.org/3/library/calendar.html)
- **`os.environ`.** The rare *documented* mutable global — mutation is its
  entire job, which is exactly the bar a mutable module global must clear.
  [docs.python.org/3/library/os.html#os.environ](https://docs.python.org/3/library/os.html#os.environ)
- **`logging.root` and the module-logger convention.** `logger =
  logging.getLogger(__name__)` at module top is a per-module global object
  built through a cached factory.
  [docs.python.org/3/library/logging.html](https://docs.python.org/3/library/logging.html)

## Major ecosystems

- **`django.conf.settings`.** A lazy global object: importing it is free, the
  wrapped settings module materializes on first attribute access — the same
  deferral this unit's `Lazy` provides.
  [docs.djangoproject.com/en/stable/topics/settings/](https://docs.djangoproject.com/en/stable/topics/settings/)
- **The guide chapter.** The import-time-I/O prohibition, the dunder-constant
  conventions, and the Constant/Global Object distinction this unit encodes.
  [python-patterns.guide/python/module-globals](https://python-patterns.guide/python/module-globals/)

## What to notice across all of them

Every healthy global is either immutable, lazily built, or mutable *by
documented design* — there is no fourth kind in the wild. When reviewing,
classify each module global into one of the three; whatever resists
classification is the bug.
