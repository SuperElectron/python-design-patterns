"""Team notification routing built on the Bridge.

Run it: ``uv run python -m patterns.structural.bridge.examples.notification_center``
"""

from patterns.structural.bridge.examples.notification_center.center import (
    NotificationCenter,
    TeamChannel,
)

__all__ = ["NotificationCenter", "TeamChannel"]
