"""A sales-report pipeline: one fixed skeleton, interchangeable steps.

The spine (fetch → transform → render → deliver) is ``Skeleton.run`` from
the pattern package; every report variant below is the same spine with
different steps plugged in — no subclass per report.
"""

from __future__ import annotations

from patterns.behavioral.template_method.examples.report_pipeline.models import Sale, Sales
from patterns.behavioral.template_method.pattern import Skeleton


def fetch_sample_sales() -> Sales:
    """Stand-in for a database or API pull."""
    return (
        Sale("espresso machine", 2, 249.0),
        Sale("grinder", 5, 89.0),
        Sale("filter pack", 40, 3.5),
        Sale("gift card", 1, 50.0, refunded=True),
    )


def drop_refunds(sales: Sales) -> Sales:
    return tuple(sale for sale in sales if not sale.refunded)


def csv_rows(sales: Sales) -> str:
    lines = ["product,quantity,revenue"]
    lines += [f"{s.product},{s.quantity},{s.revenue():.2f}" for s in sales]
    return "\n".join(lines)


def markdown_table(sales: Sales) -> str:
    lines = ["| product | quantity | revenue |", "|---|---|---|"]
    lines += [f"| {s.product} | {s.quantity} | {s.revenue():.2f} |" for s in sales]
    return "\n".join(lines)


def print_delivery(document: str) -> None:
    print(document)


def build_csv_report() -> Skeleton[Sales, str]:
    """The baseline report; variants derive from it by swapping steps."""
    return Skeleton(
        fetch=fetch_sample_sales,
        transform=drop_refunds,
        render=csv_rows,
        deliver=print_delivery,
    )


def build_markdown_report() -> Skeleton[Sales, str]:
    """Same spine, same data — only the render step differs."""
    return build_csv_report().with_steps(render=markdown_table)
