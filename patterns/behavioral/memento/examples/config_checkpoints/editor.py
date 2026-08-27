"""The originator: a config editor with validate-or-rollback and checkpoints.

Because ``ServiceConfig`` is frozen, a snapshot is just the current object —
the editor hands it to ``History`` (the caretaker), which stores it without
ever reading a field.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import replace
from typing import Any

from patterns.behavioral.memento.examples.config_checkpoints.models import (
    ServiceConfig,
    validate,
)
from patterns.behavioral.memento.pattern import History


class ConfigEditor:
    """Edits a ``ServiceConfig``; every committed edit is undoable."""

    def __init__(self, config: ServiceConfig | None = None) -> None:
        self.config = config if config is not None else ServiceConfig()
        self._history: History[ServiceConfig] = History()

    def apply(self, changes: Mapping[str, Any]) -> ServiceConfig:
        """Apply a batch atomically: validate the result, commit or reject.

        On success the pre-batch snapshot goes onto the undo stack. On
        failure ``InvalidConfigError`` propagates and the live config is
        untouched — the caller never sees a half-applied batch.
        """
        candidate = replace(self.config, **changes)
        validate(candidate)
        self._history.save(self.config)
        self.config = candidate
        return self.config

    def undo(self) -> ServiceConfig:
        """Restore the config as it was before the last committed batch."""
        self.config = self._history.undo()
        return self.config

    def checkpoint(self, name: str) -> None:
        """Name the current config so it can be restored much later."""
        self._history.checkpoint(name, self.config)

    def rollback_to(self, name: str) -> ServiceConfig:
        """Jump back to a named checkpoint (the jump itself is undoable)."""
        restored = self._history.rollback_to(name)
        self._history.save(self.config)
        self.config = restored
        return self.config
