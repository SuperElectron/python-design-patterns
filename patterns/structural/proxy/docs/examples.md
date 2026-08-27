# Proxy — where it lives outside this repo

Cited, real implementations to study (or point an agent at) when designing or
reviewing proxy-shaped code.

## Python standard library

- **`weakref.proxy`.** Forwards everything to its referent without keeping
  it alive; raises `ReferenceError` once the referent is collected — a
  lifetime-mediating proxy in the box.
  [docs.python.org/3/library/weakref.html#weakref.proxy](https://docs.python.org/3/library/weakref.html#weakref.proxy)
- **`functools.cached_property`.** The virtual proxy shrunk to its minimal
  honest size: one attribute, computed on first access, cached after.
  [docs.python.org/3/library/functools.html#functools.cached_property](https://docs.python.org/3/library/functools.html#functools.cached_property)
- **`unittest.mock.Mock`.** A stand-in you interrogate afterwards — the
  smart-reference flavor: every access recorded, assertions available.
  [docs.python.org/3/library/unittest.mock.html](https://docs.python.org/3/library/unittest.mock.html)

## Major ecosystems

- **Werkzeug `LocalProxy`** (Flask's `request` and `g`). Module-level names
  that forward to context-local objects per request — remote-ish proxies to
  "wherever the current context keeps it".
  [werkzeug.palletsprojects.com/en/stable/local/](https://werkzeug.palletsprojects.com/en/stable/local/)
- **Django `SimpleLazyObject`** and lazy `QuerySet` evaluation. Virtual
  proxies in a mainstream ORM: `request.user` is built only if touched;
  querysets hit the database only when iterated.
  [docs.djangoproject.com/en/stable/ref/models/querysets/#when-querysets-are-evaluated](https://docs.djangoproject.com/en/stable/ref/models/querysets/#when-querysets-are-evaluated)
- **`wrapt` / `lazy-object-proxy`.** Production-grade generic proxies whose
  documentation is largely about the dunder problem — evidence for how hard
  the full disguise really is.
  [wrapt.readthedocs.io](https://wrapt.readthedocs.io/)

## What to notice across all of them

Each one mediates exactly one concern (lifetime, laziness, context,
recording), none pretend the disguise is complete — `weakref.proxy`
documents which operations see through it, Werkzeug documents `isinstance`
behavior — and the ones that must survive dunders (`wrapt`) pay a whole
library's worth of effort for it.
