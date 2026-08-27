"""A flaky API client hardened by stacking decorators.

Run it: ``uv run python -m patterns.structural.decorator.examples.resilient_client``
"""

from patterns.structural.decorator.examples.resilient_client.client import (
    FlakyPaymentAPI,
    TransientNetworkError,
)
from patterns.structural.decorator.examples.resilient_client.service import (
    build_charge,
)

__all__ = ["FlakyPaymentAPI", "TransientNetworkError", "build_charge"]
