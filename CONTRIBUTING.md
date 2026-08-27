# Contributing

## Workflow

Branches flow `main ← staging ← feat/<slug>`. PRs target `staging`; `main`
takes only reviewed milestone merges. CI (3.11/3.12/3.13) must pass.

## Adding a pattern unit

1. Scaffold: `/new-pattern <group>/<slug> "Name"` (Claude Code) or copy an
   existing unit's shape (the template is in [CLAUDE.md](CLAUDE.md)).
2. Fill the frontmatter — every key; `id` must equal `<group>/<slug>`; pick the
   verdict (`pythonic` | `use-with-care` | `prefer-alternative`, defined in
   [CLAUDE.md](CLAUDE.md)). The catalog loader validates this in CI and fails loudly.
3. Build the module: `pattern/` (the importable code), the three `docs/` files,
   at least one `examples/<project>/` mini-project that genuinely imports
   `pattern/` (entry point `main.py`, never `__main__.py`), and behavioral
   tests for both.
4. `make check` — ruff, mypy --strict, pytest must all pass. The loader rejects
   a unit missing any part of the template, and a catalog test rejects an
   example that never imports its own pattern package.
5. `make readme` — regenerate the catalog table (CI rejects a stale one).

## Quality bar

- Full type hints; import-safe modules (no side effects at import).
- Tests assert behavior, not "it runs" — and load-bearing claims get the
  mutation treatment (mutate the code, prove the suite fails, revert). Reviews
  are severity-ordered; machines own style, humans argue design.
- Mini-projects use realistic domains, no Foo/Bar.
- Prose: one page, problem-first, no UML, no history lessons. The classic
  (GoF) form lives in each unit's `docs/fundamentals.md` as an annotated listing.
