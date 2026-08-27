# Registry — where it lives outside this repo

Cited, real implementations to study (or point an agent at) when designing or
reviewing registry-shaped code.

## Python standard library

- **`codecs.register` / `codecs.lookup`.** The encodings machinery is a full
  plugin registry: every `"text".encode(name)` is a lookup, and registered
  search functions can serve entirely new names.
  [docs.python.org/3/library/codecs.html](https://docs.python.org/3/library/codecs.html)
- **`functools.singledispatch`.** A registry keyed by *type* instead of name,
  with the same decorator registration surface and MRO-aware lookup.
  [docs.python.org/3/library/functools.html#functools.singledispatch](https://docs.python.org/3/library/functools.html#functools.singledispatch)
- **`atexit.register`.** A registry whose "dispatch" is the interpreter
  shutting down — registration as decorator, in the stdlib since forever.
  [docs.python.org/3/library/atexit.html](https://docs.python.org/3/library/atexit.html)

## Major ecosystems

- **Flask route decorators.** `@app.route("/users")` fills the URL map — a
  registry populated at import time, which is why a views module that never
  gets imported serves 404s (the caveat, in production form).
  [flask.palletsprojects.com](https://flask.palletsprojects.com/)
- **Django `admin.site.register`.** The explicit-call flavor: the admin is a
  registry of model → options, filled in each app's `admin.py` — a module
  Django deliberately auto-imports, solving the import-time problem by
  convention.
  [docs.djangoproject.com/en/stable/ref/contrib/admin/](https://docs.djangoproject.com/en/stable/ref/contrib/admin/)
- **setuptools entry points.** Registration moved out of code into package
  metadata, so plugins in *other distributions* are discoverable without any
  import — the industrial-strength answer to "a plugin nobody imports".
  [packaging.python.org/en/latest/specifications/entry-points/](https://packaging.python.org/en/latest/specifications/entry-points/)

## What to notice across all of them

Each one has an explicit answer to the two policy questions: unknown names
(`LookupError` from `codecs`, 404 from Flask) and registration time (import
side effects, auto-imported conventions, or metadata). When reviewing
registry code, find both answers; if either is implicit, that's the bug
waiting.
