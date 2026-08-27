# Strategy — where it lives outside this repo

Cited, real implementations to study (or point an agent at) when designing or
reviewing strategy-shaped code.

## Python standard library

- **`sorted(key=...)` / `list.sort`.** The key function is an interchangeable
  ordering algorithm passed as an argument — the pattern with zero ceremony.
  `functools.cmp_to_key` adapts old-style comparator strategies into key
  strategies.
  [docs.python.org/3/howto/sorting.html](https://docs.python.org/3/howto/sorting.html)
- **`logging.Formatter`.** A formatting strategy injected into handlers;
  swapping output formats is constructing a different formatter, not
  subclassing the handler.
  [docs.python.org/3/library/logging.html#formatter-objects](https://docs.python.org/3/library/logging.html#formatter-objects)

## Major ecosystems

- **requests custom authentication.** Anything callable can be passed as
  `auth=`; `AuthBase` subclasses are strategy objects attached per-request —
  the "strategy carries state" case done right.
  [requests.readthedocs.io/en/latest/user/advanced/#custom-authentication](https://requests.readthedocs.io/en/latest/user/advanced/#custom-authentication)
- **Django password hashers.** `PASSWORD_HASHERS` is a configured, ordered
  family of hashing algorithms; verification tries them by preference and
  upgrades stored hashes — a registry of strategies plus a selection policy.
  [docs.djangoproject.com/en/stable/topics/auth/passwords/](https://docs.djangoproject.com/en/stable/topics/auth/passwords/)
- **Fluent Python's strategy→function refactor (Ramalho).** The canonical
  written account of the class-hierarchy-to-functions collapse; this unit's
  promotions example descends from it.

## What to notice across all of them

None of these define a `Strategy` interface with one method — the signature
*is* the interface. And each pairs the family with an explicit **selection
policy** (first match, best score, configured order): when reviewing
strategy code, find where selection happens and check it is deliberate and
tested, not an accident of iteration order.
