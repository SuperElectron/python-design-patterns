"""The document tree: plain frozen dataclasses, no ``accept()`` anywhere.

Adding an operation over these nodes never edits this file — that is the
pattern's promise, kept by keeping the nodes ignorant of their visitors.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Paragraph:
    text: str


@dataclass(frozen=True)
class CodeBlock:
    language: str
    code: str


@dataclass(frozen=True)
class BulletList:
    items: tuple[str, ...]


@dataclass(frozen=True)
class Section:
    title: str
    children: tuple[Block, ...]


@dataclass(frozen=True)
class Document:
    title: str
    children: tuple[Block, ...]


Block = Paragraph | CodeBlock | BulletList | Section
