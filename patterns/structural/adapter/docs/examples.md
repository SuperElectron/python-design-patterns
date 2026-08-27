# Adapter — where it lives outside this repo

Cited, real implementations to study (or point an agent at) when designing or
reviewing adapter-shaped code.

## Python standard library

- **`io.TextIOWrapper`** — the stdlib's flagship adapter: wraps a binary
  stream and exposes the text-file interface; your code reads `str` while
  bytes flow underneath.
  [docs.python.org/3/library/io.html#io.TextIOWrapper](https://docs.python.org/3/library/io.html#io.TextIOWrapper)
- **`functools.cmp_to_key`** — adapts an old-style two-argument comparator to
  the one-argument `key=` interface; an entire adapter in function form.
  [docs.python.org/3/library/functools.html#functools.cmp_to_key](https://docs.python.org/3/library/functools.html#functools.cmp_to_key)
- **`socket.makefile()`** — adapts a socket to a file-like object so
  file-consuming code can speak to the network.
  [docs.python.org/3/library/socket.html#socket.socket.makefile](https://docs.python.org/3/library/socket.html#socket.socket.makefile)

## Major ecosystems

- **`requests` transport adapters.** `HTTPAdapter` adapts urllib3's
  connection machinery to the `Session` API, and users mount custom adapters
  per URL prefix — the pattern offered as a public extension point.
  [requests.readthedocs.io/en/latest/user/advanced/#transport-adapters](https://requests.readthedocs.io/en/latest/user/advanced/#transport-adapters)
- **SQLAlchemy dialects.** Each dialect adapts one DBAPI driver's quirks
  (paramstyles, type handling) to a single Core interface, which is why one
  query API spans many databases.
  [docs.sqlalchemy.org/en/20/dialects/](https://docs.sqlalchemy.org/en/20/dialects/)

## What to notice across all of them

Every production adapter translates *conventions*, not just method names:
`cmp_to_key` bridges calling conventions, `TextIOWrapper` bridges data
models (bytes vs text), dialects bridge error hierarchies. When reviewing an
adapter, ask what happens to the adaptee's failure modes — an adapter that
only renames methods has usually left the hard mismatch in the client.
