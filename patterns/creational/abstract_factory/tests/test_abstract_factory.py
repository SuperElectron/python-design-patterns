"""Behavioral tests for all three abstract-factory variants."""

from decimal import Decimal
from typing import ClassVar

from patterns.creational.abstract_factory import naive, pythonic, real_world


class TestNaive:
    def test_client_builds_through_the_interface(self) -> None:
        floats = naive.parse_numbers(["1.5"], naive.FloatFactory())
        exacts = naive.parse_numbers(["1.5"], naive.DecimalFactory())
        assert floats == [1.5] and isinstance(floats[0], float)
        assert exacts == [Decimal("1.5")] and isinstance(exacts[0], Decimal)


class TestPythonic:
    ROWS: ClassVar[list[list[str]]] = [["west", "$12k"], ["east", "$9k"]]

    def test_markdown_family_renders_consistently(self) -> None:
        doc = pythonic.render_sales_report(pythonic.MARKDOWN, self.ROWS)
        assert doc.startswith("## Sales by region")
        assert "| west | $12k |" in doc
        assert doc.endswith("> Figures exclude refunds.")

    def test_html_family_renders_consistently(self) -> None:
        doc = pythonic.render_sales_report(pythonic.HTML, self.ROWS)
        assert "<h2>Sales by region</h2>" in doc
        assert "<td>west</td>" in doc
        assert '<div class="callout">' in doc

    def test_client_is_format_blind(self) -> None:
        # A brand-new family works without touching the renderer.
        plain = pythonic.DocumentFamily(
            heading=str.upper,
            table=lambda headers, rows: "; ".join(",".join(r) for r in rows),
            callout=lambda text: f"NB: {text}",
        )
        doc = pythonic.render_sales_report(plain, self.ROWS)
        assert doc.splitlines()[0] == "SALES BY REGION"


class TestRealWorld:
    def test_parse_float_hook_changes_the_family(self) -> None:
        doc = real_world.load_exact('{"x": 0.1}')
        assert isinstance(doc, dict)
        assert doc["x"] == Decimal("0.1")
        assert isinstance(doc["x"], Decimal)
