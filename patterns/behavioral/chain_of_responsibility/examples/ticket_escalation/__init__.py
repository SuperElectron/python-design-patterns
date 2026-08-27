"""Support-ticket escalation built on the Chain of Responsibility.

Run it: ``uv run python -m patterns.behavioral.chain_of_responsibility.examples.ticket_escalation``
"""

from patterns.behavioral.chain_of_responsibility.examples.ticket_escalation.handlers import (
    build_escalation_chain,
    route,
)
from patterns.behavioral.chain_of_responsibility.examples.ticket_escalation.models import (
    Resolution,
    Ticket,
)

__all__ = ["Resolution", "Ticket", "build_escalation_chain", "route"]
