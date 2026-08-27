"""Three operations over the document tree, each a dispatch family.

A new exporter is a new ``Operation`` plus one case per node type — the node
classes in ``nodes.py`` are never touched.
"""

from __future__ import annotations

from patterns.behavioral.visitor.examples.doc_exporters.nodes import (
    BulletList,
    CodeBlock,
    Document,
    Paragraph,
    Section,
)
from patterns.behavioral.visitor.pattern import Operation

markdown: Operation[str] = Operation("markdown")


@markdown.register
def _document_md(node: Document) -> str:
    body = "\n\n".join(markdown(child) for child in node.children)
    return f"# {node.title}\n\n{body}"


@markdown.register
def _section_md(node: Section) -> str:
    body = "\n\n".join(markdown(child) for child in node.children)
    return f"## {node.title}\n\n{body}"


@markdown.register
def _paragraph_md(node: Paragraph) -> str:
    return node.text


@markdown.register
def _code_md(node: CodeBlock) -> str:
    return f"```{node.language}\n{node.code}\n```"


@markdown.register
def _bullets_md(node: BulletList) -> str:
    return "\n".join(f"- {item}" for item in node.items)


plain_text: Operation[str] = Operation("plain_text")


@plain_text.register
def _document_txt(node: Document) -> str:
    body = "\n\n".join(plain_text(child) for child in node.children)
    return f"{node.title.upper()}\n\n{body}"


@plain_text.register
def _section_txt(node: Section) -> str:
    body = "\n\n".join(plain_text(child) for child in node.children)
    return f"{node.title}\n{'-' * len(node.title)}\n{body}"


@plain_text.register
def _paragraph_txt(node: Paragraph) -> str:
    return node.text


@plain_text.register
def _code_txt(node: CodeBlock) -> str:
    return "\n".join(f"    {line}" for line in node.code.splitlines())


@plain_text.register
def _bullets_txt(node: BulletList) -> str:
    return "\n".join(f"  * {item}" for item in node.items)


word_count: Operation[int] = Operation("word_count")


@word_count.register
def _document_wc(node: Document) -> int:
    return len(node.title.split()) + sum(word_count(child) for child in node.children)


@word_count.register
def _section_wc(node: Section) -> int:
    return len(node.title.split()) + sum(word_count(child) for child in node.children)


@word_count.register
def _paragraph_wc(node: Paragraph) -> int:
    return len(node.text.split())


@word_count.register
def _code_wc(node: CodeBlock) -> int:
    return 0  # code is not prose


@word_count.register
def _bullets_wc(node: BulletList) -> int:
    return sum(len(item.split()) for item in node.items)
