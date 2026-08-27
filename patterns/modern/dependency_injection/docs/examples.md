# Dependency Injection — where it lives outside this repo

Cited, real implementations to study (or point an agent at) when designing or
reviewing injection seams.

## Python standard library

- **`sorted(key=...)` / `min` / `max`.** The ordering policy is injected as a
  callable — micro-DI so idiomatic nobody calls it a pattern.
  [docs.python.org/3/library/functions.html#sorted](https://docs.python.org/3/library/functions.html#sorted)
- **`json.dumps(cls=...)`.** The encoder is a constructor-injected
  collaborator with a production default (`JSONEncoder`).
  [docs.python.org/3/library/json.html](https://docs.python.org/3/library/json.html)
- **`unittest.mock`.** The other half of the pattern: the fakes that exist to
  be injected through the seams you left.
  [docs.python.org/3/library/unittest.mock.html](https://docs.python.org/3/library/unittest.mock.html)

## Major ecosystems

- **pytest fixtures.** Injection driven by argument *name*: declaring a
  parameter called `tmp_path` is asking the framework to construct and pass
  one — a composition root run per test.
  [docs.pytest.org/en/stable/how-to/fixtures.html](https://docs.pytest.org/en/stable/how-to/fixtures.html)
- **FastAPI `Depends`.** Request-scoped DI as a framework feature; the
  declared dependency graph is resolved per call, with overrides for tests.
  [fastapi.tiangolo.com/tutorial/dependencies/](https://fastapi.tiangolo.com/tutorial/dependencies/)
- **Fowler's taxonomy.** Constructor vs setter vs interface injection, and why
  containers exist at all — the vocabulary the industry still uses.
  [martinfowler.com/articles/injection.html](https://martinfowler.com/articles/injection.html)

## What to notice across all of them

None of the Python examples involve a container: the language's keyword
arguments and structural typing carry the whole pattern. When reviewing,
look for the two failure directions — a seam that is missing (tests patch
internals) and seams that are gratuitous (constructors as wiring diagrams).
