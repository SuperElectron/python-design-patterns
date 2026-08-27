"""Bridge — public API.

>>> from patterns.structural.bridge import AlertNotifier, SlackTransport
"""

from patterns.structural.bridge.pattern import (
    AlertNotifier,
    DigestNotifier,
    EmailTransport,
    SlackTransport,
    SmsTransport,
    Transport,
)

__all__ = [
    "AlertNotifier",
    "DigestNotifier",
    "EmailTransport",
    "SlackTransport",
    "SmsTransport",
    "Transport",
]
