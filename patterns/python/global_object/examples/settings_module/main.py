"""Demo: the three kinds of global, and when each one pays its cost."""

from __future__ import annotations

from patterns.python.global_object.examples.settings_module import settings
from patterns.python.global_object.examples.settings_module.shipping import (
    is_valid_slug,
    shipping_zone,
)


def main() -> None:
    print(f"constant:            RETRY_LIMIT = {settings.RETRY_LIMIT}")
    print(f"prebuilt regex:      is_valid_slug('summer-sale') = {is_valid_slug('summer-sale')}")
    print(f"lazy built at import? {settings.ZONE_TABLE.initialized}")
    print(f"shipping_zone('FR'):  {shipping_zone('FR')}")
    print(f"lazy built after use? {settings.ZONE_TABLE.initialized}")
    print(f"factory ran:          {settings.FACTORY_RUNS} time(s)")


if __name__ == "__main__":
    main()
