"""Abstract Factory — public API.

>>> from patterns.creational.abstract_factory import DocumentFamily
"""

from patterns.creational.abstract_factory.pattern import (
    HTML,
    MARKDOWN,
    DocumentFamily,
)

__all__ = ["HTML", "MARKDOWN", "DocumentFamily"]
