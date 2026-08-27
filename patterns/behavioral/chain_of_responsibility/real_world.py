"""``logging`` propagation: a record climbs the logger hierarchy.

A child logger with no handlers still gets its records delivered -- they
propagate up the chain until some ancestor's handler takes them.
"""

from __future__ import annotations

import logging


def chain_delivery(sink: list[str]) -> None:
    """Log on the child; watch the parent's handler receive it."""

    class ListHandler(logging.Handler):
        def emit(self, record: logging.LogRecord) -> None:
            sink.append(f"{record.name}: {record.getMessage()}")

    parent = logging.getLogger("cor_demo")
    parent.handlers.clear()
    parent.setLevel(logging.INFO)
    parent.addHandler(ListHandler())

    child = logging.getLogger("cor_demo.web.requests")  # no handlers of its own
    child.info("timeout on /api")


def main() -> None:
    sink: list[str] = []
    chain_delivery(sink)
    print(sink)


if __name__ == "__main__":
    main()
