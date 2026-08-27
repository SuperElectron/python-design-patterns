# Prototype — fundamentals

## Intent

Create new objects by copying a pre-configured exemplar instead of
constructing from scratch — classically, a framework offers a menu of
prototypes the user picks from, and each pick is cloned so the exemplar stays
pristine.

## Participants

| Role | Classic (GoF) form | Python form |
|---|---|---|
| Prototype contract | Abstract class with a `clone()` method | Any zero-argument callable that builds a product — `Template` in [`pattern/templates.py`](../pattern/templates.py) |
| Concrete prototypes | Instances implementing `clone()` (usually via deep copy) | `functools.partial(Product, ...)` freezing the configuration |
| Registry / client | Maps names to exemplars, clones on request | `TemplateRegistry` maps names to callables, *calls* on request |
| Per-use customization | Mutate the clone after copying | `dataclasses.replace` on a frozen product |

## Mechanism

1. Each configuration worth naming becomes a template.
2. A request for a named template builds a **fresh** product — never a shared
   one, so callers can't corrupt the menu.
3. Per-request tweaks produce another new object; the template is immutable
   from the caller's point of view.

## The classic form, and what Python absorbs

The textbook version stores instances and copies them through a `clone()`
protocol:

```python
class Shape(ABC):
    @abstractmethod
    def clone(self) -> Self: ...  # the pattern's whole surface


class Circle(Shape):
    def clone(self) -> Self:
        return copy.deepcopy(self)  # copying IS the construction


class PrototypeRegistry:
    def register(self, name: str, prototype: Shape) -> None:
        self._prototypes[name] = prototype  # stores a live exemplar

    def create(self, name: str) -> Shape:
        return self._prototypes[name].clone()
```

The pattern targets a 1990s constraint: classes weren't values, so the only
way to hand a framework "how to make one of these" was a pre-made instance to
copy. Python callables *are* values — store the recipe, not a cooked meal.
`copy.copy`/`copy.deepcopy` (with the `__copy__`/`__deepcopy__` hooks) remain
for objects genuinely cheaper to copy than rebuild, and shallow-vs-deep is the
caveat to respect: `copy.copy` shares nested mutable state.

## When to use it

- A menu of named, pre-configured starting points (report templates, document
  boilerplates, game archetypes).
- Construction is expensive or awkward and instances are cheap to copy —
  that's the residual case for `copy.deepcopy`.

## When not to use it

- One-off construction with known arguments → just call the class.
- The "template" varies per call in every field → it's not a template, pass
  arguments.
- You reached for `clone()` to dodge `__init__` — fix the constructor instead.

## Verdict: prefer an alternative

Store callables, not exemplars: `partial` + `dataclasses.replace` do the whole
job with no protocol. Reach for `copy.deepcopy` only when instances are
genuinely expensive or awkward to rebuild from arguments.
