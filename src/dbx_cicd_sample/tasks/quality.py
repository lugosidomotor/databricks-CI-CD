"""Quality gate: fail the complete job when its output is invalid."""

from __future__ import annotations

from dbx_cicd_sample.common import get_spark, log_event, parse_task_config


def main() -> None:
    config = parse_task_config()
    spark = get_spark("dbx-cicd-sample-quality")

    from pyspark.sql import functions as F

    target = config.table("gold_daily_sales")
    data = spark.table(target)
    metrics = data.agg(
        F.count("*").alias("row_count"),
        F.sum("order_count").alias("order_count"),
        F.round(F.sum("revenue"), 2).alias("revenue"),
        F.sum(F.when(F.col("revenue") <= 0, 1).otherwise(0)).alias("invalid_revenue_rows"),
    ).first()

    failures: list[str] = []
    if metrics["row_count"] == 0:
        failures.append("The Gold table is empty.")
    if metrics["invalid_revenue_rows"] > 0:
        failures.append("The Gold table contains non-positive revenue.")
    if metrics["order_count"] != 3:
        failures.append(f"Expected 3 valid orders, found {metrics['order_count']}.")
    if float(metrics["revenue"] or 0) != 175.0:
        failures.append(f"Expected revenue of 175.0, found {metrics['revenue']}.")

    log_event("quality_checked", table=target, failures=failures, metrics=metrics.asDict())
    if failures:
        raise RuntimeError("Data quality check failed: " + " ".join(failures))


if __name__ == "__main__":
    main()
