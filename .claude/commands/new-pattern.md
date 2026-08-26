---
description: Scaffold a new pattern unit under patterns/<group>/<slug>
argument-hint: <group>/<slug> "Pattern Name"
---

Scaffold a new pattern unit for $ARGUMENTS.

1. Validate the group is one of: principle, python, creational, structural, behavioral, modern.
   Refuse anything else.
2. Create `patterns/<group>/<slug>/` with the exact template from CLAUDE.md:
   README.md (frontmatter with `id: <group>/<slug>`, all schema keys present,
   `verdict:` left as `use-with-care` with a `TODO` caveat), empty-but-importable
   `__init__.py`, and stub `naive.py`, `pythonic.py`, `real_world.py` each with a
   typed `main() -> None` and script guard, plus `tests/test_<slug>.py` with one
   failing `test_todo` marked `xfail(reason="unit not yet written")`.
3. Run `make check` and report the result. Do not write the actual pattern content —
   scaffolding only.
