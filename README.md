# Python Design Patterns

Every design pattern as a fluent Python developer would actually write it —
the classic GoF form contrasted with the Python form, importable code, a
runnable mini-project, and an honest verdict when the right answer is "don't".

## MCP

```bash
claude mcp add design-patterns -- uv run --directory <this-repo> python-design-patterns-mcp
```

- Agents get search and recommendations over the catalog, then per pattern:
  docs → run the examples (sandboxed) → read the source.
- HTTP instead of stdio: `python-design-patterns-mcp --http`.
- Sandbox: `python -I`, scrubbed env, 10s/64KB caps, catalog-resolved packages only.

## Use it

```python
from patterns.structural.decorator import retry, logged
```

Run any mini-project: `uv run python -m patterns.structural.decorator.examples.resilient_client`

## Catalog

Based on [python-patterns.guide](https://python-patterns.guide/).

<!-- catalog:begin (generated: make readme) -->

| Pattern | Group | Verdict | Problem it solves |
|---|---|---|---|
| [Composition Over Inheritance](patterns/principle/composition_over_inheritance/) | Principles | ✅ pythonic | Vary independent behaviors without one subclass per combination of them. |
| [Global Object](patterns/python/global_object/) | Python-native | ⚠️ use with care | Give a whole program shared access to a constant or a pre-built object by assigning it at module level. |
| [Prebound Method](patterns/python/prebound_method/) | Python-native | ✅ pythonic | Offer module-level functions that share state, by binding the methods of one hidden instance to module globals. |
| [Sentinel Object](patterns/python/sentinel_object/) | Python-native | ✅ pythonic | Mark 'no value here' unambiguously when None itself is a legitimate value. |
| [Abstract Factory](patterns/creational/abstract_factory/) | Creational (GoF) | 🔄 prefer alternative | Let code build families of related objects without naming their concrete classes. |
| [Builder](patterns/creational/builder/) | Creational (GoF) | ⚠️ use with care | Assemble a complex object step by step, so the assembly process is reusable and readable. |
| [Factory Method](patterns/creational/factory_method/) | Creational (GoF) | 🔄 prefer alternative | Let a class defer which helper object it constructs, so subclasses or callers can substitute another. |
| [Prototype](patterns/creational/prototype/) | Creational (GoF) | 🔄 prefer alternative | Create new objects by copying a pre-configured exemplar instead of constructing from scratch. |
| [Singleton](patterns/creational/singleton/) | Creational (GoF) | 🔄 prefer alternative | Guarantee a class has exactly one instance and give the whole program access to it. |
| [Adapter](patterns/structural/adapter/) | Structural (GoF) | ✅ pythonic | Make an existing class usable through the interface your code expects, without editing either side. |
| [Bridge](patterns/structural/bridge/) | Structural (GoF) | 🔄 prefer alternative | Let an abstraction and its implementation vary independently, instead of multiplying subclasses across both axes. |
| [Composite](patterns/structural/composite/) | Structural (GoF) | ✅ pythonic | Let callers treat a single object and a whole tree of objects through one interface. |
| [Decorator](patterns/structural/decorator/) | Structural (GoF) | ✅ pythonic | Add behavior around an object or callable without editing it or subclassing it. |
| [Facade](patterns/structural/facade/) | Structural (GoF) | ✅ pythonic | Give a complicated subsystem one simple entry point for the common case. |
| [Flyweight](patterns/structural/flyweight/) | Structural (GoF) | ⚠️ use with care | Support huge numbers of fine-grained objects by sharing immutable instances instead of duplicating them. |
| [Proxy](patterns/structural/proxy/) | Structural (GoF) | ⚠️ use with care | Stand in for another object to control access to it — deferring, guarding, or instrumenting the real thing. |
| [Chain of Responsibility](patterns/behavioral/chain_of_responsibility/) | Behavioral (GoF) | 🔄 prefer alternative | Pass a request along a line of handlers until one of them takes it. |
| [Command](patterns/behavioral/command/) | Behavioral (GoF) | ⚠️ use with care | Package a request as an object so it can be queued, logged, undone, or executed later by code that doesn't know its details. |
| [Interpreter](patterns/behavioral/interpreter/) | Behavioral (GoF) | 🔄 prefer alternative | Represent a small language's grammar as data and evaluate sentences in it. |
| [Iterator](patterns/behavioral/iterator/) | Behavioral (GoF) | ✅ pythonic | Traverse a container's elements without exposing how the container stores them. |
| [Mediator](patterns/behavioral/mediator/) | Behavioral (GoF) | ⚠️ use with care | Stop a web of objects from referencing each other by routing their interactions through one coordinator. |
| [Memento](patterns/behavioral/memento/) | Behavioral (GoF) | ⚠️ use with care | Capture an object's state so it can be restored later, without exposing its internals. |
| [Observer](patterns/behavioral/observer/) | Behavioral (GoF) | ✅ pythonic | Notify interested parties when something changes, without the subject knowing who they are. |
| [State](patterns/behavioral/state/) | Behavioral (GoF) | ⚠️ use with care | Change an object's behavior when its internal state changes, without an if-forest over a mode flag. |
| [Strategy](patterns/behavioral/strategy/) | Behavioral (GoF) | 🔄 prefer alternative | Make an algorithm interchangeable at runtime without the caller knowing which variant it got. |
| [Template Method](patterns/behavioral/template_method/) | Behavioral (GoF) | 🔄 prefer alternative | Fix an algorithm's skeleton while letting callers vary individual steps. |
| [Visitor](patterns/behavioral/visitor/) | Behavioral (GoF) | 🔄 prefer alternative | Run a new operation over every node of an object structure without adding a method to every node class. |
| [Async Producer/Consumer](patterns/modern/async_producer_consumer/) | Modern Python | ⚠️ use with care | Decouple work generation from work processing under asyncio, with bounded memory and clean shutdown. |
| [Context Manager](patterns/modern/context_manager/) | Modern Python | ✅ pythonic | Guarantee acquire/release pairing around a block of code, even when it raises. |
| [Dependency Injection](patterns/modern/dependency_injection/) | Modern Python | ✅ pythonic | Hand an object its collaborators instead of letting it construct them, so they can be swapped — above all in tests. |
| [Registry](patterns/modern/registry/) | Modern Python | ✅ pythonic | Let implementations announce themselves by name, so dispatch is a lookup instead of an if/elif ladder. |
| [Repository](patterns/modern/repository/) | Modern Python | ⚠️ use with care | Keep domain logic ignorant of how objects are stored, behind a collection-like interface. |
<!-- catalog:end -->
