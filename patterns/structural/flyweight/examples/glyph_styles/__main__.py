"""Demo: a large document, a tiny number of live Style objects."""

from __future__ import annotations

from patterns.structural.flyweight.examples.glyph_styles.document import Document


def main() -> None:
    doc = Document()
    doc.write("Chapter One", font="Georgia", size=18, weight="bold")
    for _ in range(1000):
        doc.write("All happy families are alike. ", font="Georgia", size=11)
    doc.write("THE END", font="Georgia", size=18, weight="bold")

    a = doc.glyphs[0].style
    b = doc.glyphs[-1].style
    print(f"glyphs in document:  {len(doc):,}")
    print(f"distinct styles:     {doc.styles.distinct_styles}")
    print(f"headers share one object: {a is b}")


if __name__ == "__main__":
    main()
