"""Smoke test: the package imports and reports a version."""

import design_patterns


def test_version() -> None:
    assert design_patterns.__version__
