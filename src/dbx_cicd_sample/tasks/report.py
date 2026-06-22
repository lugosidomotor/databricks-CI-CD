"""Külön job entry point a Gold eredmény emberi olvasásához."""

from __future__ import annotations

from dbx_cicd_sample.common import get_spark, log_event, parse_task_config


def main() -> None:
    config = parse_task_config()
    spark = get_spark("dbx-cicd-sample-report")

    from pyspark.sql import functions as F

    source = config.table("gold_daily_sales")
    report = spark.table(source).orderBy(F.desc("revenue"), F.asc("country"))
    log_event("report_started", source=source, run_id=config.run_id)
    report.show(100, truncate=False)


if __name__ == "__main__":
    main()

