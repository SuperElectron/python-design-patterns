"""Observer — public API.

>>> from patterns.behavioral.observer import Signal
"""

from patterns.behavioral.observer.pattern import ErrorPolicy, Signal, Subscriber

__all__ = ["ErrorPolicy", "Signal", "Subscriber"]
