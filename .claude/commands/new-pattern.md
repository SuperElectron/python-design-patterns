---
description: Scaffold a new pattern module under patterns/<group>/<slug>
argument-hint: <group>/<slug> "Pattern Name"
---

Scaffold a new pattern module for $ARGUMENTS.

1. Validate the group is one of: principle, python, creational, structural, behavioral, modern.
   Refuse anything else.
2. Create `patterns/<group>/<slug>/` with the exact module template from CLAUDE.md:
   - `README.md` — frontmatter with `id: <group>/<slug>`, all schema keys present,
     `verdict:` left as `use-with-care` with a `TODO` caveat; a ~10-line front door
     mapping the folders.
   - `__init__.py` and `pattern/__init__.py` holding ONLY as-alias re-export
     lines (`from .pattern.<slug> import X as X` / `from .<slug> import X as X`
     — no docstrings, no `__all__`); `pattern/<slug>.py` with a typed stub.
   - `docs/fundamentals.md`, `docs/implementation.md`, `docs/examples.md` — each a
     heading plus a `TODO` line naming what belongs there (classic-form contrast in
     fundamentals; never use the word "naive").
   - `examples/demo/main.py` with a typed `main() -> None` + script guard
     that imports from `...pattern`. Create NO other `__init__.py` — empty ones
     are banned (PEP 420 namespace packages); the loader rejects them.
   - `tests/test_<slug>.py` with one failing `test_todo` marked
     `xfail(reason="unit not yet written")`.
3. Run `make check` and report the result. Note: the catalog loader will fail the
   unit until the docs files, a runnable example importing `pattern/`, and real
   tests exist — that is the point. Do not write the actual pattern content —
   scaffolding only.
