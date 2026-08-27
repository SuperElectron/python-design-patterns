"""Report jobs stamped from templates, built on the Prototype's Python form.

Run it: ``uv run python -m patterns.creational.prototype.examples.report_job_templates``
"""

from patterns.creational.prototype.examples.report_job_templates.models import ReportJob
from patterns.creational.prototype.examples.report_job_templates.scheduler import (
    Scheduler,
    build_template_menu,
)

__all__ = ["ReportJob", "Scheduler", "build_template_menu"]
