# Python Design Patterns

Look up any design pattern and see what a fluent Python developer would
*actually* write — the classic GoF form contrasted with the Python form,
importable reference code, and a mini-project that puts it to work — with an
honest verdict when the right answer is "don't". All 23 Gang of Four patterns
plus Python-native and modern ones, every unit typed, tested, and runnable.

## Use it

Each pattern is a self-contained module:

```
patterns/structural/decorator/
├── README.md       # the problem, the verdict, the map
├── pattern/        # the pattern as importable, typed code
├── docs/           # fundamentals · implementation · cited external examples
├── examples/       # runnable mini-projects that use pattern/
└── tests/          # behavioral tests for both
```

```python
from patterns.structural.decorator import retry, logged
```

Run any mini-project: `uv run python -m patterns.structural.decorator.examples.resilient_client.main`

Give it to your agents (MCP server with search, runnable examples, and
pattern recommendations):

```bash
claude mcp add design-patterns -- uv run --directory <this-repo> python-design-patterns-mcp
```

## Catalog

Based on [python-patterns.guide](https://python-patterns.guide/).

<!-- catalog:begin (generated: make readme) -->

### Principles

| Pattern | Verdict | Problem it solves |
|---|---|---|
| [Composition Over Inheritance](patterns/principle/composition_over_inheritance/) | ✅ pythonic | Vary independent behaviors without one subclass per combination of them. |

### Python-native

| Pattern | Verdict | Problem it solves |
|---|---|---|
| [Global Object](patterns/python/global_object/) | ⚠️ use with care | Give a whole program shared access to a constant or a pre-built object by assigning it at module level. |
| [Prebound Method](patterns/python/prebound_method/) | ✅ pythonic | Offer module-level functions that share state, by binding the methods of one hidden instance to module globals. |
| [Sentinel Object](patterns/python/sentinel_object/) | ✅ pythonic | Mark 'no value here' unambiguously when None itself is a legitimate value. |

### Creational (GoF)

| Pattern | Verdict | Problem it solves |
|---|---|---|
| [Abstract Factory](patterns/creational/abstract_factory/) | 🔄 prefer alternative | Let code build families of related objects without naming their concrete classes. |
| [Builder](patterns/creational/builder/) | ⚠️ use with care | Assemble a complex object step by step, so the assembly process is reusable and readable. |
| [Factory Method](patterns/creational/factory_method/) | 🔄 prefer alternative | Let a class defer which helper object it constructs, so subclasses or callers can substitute another. |
| [Prototype](patterns/creational/prototype/) | 🔄 prefer alternative | Create new objects by copying a pre-configured exemplar instead of constructing from scratch. |
| [Singleton](patterns/creational/singleton/) | 🔄 prefer alternative | Guarantee a class has exactly one instance and give the whole program access to it. |

### Structural (GoF)

| Pattern | Verdict | Problem it solves |
|---|---|---|
| [Adapter](patterns/structural/adapter/) | ✅ pythonic | Make an existing class usable through the interface your code expects, without editing either side. |
| [Bridge](patterns/structural/bridge/) | 🔄 prefer alternative | Let an abstraction and its implementation vary independently, instead of multiplying subclasses across both axes. |
| [Composite](patterns/structural/composite/) | ✅ pythonic | Let callers treat a single object and a whole tree of objects through one interface. |
| [Decorator](patterns/structural/decorator/) | ✅ pythonic | Add behavior around an object or callable without editing it or subclassing it. |
| [Facade](patterns/structural/facade/) | ✅ pythonic | Give a complicated subsystem one simple entry point for the common case. |
| [Flyweight](patterns/structural/flyweight/) | ⚠️ use with care | Support huge numbers of fine-grained objects by sharing immutable instances instead of duplicating them. |
| [Proxy](patterns/structural/proxy/) | ⚠️ use with care | Stand in for another object to control access to it — deferring, guarding, or instrumenting the real thing. |

### Behavioral (GoF)

| Pattern | Verdict | Problem it solves |
|---|---|---|
| [Chain of Responsibility](patterns/behavioral/chain_of_responsibility/) | 🔄 prefer alternative | Pass a request along a line of handlers until one of them takes it. |
| [Command](patterns/behavioral/command/) | ⚠️ use with care | Package a request as an object so it can be queued, logged, undone, or executed later by code that doesn't know its details. |
| [Interpreter](patterns/behavioral/interpreter/) | 🔄 prefer alternative | Represent a small language's grammar as data and evaluate sentences in it. |
| [Iterator](patterns/behavioral/iterator/) | ✅ pythonic | Traverse a container's elements without exposing how the container stores them. |
| [Mediator](patterns/behavioral/mediator/) | ⚠️ use with care | Stop a web of objects from referencing each other by routing their interactions through one coordinator. |
| [Memento](patterns/behavioral/memento/) | ⚠️ use with care | Capture an object's state so it can be restored later, without exposing its internals. |
| [Observer](patterns/behavioral/observer/) | ✅ pythonic | Notify interested parties when something changes, without the subject knowing who they are. |
| [State](patterns/behavioral/state/) | ⚠️ use with care | Change an object's behavior when its internal state changes, without an if-forest over a mode flag. |
| [Strategy](patterns/behavioral/strategy/) | 🔄 prefer alternative | Make an algorithm interchangeable at runtime without the caller knowing which variant it got. |
| [Template Method](patterns/behavioral/template_method/) | 🔄 prefer alternative | Fix an algorithm's skeleton while letting callers vary individual steps. |
| [Visitor](patterns/behavioral/visitor/) | 🔄 prefer alternative | Run a new operation over every node of an object structure without adding a method to every node class. |

### Modern Python

| Pattern | Verdict | Problem it solves |
|---|---|---|
| [Async Producer/Consumer](patterns/modern/async_producer_consumer/) | ⚠️ use with care | Decouple work generation from work processing under asyncio, with bounded memory and clean shutdown. |
| [Context Manager](patterns/modern/context_manager/) | ✅ pythonic | Guarantee acquire/release pairing around a block of code, even when it raises. |
| [Dependency Injection](patterns/modern/dependency_injection/) | ✅ pythonic | Hand an object its collaborators instead of letting it construct them, so they can be swapped — above all in tests. |
| [Registry](patterns/modern/registry/) | ✅ pythonic | Let implementations announce themselves by name, so dispatch is a lookup instead of an if/elif ladder. |
| [Repository](patterns/modern/repository/) | ⚠️ use with care | Keep domain logic ignorant of how objects are stored, behind a collection-like interface. |
<!-- catalog:end -->

More in [docs/](docs/index.md) — verdict definitions, MCP reference, contributing.
