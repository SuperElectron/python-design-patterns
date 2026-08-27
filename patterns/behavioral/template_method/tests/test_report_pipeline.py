"""Behavioral tests for the report-pipeline mini-project."""

from __future__ import annotations

import pytest

from patterns.behavioral.template_method.examples.report_pipeline.main import main
from patterns.behavioral.template_method.examples.report_pipeline.models import Sale
from patterns.behavioral.template_method.examples.report_pipeline.pipeline import (
    build_csv_report,
    build_markdown_report,
    csv_rows,
    drop_refunds,
    markdown_table,
)


class TestSteps:
    def test_drop_refunds_removes_only_refunded_sales(self) -> None:
        kept = Sale("grinder", 1, 89.0)
        gone = Sale("gift card", 1, 50.0, refunded=True)
        assert drop_refunds((kept, gone)) == (kept,)

    def test_csv_rows_renders_header_plus_one_line_per_sale(self) -> None:
        out = csv_rows((Sale("grinder", 5, 89.0),))
        assert out == "product,quantity,revenue\ngrinder,5,445.00"

    def test_markdown_table_renders_the_same_data_as_a_table(self) -> None:
        out = markdown_table((Sale("grinder", 5, 89.0),))
        assert out.splitlines()[0] == "| product | quantity | revenue |"
        assert "| grinder | 5 | 445.00 |" in out


class TestVariants:
    def test_csv_report_excludes_the_refunded_sale(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        document = build_csv_report().run()
        assert "gift card" not in document
        assert document.startswith("product,quantity,revenue")
        assert capsys.readouterr().out.strip() == document  # delivered by printing

    def test_markdown_variant_shares_fetch_and_transform_with_csv(self) -> None:
        csv_doc = build_csv_report().run()
        md_doc = build_markdown_report().run()
        assert "espresso machine" in csv_doc and "espresso machine" in md_doc
        assert "gift card" not in md_doc  # same transform step ran


class TestDemo:
    def test_demo_prints_both_report_formats(self, capsys: pytest.CaptureFixture[str]) -> None:
        main()
        out = capsys.readouterr().out
        assert "-- csv --" in out
        assert "product,quantity,revenue" in out
        assert "| product | quantity | revenue |" in out
