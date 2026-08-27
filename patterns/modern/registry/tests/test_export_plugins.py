"""Behavioral tests for the export-plugins mini-project."""

from __future__ import annotations

import json

import pytest

from patterns.modern.registry.examples.export_plugins import EXPORTERS, export
from patterns.modern.registry.examples.export_plugins.__main__ import main
from patterns.modern.registry.pattern import UnknownKeyError

ROWS = [{"name": "ada", "role": "eng"}, {"name": "grace", "role": "ops"}]


class TestExporters:
    def test_csv_round_trips_headers_and_rows(self) -> None:
        assert export(ROWS, "csv") == "name,role\nada,eng\ngrace,ops"

    def test_json_is_real_json(self) -> None:
        assert json.loads(export(ROWS, "json")) == ROWS

    def test_markdown_renders_a_table(self) -> None:
        out = export(ROWS, "markdown")
        assert out.splitlines()[0] == "| name | role |"
        assert "| ada | eng |" in out

    def test_empty_input_is_not_an_error(self) -> None:
        assert export([], "csv") == ""
        assert export([], "markdown") == ""


class TestPluginDiscovery:
    def test_the_separate_module_plugin_registered_via_the_package_import(self) -> None:
        # markdown.py is imported only by the package __init__ — its presence
        # here is the import-time caveat's fix, working.
        assert EXPORTERS.names() == ("csv", "json", "markdown")

    def test_unknown_format_policy_lives_in_one_place(self) -> None:
        with pytest.raises(UnknownKeyError, match="unknown format 'xml'"):
            export(ROWS, "xml")


class TestDemo:
    def test_main_exports_every_format_and_shows_the_unknown_policy(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        main()
        out = capsys.readouterr().out
        assert "--- csv ---" in out
        assert "--- markdown ---" in out
        assert "unknown format 'xml'" in out
