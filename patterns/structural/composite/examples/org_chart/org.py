"""Departments hold teams hold people; one ``total()`` serves every level.

The interface-honesty rule in practice: ``Employee`` is a frozen leaf with no
child management — only ``Department`` (a ``Composite``) can ``add``/``remove``.
Both answer ``total()``, so headcount and cost roll up through any nesting
without ever asking a node what kind it is.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from patterns.structural.composite.pattern import Composite, HasTotal


@dataclass(frozen=True)
class OrgMetrics:
    """The rollup value: both measures travel up the tree together."""

    headcount: int
    annual_cost: int

    def __add__(self, other: OrgMetrics) -> OrgMetrics:
        return OrgMetrics(self.headcount + other.headcount, self.annual_cost + other.annual_cost)


ZERO = OrgMetrics(0, 0)


def combine(parts: Iterable[OrgMetrics]) -> OrgMetrics:
    return sum(parts, start=ZERO)


@dataclass(frozen=True)
class Employee:
    """A leaf. No ``add()`` — people honestly cannot hold reports here."""

    name: str
    salary: int

    def total(self) -> OrgMetrics:
        return OrgMetrics(headcount=1, annual_cost=self.salary)


class Department(Composite[OrgMetrics]):
    """A named container node; child management lives here, where it belongs."""

    def __init__(self, name: str, members: Iterable[HasTotal[OrgMetrics]] = ()) -> None:
        super().__init__(combine, members)
        self.name = name
