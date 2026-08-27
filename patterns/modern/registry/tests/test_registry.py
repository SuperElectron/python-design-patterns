"""Behavioral tests for all three registry variants."""

import pytest

from patterns.modern.registry import naive, pythonic, real_world

ROWS = [{"name": "ada", "role": "eng"}]


class TestNaive:
    def test_ladder_dispatch_works(self) -> None:
        assert naive.export(ROWS, "csv") == "name,role\nada,eng"

    def test_unknown_format(self) -> None:
        with pytest.raises(ValueError, match="unknown format"):
            naive.export(ROWS, "yaml")


class TestPythonic:
    def test_registered_handlers_dispatch_by_name(self) -> None:
        assert pythonic.export(ROWS, "csv") == "name,role\nada,eng"
        assert pythonic.export(ROWS, "keyvalue") == "name=ada\nrole=eng"

    def test_new_handler_registers_without_touching_the_dispatcher(self) -> None:
        @pythonic.register("upper")
        def to_upper(rows: list[dict[str, str]]) -> str:
            return " ".join(v.upper() for row in rows for v in row.values())

        try:
            assert pythonic.export(ROWS, "upper") == "ADA ENG"
        finally:
            del pythonic.EXPORTERS["upper"]

    def test_unknown_format_names_the_known_ones(self) -> None:
        with pytest.raises(ValueError, match="known: csv, keyvalue"):
            pythonic.export(ROWS, "yaml")


class TestRealWorld:
    def test_codec_registry_resolves_names(self) -> None:
        assert real_world.rot13("gura fur fnvq") == "then she said"
        assert real_world.lookup_is_the_registry("UTF8") == "utf-8"
