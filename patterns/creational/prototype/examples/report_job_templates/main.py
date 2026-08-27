"""Demo: a night's report runs stamped from the template menu."""

from __future__ import annotations

from patterns.creational.prototype.examples.report_job_templates.scheduler import Scheduler


def main() -> None:
    scheduler = Scheduler()
    scheduler.enqueue("nightly-sales")
    rush = scheduler.enqueue("weekly-audit", fmt="csv", recipients=("cfo@example.com",))

    print(f"menu:   {scheduler.menu.names()}")
    print(f"queued: {[job.name for job in scheduler.queue]}")
    print(f"per-run override: {rush.fmt}")
    print(f"template untouched: {scheduler.menu.create('weekly-audit').fmt}")


if __name__ == "__main__":
    main()
