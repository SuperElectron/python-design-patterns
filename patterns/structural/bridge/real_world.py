"""``logging``: a Bridge in daily use.

Logger is the abstraction callers hold; Handlers are the interchangeable
implementation hierarchy on the far side of the bridge.
"""

from __future__ import annotations

import logging


def logger_with_two_backends(name: str, sink_a: list[str], sink_b: list[str]) -> logging.Logger:
    """One abstraction, two implementations receiving the same calls."""

    def handler_for(sink: list[str]) -> logging.Handler:
        class ListHandler(logging.Handler):
            def emit(self, record: logging.LogRecord) -> None:
                sink.append(record.getMessage())

        return ListHandler()

    logger = logging.getLogger(name)
    logger.handlers.clear()
    logger.propagate = False
    logger.setLevel(logging.INFO)
    logger.addHandler(handler_for(sink_a))
    logger.addHandler(handler_for(sink_b))
    return logger


def main() -> None:
    a: list[str] = []
    b: list[str] = []
    logger_with_two_backends("bridge-demo", a, b).info("one call")
    print(f"backend a: {a}, backend b: {b}")


if __name__ == "__main__":
    main()
