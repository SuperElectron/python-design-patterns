"""Atomic config deployment built on the context manager pattern.

Run it: ``uv run python -m patterns.modern.context_manager.examples.atomic_deploy``
"""

from patterns.modern.context_manager.examples.atomic_deploy.deploy import (
    ReleaseError,
    deploy,
    no_validation,
    require_nonempty,
)

__all__ = ["ReleaseError", "deploy", "no_validation", "require_nonempty"]
