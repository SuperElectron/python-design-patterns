"""``weakref.proxy``: a stdlib proxy with teeth.

It forwards attribute access to the referent without keeping it alive;
once the referent is collected, the proxy raises ReferenceError.
"""

from __future__ import annotations

import weakref


class Service:
    def ping(self) -> str:
        return "pong"


def live_proxy_forwards() -> str:
    service = Service()
    proxy = weakref.proxy(service)
    return str(proxy.ping())


def dead_proxy_raises() -> bool:
    service = Service()
    proxy = weakref.proxy(service)
    del service  # CPython refcounting collects immediately
    try:
        proxy.ping()
    except ReferenceError:
        return True
    return False


def main() -> None:
    print(f"live proxy: {live_proxy_forwards()}")
    print(f"dead proxy raises ReferenceError: {dead_proxy_raises()}")


if __name__ == "__main__":
    main()
