"""The Bridge pattern, importable as library code."""

from patterns.structural.bridge.pattern.bridge import (
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
