"""Self-registering exporters over a shared ``Registry``.

Run it: ``uv run python -m patterns.modern.registry.examples.export_plugins``

The import below is load-bearing: ``markdown`` registers itself at import
time, and a plugin nobody imports doesn't exist (the pattern's sharpest
caveat). This package's ``__init__`` is where that import is guaranteed.
"""

from patterns.modern.registry.examples.export_plugins import markdown as markdown
from patterns.modern.registry.examples.export_plugins.exporters import (
    EXPORTERS,
    export,
)

__all__ = ["EXPORTERS", "export", "markdown"]
