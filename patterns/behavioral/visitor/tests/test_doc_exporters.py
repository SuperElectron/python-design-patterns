"""Behavioral tests for the doc-exporters mini-project."""

from __future__ import annotations

import pytest

from patterns.behavioral.visitor import Operation, UnhandledNodeError
from patterns.behavioral.visitor.examples.doc_exporters.__main__ import main, sample_document
from patterns.behavioral.visitor.examples.doc_exporters.exporters import (
    markdown,
    plain_text,
    word_count,
)
from patterns.behavioral.visitor.examples.doc_exporters.nodes import (
    BulletList,
    CodeBlock,
    Document,
    Paragraph,
    Section,
)


class TestMarkdown:
    def test_renders_the_whole_tree_with_heading_levels(self) -> None:
        out = markdown(sample_document())
        lines = out.splitlines()
        # Exact-line assertions: "## Highlights" as a substring would also
        # match "### Highlights", hiding a heading-level regression.
        assert lines[0] == "# Release notes"
        assert "## Highlights" in lines
        assert "- dark mode" in lines
        assert "```bash\npip install app==2.0\n```" in out


class TestPlainText:
    def test_renders_titles_and_indents_code(self) -> None:
        out = plain_text(sample_document())
        assert out.startswith("RELEASE NOTES")
        assert "Highlights\n----------" in out
        assert "    pip install app==2.0" in out


class TestWordCount:
    def test_counts_prose_words_and_ignores_code(self) -> None:
        doc = Document(
            "Two words",  # 2
            (
                Paragraph("one two three"),  # 3
                Section("title", (CodeBlock("py", "print('not counted')"),)),  # 1 + 0
                BulletList(("a b", "c")),  # 3
            ),
        )
        assert word_count(doc) == 9


class TestThePatternsPromise:
    def test_a_new_operation_needs_no_edit_to_the_node_classes(self) -> None:
        html: Operation[str] = Operation("html")

        @html.register
        def _p(node: Paragraph) -> str:
            return f"<p>{node.text}</p>"

        @html.register
        def _d(node: Document) -> str:
            return f"<h1>{node.title}</h1>" + "".join(html(child) for child in node.children)

        out = html(Document("T", (Paragraph("hello"),)))
        assert out == "<h1>T</h1><p>hello</p>"

    def test_an_unregistered_node_type_is_an_error_not_silence(self) -> None:
        html: Operation[str] = Operation("html")

        @html.register
        def _(node: Paragraph) -> str:
            return node.text

        with pytest.raises(UnhandledNodeError, match="'html' has no case for CodeBlock"):
            html(CodeBlock("py", "x = 1"))


class TestDemo:
    def test_demo_prints_all_three_exports(self, capsys: pytest.CaptureFixture[str]) -> None:
        main()
        out = capsys.readouterr().out
        assert "-- markdown --" in out
        assert "-- plain text --" in out
        assert "-- word count: " in out
