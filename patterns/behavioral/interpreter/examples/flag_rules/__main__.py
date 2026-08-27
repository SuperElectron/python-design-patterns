"""Demo: three users against a small flag config."""

from __future__ import annotations

from patterns.behavioral.interpreter.examples.flag_rules.engine import FlagEngine
from patterns.behavioral.interpreter.pattern import Expr, Value

FLAGS: dict[str, Expr] = {
    "new-dashboard": ("and", (">=", "age", 18), ("==", "country", "CA")),
    "beta-exports": ("or", ("==", "plan", "pro"), ("==", "role", "staff")),
    "legacy-ui": ("not", (">=", "signup_year", 2024)),
}


def main() -> None:
    users: dict[str, dict[str, Value]] = {
        "ada": {"age": 31, "country": "CA", "plan": "pro", "role": "user", "signup_year": 2021},
        "lin": {"age": 17, "country": "CA", "plan": "free", "role": "staff", "signup_year": 2025},
        "sam": {"age": 40, "country": "US", "plan": "free", "role": "user", "signup_year": 2024},
    }
    engine = FlagEngine(FLAGS)
    for name, user in users.items():
        verdicts = ", ".join(
            f"{flag}={'on' if on else 'off'}" for flag, on in engine.rollout(user).items()
        )
        print(f"{name}: {verdicts}")


if __name__ == "__main__":
    main()
