# Visitor — where it lives outside this repo

Cited, real implementations to study (or point an agent at) when designing or
reviewing visitor-shaped code.

## Python standard library

- **`ast.NodeVisitor` / `ast.NodeTransformer`.** The classic form as a
  supported API: subclass, implement `visit_ClassName` per node, call
  `generic_visit` to recurse. When the tree is Python source, this is the
  right tool — the stdlib owns the node family, you own the operation.
  [docs.python.org/3/library/ast.html#ast.NodeVisitor](https://docs.python.org/3/library/ast.html#ast.NodeVisitor)
- **`functools.singledispatch`.** The deletion of the pattern's plumbing:
  dispatch on argument type, registered by annotation — what this unit's
  `Operation` wraps with a strict default.
  [docs.python.org/3/library/functools.html#functools.singledispatch](https://docs.python.org/3/library/functools.html#functools.singledispatch)

## Major ecosystems

- **pylint checkers.** Every lint rule is a visitor: checkers implement
  `visit_<nodetype>` methods over the parsed tree, and new rules ship
  without touching the node classes — the open-operation-set promise at
  ecosystem scale.
  [pylint.readthedocs.io](https://pylint.readthedocs.io/)
- **LibCST.** Concrete-syntax-tree visitors and transformers powering
  large-scale codemods (Instagram's refactors); the visitor as a production
  migration tool.
  [libcst.readthedocs.io](https://libcst.readthedocs.io/)
- **SQLAlchemy's `visitors` module.** SQL compilation walks clause trees
  with visitor machinery (`ClauseVisitor`, traversal utilities) — the
  pattern deep inside a library most Python services already depend on.
  [docs.sqlalchemy.org/en/latest/core/visitors.html](https://docs.sqlalchemy.org/en/latest/core/visitors.html)

## What to notice across all of them

The pattern appears wherever the **node family is stable and owned by
someone else** (Python's grammar, SQL clauses) while operations multiply
(lint rules, compilers, codemods). None of the Python examples hand-write
`accept()` — dispatch is either a naming convention (`visit_X`) or
`singledispatch`. When reviewing, check the unknown-node policy: `ast`'s
`generic_visit` deliberately recurses past unknown nodes, lint rules
deliberately skip — an *exporter* that skips unknown nodes is losing data
silently.
