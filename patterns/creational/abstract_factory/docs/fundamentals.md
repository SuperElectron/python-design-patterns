# Abstract Factory — fundamentals

## Intent

Let code build *families* of related objects without naming their concrete
classes — so the whole family can be swapped at once, and members of
different families never get mixed.

## Participants

| Role | Classic (GoF) form | Python form |
|---|---|---|
| Abstract factory | Interface with one creation method per product | A frozen dataclass of callables — [`DocumentFamily`](../pattern/family.py) |
| Concrete factory | One subclass per family | One dataclass *instance* per family (`HTML`, `MARKDOWN`) |
| Products | Class hierarchies per product kind | Whatever the callables return |
| Client | Programs against the interface | Accepts the family as a parameter |

## Mechanism

1. Identify the objects that must stay **consistent with each other** — that
   consistency is the only reason to bundle factories at all.
2. Bundle one callable per product kind in a frozen dataclass.
3. Client code accepts the bundle and builds everything through it, never
   naming a concrete class or format.
4. Swapping the family — for a different output target, or for test stubs —
   changes every product together and cannot change only some of them.

## The classic form, and what Python absorbs

The textbook shape is an abstract class with one abstract method per product,
subclassed once per family:

```python
class NumberFactory(ABC):
    @abstractmethod
    def build_number(self, text: str) -> object: ...


class FloatFactory(NumberFactory):
    def build_number(self, text: str) -> object:
        return float(text)


class DecimalFactory(NumberFactory):
    def build_number(self, text: str) -> object:
        return Decimal(text)


def parse_numbers(texts: list[str], factory: NumberFactory) -> list[object]:
    return [factory.build_number(t) for t in texts]
```

That ceremony exists because 1990s languages could not pass a class or a
function as a value. Python can: `parse_numbers(texts, float)` needs no
interface and no subclasses — the stdlib itself ships this collapse as
`json.load(fp, parse_float=Decimal)`. What survives is only the *bundle*: when
several factories must stay consistent, group them in a frozen dataclass.

## When to use it

- Several created objects must belong to the same family, and mixing families
  is a bug you want the structure to prevent.
- Whole-family swap is a real requirement: output targets, storage backends,
  test doubles for everything at once.

Note: the bundled `HTML` family interpolates content unescaped — it is
teaching code, not a sanitizer. Escape untrusted text before rendering.

## When not to use it

- One factory would do → pass a single callable; no bundle, no pattern.
- The "family" never varies → construct directly and skip the indirection.
- Members do not actually need to be consistent → separate parameters.

## Verdict: prefer an alternative

Pass callables. Reach for a factory *object* — the frozen dataclass bundle —
only when the family is large enough that bundling beats passing them
individually. This module's `DocumentFamily` is that bundle at its smallest
honest size: three builders that must agree.
