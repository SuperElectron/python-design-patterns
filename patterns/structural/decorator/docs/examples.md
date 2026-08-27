# Decorator — where it lives outside this repo

Cited, real implementations to study (or point an agent at) when designing or
reviewing decorator-shaped code.

## Python standard library

- **`functools.lru_cache` / `functools.cache`.** Memoization as a decorator —
  wrap a function, gain a cache and `cache_info()` statistics. The pattern
  shipping in the box.
  [docs.python.org/3/library/functools.html#functools.lru_cache](https://docs.python.org/3/library/functools.html#functools.lru_cache)
- **`functools.wraps`.** A decorator whose only job is making other decorators
  honest — it copies the wrapped function's identity onto the wrapper.
  [docs.python.org/3/library/functools.html#functools.wraps](https://docs.python.org/3/library/functools.html#functools.wraps)
- **`contextlib.contextmanager`.** Wraps a generator into a context manager —
  a decorator that changes the *kind* of the thing it wraps.
  [docs.python.org/3/library/contextlib.html#contextlib.contextmanager](https://docs.python.org/3/library/contextlib.html#contextlib.contextmanager)

## Major ecosystems

- **Flask routing.** `@app.route("/path")` registers view functions into the
  URL map at definition site — decorator as registration API.
  [flask.palletsprojects.com/en/stable/quickstart/#routing](https://flask.palletsprojects.com/en/stable/quickstart/#routing)
- **Django's `@login_required`.** Access control layered onto views without
  touching them.
  [docs.djangoproject.com/en/stable/topics/auth/default/#the-login-required-decorator](https://docs.djangoproject.com/en/stable/topics/auth/default/#the-login-required-decorator)
- **`tenacity`.** Production retry policies (backoff, jitter, stop conditions)
  stacked onto callables — this unit's `retry` grown up.
  [tenacity.readthedocs.io](https://tenacity.readthedocs.io/)
- **`click`.** Whole CLIs built by stacking `@click.command` and
  `@click.option` — decorators composing a program's surface.
  [click.palletsprojects.com](https://click.palletsprojects.com/)

## What to notice across all of them

Every one preserves the wrapped callable's contract (arguments in, result
out) and adds exactly one concern beside it. And every serious one calls
`functools.wraps` — check for it first when reviewing any hand-rolled
decorator.
