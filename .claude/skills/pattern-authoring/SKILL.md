---
name: pattern-authoring
description: How to write a complete pattern unit for this repo — variant roles, frontmatter, verdict rubric, and test expectations. Use when authoring or reviewing any patterns/<group>/<slug>/ content.
---

# Authoring a pattern unit

## The three variants have distinct jobs — don't blur them

- **naive.py** — the Gang-of-Four/Java translation, faithfully. Class-heavy,
  interface-driven, even when it looks silly in Python. It exists so a reader can
  diff it against pythonic.py and *see* what Python absorbs. Keep it correct and
  typed, but do not "improve" it.
- **pythonic.py** — what a fluent Python developer writes for the same problem.
  If the pattern collapses into a language feature (first-class functions, modules,
  dunder protocols, decorators, singledispatch), show the collapse and name it.
- **real_world.py** — a small program using the *stdlib's own* embodiment of the
  pattern (e.g. Iterator → generators/`iter()`, Decorator → `functools.wraps`,
  Prototype → `copy.deepcopy`, Command → `functools.partial` callbacks). Import the
  stdlib machinery; don't reimplement it.

## Choosing the verdict

- `pythonic` — the pattern, in its pythonic form, is what you'd genuinely recommend.
- `use-with-care` — legitimate uses exist, but each caveat in the frontmatter must
  name a concrete failure mode (not "be careful").
- `prefer-alternative` — the honest answer is "don't"; `pythonic.py` must then show
  the alternative, and `caveats` must name it explicitly (e.g. "You almost always
  want the Global Object pattern instead").

When python-patterns.guide has a chapter, its verdict wins; link it in `guide_url`
and align the prose with its argument. Where it has none, reason from its principles
(composition over inheritance, callables over class hierarchies).

## Prose in README.md (after the frontmatter)

Sections, in order: **Problem** (2–4 sentences, concrete), **Naive solution** (what
the GoF book prescribes and why it looks that way), **Pythonic solution** (the
collapse or refinement, with the language feature named), **In the wild** (where the
stdlib/ecosystem does this), **Verdict** (one honest paragraph). ~1 page total.
No history lessons, no UML.

## Tests

- One test file per unit, covering all three variants.
- Assert observable behavior: outputs, state transitions, raised exceptions,
  identity where the pattern is *about* identity (singleton, flyweight).
- Async units use pytest-asyncio; everything else stays synchronous.
- Never test print output by capsys unless the demo output IS the behavior.
