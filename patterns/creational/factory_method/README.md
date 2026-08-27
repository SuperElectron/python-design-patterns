---
id: creational/factory_method
name: Factory Method
aliases: [virtual-constructor, class-attribute-factory]
guide_url: https://python-patterns.guide/gang-of-four/factory-method/
problem: "Let a class defer which helper object it constructs, so subclasses or callers can substitute another."
symptoms: ["subclass to change what gets built", "framework builds objects the app must customize", "response_class-style override"]
verdict: prefer-alternative
caveats:
  - "The guide's dodge is Dependency Injection: if you already have the object, pass the object, not a method that builds it."
  - "When creation must stay inside the class, prefer a class attribute factory (override by assignment or subclass) over an abstract method — any callable can be plugged in."
stdlib_sightings: [http.client.HTTPConnection.response_class, json.JSONDecoder]
---

# Factory Method

Let a class defer which helper it constructs, so subclasses, callers, or tests
substitute another. **Verdict: prefer an alternative** — inject the object, or
make the constructor call a class-attribute slot; the abstract-method form is
Java with the serial numbers filed off.

| Where | What |
|---|---|
| [`pattern/`](pattern/) | The importable code: `factory_slot` (trap-safe class-attribute factories) and the `Factory` alias; the three dodges — injection, class-attribute slot, instance override — documented best first |
| [`docs/`](docs/) | [Fundamentals](docs/fundamentals.md) · [Implementation guide](docs/implementation.md) · [External examples](docs/examples.md) |
| [`examples/feed_client/`](examples/feed_client/) | Mini-project: a feed-client framework with a `response_class` slot |
| [`tests/`](tests/) | Behavioral tests for the pattern and the mini-project |

```bash
uv run python -m patterns.creational.factory_method.examples.feed_client.main
```
