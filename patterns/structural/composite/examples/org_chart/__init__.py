"""Org-chart rollups built on the Composite.

Run it: ``uv run python -m patterns.structural.composite.examples.org_chart``
"""

from patterns.structural.composite.examples.org_chart.org import (
    Department,
    Employee,
    OrgMetrics,
)

__all__ = ["Department", "Employee", "OrgMetrics"]
