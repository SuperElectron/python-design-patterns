"""Demo: the same report skeleton delivered as CSV, then as Markdown."""

from __future__ import annotations

from patterns.behavioral.template_method.examples.report_pipeline.pipeline import (
    build_csv_report,
    build_markdown_report,
)


def main() -> None:
    print("-- csv --")
    build_csv_report().run()
    print("-- markdown --")
    build_markdown_report().run()


if __name__ == "__main__":
    main()
