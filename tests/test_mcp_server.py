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

    async def test_get_pattern_lists_docs_and_examples(self) -> None:
        async with Client(mcp) as client:
            result = await client.call_tool("get_pattern", {"pattern_id": "structural/decorator"})
            assert result.structured_content is not None
            detail = result.structured_content
            assert detail["verdict"] == "pythonic"
            assert detail["docs"] == ["examples", "fundamentals", "implementation"]
            assert "resilient_client" in detail["examples"]
            assert detail["prose"]

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


class TestRecommendNote:
    """The prefer-alternative note is pinned via the synthetic unit."""

    async def test_note_names_the_docs_and_source_tools(
        self, module_catalog: Catalog, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        from design_patterns.mcp.search import SearchIndex

        monkeypatch.setattr(server_module, "get_catalog", lambda: module_catalog)
        monkeypatch.setattr(server_module, "get_index", lambda: SearchIndex(module_catalog))
        async with Client(mcp) as client:
            result = await client.call_tool(
                "recommend_pattern", {"problem_statement": "thing needed"}
            )
            assert result.structured_content is not None
            rec = result.structured_content["result"][0]
            assert rec["id"] == "creational/thing"
            assert "get_pattern_docs" in rec["note"] and "read_source" in rec["note"]


class TestModuleShapeTools:
    """The three access levels, against the synthetic unit."""

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

    async def test_unknown_doc_resource_error_text_reaches_client(self) -> None:
        # ResourceError (not ValueError) is required for the hint to survive
        # the SDK's template wrapper — this pins that the text gets through.
        async with Client(mcp) as client:
            with pytest.raises(Exception, match="has no doc"):
                await client.read_resource("pattern://creational/thing/docs/naive")


class TestResources:
    async def test_catalog_index_resource(self) -> None:
        async with Client(mcp) as client:
            result = await client.read_resource("catalog://index")
            contents = result.contents[0]
            assert isinstance(contents, TextResourceContents)
            assert len(json.loads(contents.text)) == 32

    async def test_pattern_doc_and_docs_templates(self) -> None:
        async with Client(mcp) as client:
            doc = await client.read_resource("pattern://behavioral/iterator")
            first = doc.contents[0]
            assert isinstance(first, TextResourceContents)
            assert "# Iterator" in first.text

            fund = await client.read_resource("pattern://behavioral/iterator/docs/fundamentals")
            first_fund = fund.contents[0]
            assert isinstance(first_fund, TextResourceContents)
            assert "# Iterator — fundamentals" in first_fund.text


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
