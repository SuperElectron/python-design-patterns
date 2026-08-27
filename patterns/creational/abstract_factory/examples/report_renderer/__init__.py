"""Quarterly-report rendering built on the Abstract Factory.

Run it: ``uv run python -m patterns.creational.abstract_factory.examples.report_renderer``
"""

from patterns.creational.abstract_factory.examples.report_renderer.renderer import render
from patterns.creational.abstract_factory.examples.report_renderer.report import (
    Report,
    Section,
    Table,
)

__all__ = ["Report", "Section", "Table", "render"]
