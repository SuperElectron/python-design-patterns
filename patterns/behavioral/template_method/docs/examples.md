# Template Method — where it lives outside this repo

Cited, real implementations to study (or point an agent at) when designing or
reviewing template-shaped code.

## Python standard library

- **`json.JSONEncoder.default`.** `encode()` owns the encoding skeleton and
  calls your `default()` hook exactly at the step it cannot handle — the
  template method most Python developers have already overridden.
  [docs.python.org/3/library/json.html#json.JSONEncoder.default](https://docs.python.org/3/library/json.html#json.JSONEncoder.default)
- **`unittest.TestCase.setUp` / `tearDown`.** The runner owns the fixed run
  loop (setUp → test → tearDown, with error policy); you own the hooks.
  [docs.python.org/3/library/unittest.html#unittest.TestCase.setUp](https://docs.python.org/3/library/unittest.html#unittest.TestCase.setUp)
- **`socketserver.BaseRequestHandler.handle`.** Accept loop, request
  lifecycle, and cleanup are fixed by the framework; `handle()` is the one
  step handed to you.
  [docs.python.org/3/library/socketserver.html](https://docs.python.org/3/library/socketserver.html)

## Major ecosystems

- **Django class-based views.** The request pipeline (`dispatch` → handler →
  response) is fixed; `get_queryset`, `get_context_data` and friends are the
  named hooks — the subclass form at a true framework boundary.
  [docs.djangoproject.com/en/stable/topics/class-based-views/](https://docs.djangoproject.com/en/stable/topics/class-based-views/)
- **Scrapy spiders.** The crawl loop, scheduling, and retries belong to the
  framework; `parse()` is your extraction step.
  [docs.scrapy.org](https://docs.scrapy.org/)

## What to notice across all of them

Every citation above is a *framework* boundary: the code that owns the loop
and the code that owns a step are maintained by different people — that
asymmetry is what justifies subclass hooks. Inside one codebase that
asymmetry is absent, and passing callables (this unit's `Skeleton`) gives the
same fixed spine with composition instead of a class per variant. When
reviewing, ask who owns the loop: someone else → hooks are fine; you → pass
the steps.
