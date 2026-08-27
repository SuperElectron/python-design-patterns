"""Demo: two charges against an API that fails twice before recovering."""

from __future__ import annotations

from patterns.structural.decorator.examples.resilient_client.client import FlakyPaymentAPI
from patterns.structural.decorator.examples.resilient_client.service import build_charge


def main() -> None:
    api = FlakyPaymentAPI(failures=2)
    charge = build_charge(api, log=lambda line: print(f"  log: {line}"))
    print(f"charge('4242', 1200) = {charge('4242', 1200)}")
    print(f"charge('4000', 800)  = {charge('4000', 800)}")
    print(f"network attempts: {api.attempts} (2 failures retried away)")
    print(f"introspection survives: charge.__name__ = {charge.__name__!r}")


if __name__ == "__main__":
    main()
