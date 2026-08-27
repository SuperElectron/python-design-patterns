"""Chain of Responsibility — public API.

>>> from patterns.behavioral.chain_of_responsibility import Chain
"""

from patterns.behavioral.chain_of_responsibility.pattern import (
    Chain,
    Handler,
    UnhandledRequestError,
)

__all__ = ["Chain", "Handler", "UnhandledRequestError"]
