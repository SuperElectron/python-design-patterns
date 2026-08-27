"""Behavioral tests for the report-job mini-project."""

from patterns.creational.prototype.examples.report_job_templates import Scheduler


class TestScheduler:
    def test_templates_stamp_out_fresh_equal_jobs(self) -> None:
        scheduler = Scheduler()
        a = scheduler.enqueue("nightly-sales")
        b = scheduler.enqueue("nightly-sales")
        assert a is not b
        assert a == b
        assert a.filters == ("exclude-test-accounts",)

    def test_per_run_overrides_leave_the_template_untouched(self) -> None:
        scheduler = Scheduler()
        rush = scheduler.enqueue("weekly-audit", fmt="csv")
        assert rush.fmt == "csv"
        assert scheduler.menu.create("weekly-audit").fmt == "xlsx"

    def test_queue_holds_customized_jobs_in_order(self) -> None:
        scheduler = Scheduler()
        scheduler.enqueue("nightly-sales")
        scheduler.enqueue("weekly-audit", recipients=("audit@example.com",))
        assert [job.name for job in scheduler.queue] == ["nightly-sales", "weekly-audit"]
        assert scheduler.queue[1].recipients == ("audit@example.com",)

    def test_menu_lists_its_templates(self) -> None:
        assert Scheduler().menu.names() == ["nightly-sales", "weekly-audit"]
