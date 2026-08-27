"""The importable Abstract Factory building block."""

from patterns.creational.abstract_factory.pattern.family import (
    HTML,
    MARKDOWN,
    DocumentFamily,
)

__all__ = ["HTML", "MARKDOWN", "DocumentFamily"]
