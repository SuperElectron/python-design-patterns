"""Demo: one document through all three exporters."""

from __future__ import annotations

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


def sample_document() -> Document:
    return Document(
        "Release notes",
        (
            Paragraph("Version 2.0 ships three long-requested features."),
            Section(
                "Highlights",
                (
                    BulletList(("faster startup", "dark mode", "offline sync")),
                    CodeBlock("bash", "pip install app==2.0"),
                ),
            ),
        ),
    )


def main() -> None:
    document = sample_document()
    print("-- markdown --")
    print(markdown(document))
    print("-- plain text --")
    print(plain_text(document))
    print(f"-- word count: {word_count(document)} --")


if __name__ == "__main__":
    main()
