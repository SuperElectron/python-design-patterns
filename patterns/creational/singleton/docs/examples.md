# Singleton — where it lives outside this repo

Cited, real implementations to study (or point an agent at) when designing or
reviewing shared-instance code.

## Python standard library

- **`None`, `Ellipsis`, `NotImplemented`.** Interpreter-level singletons —
  each has exactly one instance, which is why `is` comparison against them is
  the correct idiom.
  [docs.python.org/3/library/constants.html](https://docs.python.org/3/library/constants.html)
- **Modules themselves.** `import` consults `sys.modules` and returns the
  cached module object; every module is a built-once, process-wide instance.
  That cache is what the Global Object pattern rides.
  [docs.python.org/3/reference/import.html#the-module-cache](https://docs.python.org/3/reference/import.html#the-module-cache)
- **`logging.getLogger(name)`.** One logger per name, cached by a hidden
  manager — the accessor form of the pattern, shipped in the stdlib.
  [docs.python.org/3/library/logging.html#logging.getLogger](https://docs.python.org/3/library/logging.html#logging.getLogger)

## Major ecosystems

- **`django.conf.settings`.** A lazily-built global object behind a module
  attribute — Django needs configure-then-build ordering, exactly the case
  for the accessor/lazy form rather than import-time construction.
  *(unverified source link)*
  [docs.djangoproject.com/en/stable/topics/settings/](https://docs.djangoproject.com/en/stable/topics/settings/)
- **The guide's chapter** on the pattern's history and why Python rarely
  needs the class-based form.
  [python-patterns.guide/gang-of-four/singleton/](https://python-patterns.guide/gang-of-four/singleton/)

## What to notice across all of them

Nothing in production Python intercepts `__new__` to enforce oneness. The
stdlib and Django both reach for *a cache plus an accessor* — uniqueness is a
property of where the object is stored, not of its class. And each one has an
answer to test isolation (logging's per-name registry, Django's
`override_settings`) — when reviewing shared-instance code, ask where the
reset seam is.
