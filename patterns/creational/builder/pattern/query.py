"""What survives of the Builder in Python: staged assembly, frozen product.

Keyword arguments already solve the telescoping constructor. A builder still
earns its keep when construction is genuinely staged and validated — here, a
fluent ``SelectBuilder`` accumulating clauses, emitting an immutable ``Query``
(parameterized SQL, ``?`` placeholders) that mutating the builder afterwards
cannot touch.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Query:
    """The immutable product: a parameterized SELECT statement."""

    table: str
    columns: tuple[str, ...] = ("*",)
    conditions: tuple[str, ...] = ()
    params: tuple[object, ...] = ()
    order: tuple[str, ...] = ()
    limit_count: int | None = None

    def sql(self) -> str:
        """Render the statement; values stay in ``params``, never in the text."""
        clauses = [f"SELECT {', '.join(self.columns)} FROM {self.table}"]
        if self.conditions:
            clauses.append("WHERE " + " AND ".join(self.conditions))
        if self.order:
            clauses.append("ORDER BY " + ", ".join(self.order))
        if self.limit_count is not None:
            clauses.append(f"LIMIT {self.limit_count}")
        return " ".join(clauses)


class SelectBuilder:
    """The mutable assembly surface in front of the frozen ``Query``.

    Every step returns ``self`` for chaining and validates what a one-shot
    constructor could not express: placeholder counts, positive limits.
    """

    def __init__(self, table: str) -> None:
        if not table:
            raise ValueError("a query needs a table")
        self._table = table
        self._columns: list[str] = []
        self._conditions: list[str] = []
        self._params: list[object] = []
        self._order: list[str] = []
        self._limit: int | None = None

    def columns(self, *names: str) -> SelectBuilder:
        """Select these columns (default when never called: ``*``)."""
        self._columns.extend(names)
        return self

    def where(self, condition: str, *params: object) -> SelectBuilder:
        """AND-append a condition; ``?`` placeholders must match ``params``."""
        if condition.count("?") != len(params):
            raise ValueError(
                f"condition {condition!r} has {condition.count('?')} placeholder(s) "
                f"but {len(params)} parameter(s)"
            )
        self._conditions.append(condition)
        self._params.extend(params)
        return self

    def order_by(self, *terms: str) -> SelectBuilder:
        """Append ORDER BY terms (e.g. ``"amount DESC"``)."""
        self._order.extend(terms)
        return self

    def limit(self, count: int) -> SelectBuilder:
        """Cap the row count; must be positive."""
        if count < 1:
            raise ValueError(f"limit must be positive, got {count}")
        self._limit = count
        return self

    def build(self) -> Query:
        """Emit the frozen product; the builder may keep being used after."""
        return Query(
            table=self._table,
            columns=tuple(self._columns) or ("*",),
            conditions=tuple(self._conditions),
            params=tuple(self._params),
            order=tuple(self._order),
            limit_count=self._limit,
        )
