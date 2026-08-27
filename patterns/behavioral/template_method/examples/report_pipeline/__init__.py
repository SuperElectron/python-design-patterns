"""A sales-report pipeline built on the Template Method pattern.

Run it: ``uv run python -m patterns.behavioral.template_method.examples.report_pipeline``
"""

from patterns.behavioral.template_method.examples.report_pipeline.models import Sale, Sales
from patterns.behavioral.template_method.examples.report_pipeline.pipeline import (
    build_csv_report,
    build_markdown_report,
    csv_rows,
    drop_refunds,
    markdown_table,
)

__all__ = [
    "Sale",
    "Sales",
    "build_csv_report",
    "build_markdown_report",
    "csv_rows",
    "drop_refunds",
    "markdown_table",
]
