"""Behavioral tests for the glyph_styles mini-project."""

from __future__ import annotations

import dataclasses

import pytest

from patterns.structural.flyweight.examples.glyph_styles.document import Document


def test_many_glyphs_share_a_handful_of_styles() -> None:
    doc = Document()
    for _ in range(500):
        doc.write("All happy families are alike. ", font="Georgia", size=11)
    doc.write("THE END", font="Georgia", size=18, weight="bold")
    assert len(doc) > 10_000
    assert doc.styles.distinct_styles == 2


def test_identical_runs_share_the_identical_style_object() -> None:
    doc = Document()
    doc.write("one", font="Georgia", size=11)
    doc.write("two", font="Georgia", size=11)
    assert doc.glyphs[0].style is doc.glyphs[-1].style


def test_styles_are_frozen() -> None:
    doc = Document()
    doc.write("x", font="Georgia", size=11)
    with pytest.raises(dataclasses.FrozenInstanceError):
        doc.glyphs[0].style.size = 99  # type: ignore[misc]


def test_extrinsic_state_stays_per_glyph() -> None:
    doc = Document()
    doc.write("ab", font="Georgia", size=11)
    first, second = doc.glyphs
    assert (first.char, second.char) == ("a", "b")
    assert first.style is second.style  # shared core, distinct occurrences
