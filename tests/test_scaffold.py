"""Smoke test: the package is installed and reports a version."""

from importlib.metadata import version


def test_version() -> None:
    assert version("python-design-patterns")
