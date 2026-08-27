"""Demo: an upgrade day saved by checkpoints."""

from __future__ import annotations

from patterns.behavioral.memento.examples.config_checkpoints.editor import ConfigEditor
from patterns.behavioral.memento.examples.config_checkpoints.models import InvalidConfigError


def main() -> None:
    editor = ConfigEditor()
    editor.apply({"workers": 8, "log_level": "WARNING"})
    editor.checkpoint("before-upgrade")
    print(f"checkpointed:   {editor.config}")

    try:
        editor.apply({"workers": 0, "timeout_s": -1.0})
    except InvalidConfigError as err:
        print(f"batch rejected: {err}")
    print(f"still intact:   {editor.config}")

    editor.apply({"feature_flags": frozenset({"new-renderer"})})
    print(f"upgraded:       {editor.config}")

    editor.rollback_to("before-upgrade")
    print(f"rolled back:    {editor.config}")


if __name__ == "__main__":
    main()
