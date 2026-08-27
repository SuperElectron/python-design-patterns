"""Behavioral tests for the org-chart mini-project."""

from __future__ import annotations

import pytest

from patterns.structural.composite.examples.org_chart.__main__ import main
from patterns.structural.composite.examples.org_chart.org import Department, Employee, OrgMetrics


def build_company() -> tuple[Department, Department]:
    platform = Department("platform", [Employee("Ada", 190_000), Employee("Grace", 185_000)])
    company = Department("engineering", [platform, Employee("Barbara", 210_000)])
    return company, platform


class TestRollups:
    def test_both_measures_travel_up_in_one_pass(self) -> None:
        company, _ = build_company()
        assert company.total() == OrgMetrics(headcount=3, annual_cost=585_000)

    def test_a_subtree_reports_only_its_own_people(self) -> None:
        _, platform = build_company()
        assert platform.total() == OrgMetrics(headcount=2, annual_cost=375_000)

    def test_an_empty_department_is_zero_not_an_error(self) -> None:
        assert Department("new-team").total() == OrgMetrics(0, 0)

    def test_a_reorg_moves_cost_between_departments(self) -> None:
        company, platform = build_company()
        hire = Employee("Edsger", 200_000)
        platform.add(hire)
        assert company.total().headcount == 4
        platform.remove(hire)
        assert company.total().headcount == 3


class TestHonesty:
    def test_employees_cannot_hold_reports(self) -> None:
        assert not hasattr(Employee("Ada", 190_000), "add")


class TestDemo:
    def test_main_prints_rollups_per_level(self, capsys: pytest.CaptureFixture[str]) -> None:
        main()
        out = capsys.readouterr().out
        assert "platform: 2 people" in out
        assert "engineering: 4 people" in out
