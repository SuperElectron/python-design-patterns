# Factory Method — where it lives outside this repo

Cited, real implementations to study (or point an agent at) when designing or
reviewing factory-slot code.

## Python standard library

- **`http.client.HTTPConnection.response_class`.** The canonical
  class-attribute factory: the connection builds its response objects through
  the attribute, so a one-line subclass swaps in a custom response type.
  [docs.python.org/3/library/http.client.html](https://docs.python.org/3/library/http.client.html)
- **`json.JSONDecoder(object_hook=..., parse_float=...)`.** Instance-attribute
  factories: each decoder instance carries the callables it will use to build
  numbers and objects.
  [docs.python.org/3/library/json.html](https://docs.python.org/3/library/json.html)
- **`asyncio.loop.set_task_factory`.** A pluggable creation hook on the event
  loop — the factory is set at runtime, not baked into a subclass.
  [docs.python.org/3/library/asyncio-eventloop.html](https://docs.python.org/3/library/asyncio-eventloop.html)

## Major ecosystems

- **Flask's `Flask.response_class` and `test_client_class`.** An application
  subclass points these attributes at its own types and the framework builds
  them everywhere.
  [flask.palletsprojects.com/en/stable/api/](https://flask.palletsprojects.com/en/stable/api/)
- **The guide's chapter** ranks the dodges this unit implements and shows the
  history of the pattern in Python.
  [python-patterns.guide/gang-of-four/factory-method/](https://python-patterns.guide/gang-of-four/factory-method/)

## What to notice across all of them

None of these ship an abstract `factory_method()` — every one is an attribute
holding a callable. The variation point is *data on the class*, which is why
overriding takes one line and why tests can substitute doubles without
touching a hierarchy.
