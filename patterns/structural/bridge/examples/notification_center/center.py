"""Routing app over the bridge: teams choose transports, code stays put.

Each team registers a channel — a preferred transport plus an address. The
center fans alerts and digests out to every team through whatever transport
each one picked. Adding a transport touches zero routing code; adding a
notifier kind touches zero transports. That independence *is* the bridge.
"""

from __future__ import annotations

from dataclasses import dataclass

from patterns.structural.bridge.pattern import AlertNotifier, DigestNotifier, Transport


@dataclass(frozen=True)
class TeamChannel:
    """One team's delivery preference."""

    team: str
    transport: Transport
    address: str


class NotificationCenter:
    """Holds the routing table; notifiers do the talking."""

    def __init__(self) -> None:
        self._channels: dict[str, TeamChannel] = {}

    def register(self, channel: TeamChannel, *, replace: bool = False) -> None:
        """Add a team's channel; refuses to silently drop an existing one.

        Pass ``replace=True`` to intentionally swap a team's transport.
        """
        if channel.team in self._channels and not replace:
            raise ValueError(
                f"team {channel.team!r} already has a channel; pass replace=True to swap it"
            )
        self._channels[channel.team] = channel

    @property
    def teams(self) -> list[str]:
        return sorted(self._channels)

    def alert(self, teams: list[str], severity: str, message: str) -> None:
        """Page specific teams through their chosen transports."""
        for team in teams:
            if team not in self._channels:
                raise KeyError(f"unknown team {team!r}; registered teams: {self.teams}")
            channel = self._channels[team]
            AlertNotifier(channel.transport, channel.address).alert(severity, message)

    def broadcast_digest(self, items: list[str]) -> None:
        """Every team gets the digest, each on its own transport."""
        for channel in self._channels.values():
            DigestNotifier(channel.transport, channel.address).digest(items)
