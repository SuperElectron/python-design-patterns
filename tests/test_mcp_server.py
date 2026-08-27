"""MCP server integration tests: driven through an in-memory client session."""

import json

from mcp import Client
from mcp.types import TextResourceContents

from design_patterns_mcp.server import mcp


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

    async def test_get_pattern_with_source(self) -> None:
        async with Client(mcp) as client:
            result = await client.call_tool(
                "get_pattern", {"pattern_id": "structural/decorator", "variant": "pythonic"}
            )
            assert result.structured_content is not None
            detail = result.structured_content
            assert detail["verdict"] == "pythonic"
            assert "functools" in detail["source"]["pythonic"]

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
        async with Client(mcp) as client:
            result = await client.call_tool(
                "run_example", {"pattern_id": "creational/singleton", "variant": "pythonic"}
            )
            assert result.structured_content is not None
            run = result.structured_content
            assert run["exit_code"] == 0 and not run["timed_out"]
            assert "module global is shared" in run["stdout"]

    async def test_recommend_attaches_caveats_and_alternative_note(self) -> None:
        async with Client(mcp) as client:
            result = await client.call_tool(
                "recommend_pattern",
                {"problem_statement": "I want a class with only one instance, a singleton"},
            )
            assert result.structured_content is not None
            recs = result.structured_content["result"]
            singleton = next(r for r in recs if r["id"] == "creational/singleton")
            assert singleton["verdict"] == "prefer-alternative"
            assert "pythonic.py" in singleton["note"]
            assert singleton["caveats"]


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
