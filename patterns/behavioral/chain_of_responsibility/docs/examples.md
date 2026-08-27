# Chain of Responsibility — where it lives outside this repo

Cited, real implementations to study (or point an agent at) when designing or
reviewing chain-shaped code.

## Python standard library

- **`logging` propagation.** A record emitted on a child logger climbs the
  dot-separated logger hierarchy, offered to each ancestor's handlers until
  `propagate` stops it — a chain wired by naming convention.
  [docs.python.org/3/library/logging.html#logging.Logger.propagate](https://docs.python.org/3/library/logging.html#logging.Logger.propagate)
- **`urllib.request.OpenerDirector`.** Openers hold an ordered list of
  `BaseHandler`s; each protocol method is tried on each handler in order until
  one returns a non-`None` response — decline-by-`None`, exactly this module's
  contract. [docs.python.org/3/library/urllib.request.html#urllib.request.OpenerDirector](https://docs.python.org/3/library/urllib.request.html#urllib.request.OpenerDirector)

## Major ecosystems

- **Django middleware.** Requests descend an ordered middleware stack; any
  layer may short-circuit by returning a response, otherwise it delegates
  inward. Ordering is explicit configuration (`MIDDLEWARE`), and the docs
  discuss it as policy.
  [docs.djangoproject.com/en/stable/topics/http/middleware/](https://docs.djangoproject.com/en/stable/topics/http/middleware/)
- **pluggy `firstresult` hooks** (the engine under pytest). Hook
  implementations run in registration order until the first non-`None` result
  wins — Chain of Responsibility offered as a library feature flag.
  [pluggy.readthedocs.io/en/stable/#first-result-only](https://pluggy.readthedocs.io/en/stable/#first-result-only)
- **WSGI middleware (PEP 3333).** Applications wrap applications; each layer
  answers or passes inward. The chain here is built by function composition
  rather than a list.
  [peps.python.org/pep-3333/](https://peps.python.org/pep-3333/)

## What to notice across all of them

Every production example makes two decisions the GoF text leaves open: the
**decline convention** (`None`, `propagate=False`, "call the next app") and
the **unhandled policy** (logging's `lastResort` handler, urllib raising
`URLError`, Django's 404). When reviewing chain code, check both are explicit.
