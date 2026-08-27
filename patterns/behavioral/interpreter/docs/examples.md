# Interpreter — where it lives outside this repo

Cited, real implementations to study (or point an agent at) when designing or
reviewing little-language code.

## Python standard library

- **`ast.literal_eval` / `ast.NodeVisitor`** — the safe-evaluation floor:
  Python parses, you walk only the nodes you allow. This module's
  [`safe_eval`](../pattern/safe_eval.py) is the canonical restricted walk.
  [docs.python.org/3/library/ast.html](https://docs.python.org/3/library/ast.html)
- **`re`** — a complete Interpreter implementation used daily: a pattern
  language parsed and compiled into a program, evaluated against strings.
  [docs.python.org/3/library/re.html](https://docs.python.org/3/library/re.html)

## Major ecosystems

- **Django `Q` objects** — query predicates built as composable expression
  trees (`Q(age__gte=18) & Q(country="CA")`), interpreted into SQL by the ORM.
  [docs.djangoproject.com/en/stable/topics/db/queries/#complex-lookups-with-q-objects](https://docs.djangoproject.com/en/stable/topics/db/queries/#complex-lookups-with-q-objects)
- **SQLAlchemy Core expression language** — column expressions form a tree
  the compiler walks to emit dialect-specific SQL: grammar-as-objects at
  production scale.
  [docs.sqlalchemy.org/en/latest/core/expression_api.html](https://docs.sqlalchemy.org/en/latest/core/expression_api.html)
- **pytest `-k` expressions** — a real shipped mini-language (`and`/`or`/
  `not` over test names) with its own tiny parser and evaluator.
  [docs.pytest.org/en/stable/how-to/usage.html#specifying-which-tests-to-run](https://docs.pytest.org/en/stable/how-to/usage.html#specifying-which-tests-to-run) *(unverified)*
- **json-logic** — rules-as-JSON evaluated by a small interpreter; the same
  shape as this unit's flag engine, standardized across languages.
  [jsonlogic.com](https://jsonlogic.com/) *(unverified)*

## What to notice across all of them

None of them expose a general-purpose evaluator to user input. Each fixes a
closed set of operations (Django's lookups, pytest's three combinators) and
validates sentences structurally before evaluating — the two guards
(`ValueError` on unknown operations, bounded depth) that this module treats
as part of the pattern, not optional hardening.
