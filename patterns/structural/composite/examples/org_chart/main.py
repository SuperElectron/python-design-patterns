"""Demo: headcount and cost rollups over a nested org chart."""

from __future__ import annotations

from patterns.structural.composite.examples.org_chart.org import Department, Employee


def main() -> None:
    platform = Department(
        "platform",
        [Employee("Ada", 190_000), Employee("Grace", 185_000)],
    )
    payments = Department(
        "payments",
        [Employee("Alan", 175_000), platform],  # a department inside a department
    )
    company = Department("engineering", [payments, Employee("Barbara", 210_000)])

    for unit in (platform, payments, company):
        metrics = unit.total()
        print(f"{unit.name}: {metrics.headcount} people, ${metrics.annual_cost:,}/yr")


if __name__ == "__main__":
    main()
