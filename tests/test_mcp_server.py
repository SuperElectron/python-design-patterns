"""MCP server integration tests: driven through an in-memory client session."""

import json

import pytest
from mcp import Client
from mcp.types import TextResourceContents

import design_patterns.mcp.server as server_module
from design_patterns.catalog import Catalog
from design_patterns.mcp.server import mcp


class TestTools:
    async def test_list_patterns_returns_whole_catalog(self) -> None:
        async with Client(mcp) as client:
            result = await client.call_tool("list_patterns", {})
            assert result.structured_content is not None
            patterns = result.structured_content["result"]
            assert len(patterns) == 32
            assert {"id", "name", "problem", "verdict"} <= patterns[0].keys()

    async def test_list_patterns_filters(self) -> None:
        async with Client(mcp) as client:
            result = await client.call_tool("list_patterns", {"group": "creational"})
            assert result.structured_content is not None
            ids = [p["id"] for p in result.structured_content["result"]]
            assert len(ids) == 5 and all(i.startswith("creational/") for i in ids)

    async def test_get_pattern_with_source(
        self, legacy_catalog: Catalog, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        # Variant source is a legacy-shape feature; every real unit migrates,
        # so this runs against the synthetic legacy unit.
        monkeypatch.setattr(server_module, "get_catalog", lambda: legacy_catalog)
        async with Client(mcp) as client:
            result = await client.call_tool(
                "get_pattern", {"pattern_id": "creational/oldthing", "variant": "pythonic"}
            )
            assert result.structured_content is not None
            detail = result.structured_content
            assert detail["verdict"] == "prefer-alternative"
            assert "pythonic oldthing runs" in detail["source"]["pythonic"]

    async def test_get_pattern_unknown_id_names_the_catalog(self) -> None:
        async with Client(mcp) as client:
            result = await client.call_tool("get_pattern", {"pattern_id": "nope/nothing"})
            assert result.is_error

    async def test_search_finds_singleton_from_symptoms(self) -> None:
        async with Client(mcp) as client:
            result = await client.call_tool(
                "search_patterns", {"query": "only one shared config instance"}
            )
            assert result.structured_content is not None
            ids = [h["id"] for h in result.structured_content["result"]]
            assert "creational/singleton" in ids

    async def test_run_example_returns_real_output(self) -> None:
        # The pilot unit is module-shape for good — a stable target while the
        # remaining units migrate group by group.
        async with Client(mcp) as client:
            result = await client.call_tool(
                "run_example",
                {
                    "pattern_id": "behavioral/chain_of_responsibility",
                    "example": "ticket_escalation",
                },
            )
            assert result.structured_content is not None
            run = result.structured_content
            assert run["exit_code"] == 0 and not run["timed_out"]
            assert "helpdesk" in run["stdout"]

    async def test_recommend_attaches_caveats(self) -> None:
        async with Client(mcp) as client:
            result = await client.call_tool(
                "recommend_pattern",
                {"problem_statement": "I want a class with only one instance, a singleton"},
            )
            assert result.structured_content is not None
            recs = result.structured_content["result"]
            singleton = next(r for r in recs if r["id"] == "creational/singleton")
            assert singleton["verdict"] == "prefer-alternative"
            assert singleton["caveats"]


class TestRecommendNoteByShape:
    """The prefer-alternative note is pinned per shape, via synthetic units."""

    @staticmethod
    def _point_at(
        catalog: Catalog,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        from design_patterns.mcp.search import SearchIndex

        monkeypatch.setattr(server_module, "get_catalog", lambda: catalog)
        monkeypatch.setattr(server_module, "get_index", lambda: SearchIndex(catalog))

    async def test_module_unit_note_names_the_module_tools(
        self, module_catalog: Catalog, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        self._point_at(module_catalog, monkeypatch)
        async with Client(mcp) as client:
            result = await client.call_tool(
                "recommend_pattern", {"problem_statement": "thing needed"}
            )
            assert result.structured_content is not None
            rec = result.structured_content["result"][0]
            assert rec["id"] == "creational/thing"
            assert "get_pattern_docs" in rec["note"] and "read_source" in rec["note"]

    async def test_legacy_unit_note_points_at_pythonic_file(
        self, legacy_catalog: Catalog, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        self._point_at(legacy_catalog, monkeypatch)
        async with Client(mcp) as client:
            result = await client.call_tool(
                "recommend_pattern", {"problem_statement": "old thing needed"}
            )
            assert result.structured_content is not None
            rec = result.structured_content["result"][0]
            assert rec["id"] == "creational/oldthing"
            assert "pythonic.py" in rec["note"]


class TestModuleShapeTools:
    """The three new access levels, against a synthetic migrated unit."""

    @pytest.fixture(autouse=True)
    def _use_module_catalog(self, module_catalog: Catalog, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(server_module, "get_catalog", lambda: module_catalog)

    async def test_get_pattern_docs(self) -> None:
        async with Client(mcp) as client:
            result = await client.call_tool(
                "get_pattern_docs", {"pattern_id": "creational/thing", "doc": "fundamentals"}
            )
            assert not result.is_error
            assert "fundamentals of Thing" in str(result.content[0])

    async def test_get_pattern_docs_rejects_unknown_doc(self) -> None:
        async with Client(mcp) as client:
            result = await client.call_tool(
                "get_pattern_docs", {"pattern_id": "creational/thing", "doc": "naive"}
            )
            assert result.is_error

    async def test_list_examples_names_the_run_call(self) -> None:
        async with Client(mcp) as client:
            result = await client.call_tool("list_examples", {"pattern_id": "creational/thing"})
            assert result.structured_content is not None
            examples = result.structured_content["result"]
            assert [e["name"] for e in examples] == ["demo"]
            assert "run_example" in examples[0]["run"]

    async def test_run_example_by_package(self) -> None:
        async with Client(mcp) as client:
            result = await client.call_tool(
                "run_example", {"pattern_id": "creational/thing", "example": "demo"}
            )
            assert result.structured_content is not None
            run = result.structured_content
            assert run["exit_code"] == 0 and "built a thing" in run["stdout"]

    async def test_run_example_requires_exactly_one_selector(self) -> None:
        async with Client(mcp) as client:
            result = await client.call_tool("run_example", {"pattern_id": "creational/thing"})
            assert result.is_error

    async def test_read_source_returns_pattern_package(self) -> None:
        async with Client(mcp) as client:
            result = await client.call_tool("read_source", {"pattern_id": "creational/thing"})
            assert result.structured_content is not None
            sources = result.structured_content
            assert "built a thing" in sources["thing.py"]

    async def test_docs_resource(self) -> None:
        async with Client(mcp) as client:
            doc = await client.read_resource("pattern://creational/thing/docs/implementation")
            first = doc.contents[0]
            assert isinstance(first, TextResourceContents)
            assert "implementation of Thing" in first.text

    async def test_variant_resource_error_text_reaches_client(self) -> None:
        # A module-shape unit refusing a legacy variant read must explain itself.
        async with Client(mcp) as client:
            with pytest.raises(Exception, match="module-shape unit"):
                await client.read_resource("pattern://creational/thing/naive")


class TestLegacyShapeErrors:
    """Module-shape tools refuse un-migrated units with a clear message, not a crash.

    Uses a synthetic legacy unit: every real unit migrates to the module shape,
    so no real id can be relied on to stay legacy.
    """

    @pytest.fixture(autouse=True)
    def _use_legacy_catalog(self, legacy_catalog: Catalog, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(server_module, "get_catalog", lambda: legacy_catalog)

    async def test_get_pattern_docs_on_legacy_unit(self) -> None:
        async with Client(mcp) as client:
            result = await client.call_tool(
                "get_pattern_docs", {"pattern_id": "creational/oldthing", "doc": "fundamentals"}
            )
            assert result.is_error
            assert "not yet migrated" in str(result.content[0])

    async def test_list_examples_on_legacy_unit(self) -> None:
        async with Client(mcp) as client:
            result = await client.call_tool("list_examples", {"pattern_id": "creational/oldthing"})
            assert result.is_error

    async def test_read_source_on_legacy_unit(self) -> None:
        async with Client(mcp) as client:
            result = await client.call_tool("read_source", {"pattern_id": "creational/oldthing"})
            assert result.is_error

    async def test_run_example_legacy_variant_dispatch(self) -> None:
        # The variant= arm is what every un-migrated unit still relies on.
        async with Client(mcp) as client:
            result = await client.call_tool(
                "run_example", {"pattern_id": "creational/oldthing", "variant": "pythonic"}
            )
            assert result.structured_content is not None
            run = result.structured_content
            assert run["exit_code"] == 0 and not run["timed_out"]
            assert "pythonic oldthing runs" in run["stdout"]

    async def test_docs_resource_error_text_reaches_client(self) -> None:
        # ResourceError (not ValueError) is required for the hint to survive
        # the SDK's template wrapper — this pins that the text gets through.
        async with Client(mcp) as client:
            with pytest.raises(Exception, match="not yet migrated"):
                await client.read_resource("pattern://creational/oldthing/docs/fundamentals")


class TestResources:
    async def test_catalog_index_resource(self) -> None:
        async with Client(mcp) as client:
            result = await client.read_resource("catalog://index")
            contents = result.contents[0]
            assert isinstance(contents, TextResourceContents)
            assert len(json.loads(contents.text)) == 32

    async def test_pattern_doc_and_source_templates(self) -> None:
        async with Client(mcp) as client:
            doc = await client.read_resource("pattern://behavioral/iterator")
            first = doc.contents[0]
            assert isinstance(first, TextResourceContents)
            assert "# Iterator" in first.text

            src = await client.read_resource("pattern://behavioral/iterator/naive")
            first_src = src.contents[0]
            assert isinstance(first_src, TextResourceContents)
            assert "__next__" in first_src.text


class TestPrompts:
    async def test_prompts_are_listed_and_render(self) -> None:
        async with Client(mcp) as client:
            listed = await client.list_prompts()
            names = {p.name for p in listed.prompts}
            assert {"refactor_toward", "explain_pattern", "choose_pattern"} <= names

            prompt = await client.get_prompt(
                "refactor_toward",
                {"pattern_id": "creational/singleton", "code": "class Config: pass"},
            )
            text = prompt.messages[0].content
            assert "prefer-alternative" in str(text)
