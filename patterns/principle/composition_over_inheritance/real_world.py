"""The ``logging`` module: composition at industrial scale.

A Logger composes Handlers and Filters; nobody subclasses per combination.
"""

from __future__ import annotations

import logging


def build_error_logger(name: str, sink: list[str]) -> logging.Logger:
    """Compose: a list-writing handler + a substring filter, one stock Logger."""

    class ListHandler(logging.Handler):
        def emit(self, record: logging.LogRecord) -> None:
            sink.append(record.getMessage())

    logger = logging.getLogger(name)
    logger.handlers.clear()
    logger.propagate = False
    logger.setLevel(logging.INFO)
    handler = ListHandler()
    handler.addFilter(lambda record: "error" in record.getMessage())
    logger.addHandler(handler)
    return logger


def main() -> None:
    sink: list[str] = []
    logger = build_error_logger("demo", sink)
    logger.info("error: disk full")
    logger.info("all fine")
    print(sink)


if __name__ == "__main__":
    main()
