"""The canonical class attribute factory: ``HTTPConnection.response_class``.

The connection builds its response objects through a class attribute, so a
one-line subclass swaps in your own response type -- no network needed to
see the wiring.
"""

from __future__ import annotations

from http.client import HTTPConnection, HTTPResponse


class LoggedResponse(HTTPResponse):
    """A custom response type the connection should build instead."""


class LoggedConnection(HTTPConnection):
    response_class = LoggedResponse


def factory_of(cls: type[HTTPConnection]) -> type[HTTPResponse]:
    result = cls.response_class
    assert isinstance(result, type)
    return result


def main() -> None:
    print(f"stock factory:      {factory_of(HTTPConnection).__name__}")
    print(f"overridden factory: {factory_of(LoggedConnection).__name__}")


if __name__ == "__main__":
    main()
