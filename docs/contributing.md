# Contributing

## Workflow

Branches flow `main ← staging ← feat/<slug>`. PRs target `staging`; `main`
takes only reviewed milestone merges. CI (3.11/3.12/3.13) must pass.

## Adding a pattern unit

1. Scaffold: `/new-pattern <group>/<slug> "Name"` (Claude Code) or copy an
   existing unit's shape.
2. Fill the frontmatter — every key; `id` must equal `<group>/<slug>`; pick
   the verdict per [verdicts.md](verdicts.md). The catalog loader validates
   this in CI and fails loudly.
3. Write the three variants (see [how-to-read-this-repo.md](how-to-read-this-repo.md)
   for what each is for) and behavioral tests for all of them.
4. `make check` — ruff, mypy --strict, pytest must all pass.
5. `make readme` — regenerate the catalog table (CI rejects a stale one).

## Quality bar

- Full type hints; import-safe modules (no side effects at import).
- Tests assert behavior, not "it runs".
- Prose: one page, problem-first, no UML, no history lessons.
