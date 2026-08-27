# Flyweight — putting it into a system

## The smell it fixes

A million tiny objects that are mostly the same object:

```python
@dataclass
class Char:
    char: str
    font: str  # "Georgia" a million times
    size: int  # 11 a million times
    weight: str  # "regular" a million times
```

Per-occurrence data (the character) is fused to duplicated data (the style),
and memory pays for the duplication a million-fold.

## Steps

1. **Measure first.** `sys.getsizeof`, `tracemalloc`, a heap profiler —
   confirm the duplicates exist and matter. CPython already interns small
   ints and many strings; your problem may be imaginary.
2. **Split intrinsic from extrinsic.** Intrinsic = identical across
   occurrences and immutable (the style); extrinsic = per occurrence (the
   char, the position). The split is the design work; the pool is plumbing.
3. **Freeze the intrinsic part** (`@dataclass(frozen=True)`) so sharing is
   safe by construction.
4. **Front construction with a pool** — `InternPool(build)` from
   [`pattern/pool.py`](../pattern/pool.py), or `functools.lru_cache` on a
   factory function when you don't need to inspect the pool.
5. **Route all construction through the factory.** A single call site that
   builds directly reintroduces duplicates silently; make the factory the
   only public door.
6. **Assert the sharing in a test** — `get(k) is get(k)` and a distinct-count
   ceiling — so a refactor that breaks interning fails loudly.

## Python idioms that keep it small

- **`functools.lru_cache` as the pool** when the key is the factory's
  argument tuple and you never need eviction control or introspection.
- **Frozen dataclasses** give immutability, `__hash__`, and `__eq__` in one
  decorator line.
- **Tuples as keys**: `(font, size, weight)` needs no key class.
- **`sys.intern`** when the flyweights are strings compared often.

## Pitfalls

- **Mutable flyweights** — one mutation corrupts every holder. The pool's
  `strict=True` refuses values it can't verify as frozen.
- **Unbounded pools from user-supplied keys** are a memory leak wearing the
  memory-optimization costume; bound them (`lru_cache(maxsize=...)`) or key
  from a closed domain.
- **Equality vs identity confusion.** Sharing makes `is` work; code that
  *relies* on `is` for correctness now silently depends on the pool being
  the only constructor.
- **Interning by reflex** — without a measurement, the pattern is pure
  ceremony (this unit's verdict in one line).

## Worked example

[`examples/glyph_styles/`](../examples/glyph_styles/) holds a ~30,000-glyph
document at two live `Style` objects and pins both the identity sharing
and the ceiling in tests:

```bash
uv run python -m patterns.structural.flyweight.examples.glyph_styles
```
