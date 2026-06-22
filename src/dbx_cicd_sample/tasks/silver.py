"""Silver task: tisztítás, típusosítás és deduplikáció."""

from __future__ import annotations

from dbx_cicd_sample.common import get_spark, log_event, parse_task_config


def main() -> None:
    config = parse_task_config()
    spark = get_spark("dbx-cicd-sample-silver")

    from pyspark.sql import functions as F

    source = config.table("bronze_orders")
    target = config.table("silver_orders")
    silver = (
        spark.table(source)
        .withColumn("order_timestamp", F.to_timestamp("order_ts"))
        .withColumn("country", F.upper(F.trim("country")))
        .withColumn("status", F.upper(F.trim("status")))
        .filter(F.col("order_timestamp").isNotNull())
        .filter(F.col("customer_id").isNotNull())
        .filter(F.col("amount") > 0)
        .filter(F.col("status").isin("COMPLETED", "PENDING"))
        .dropDuplicates(["order_id"])
        .select(
            "order_id",
            "order_timestamp",
            "customer_id",
            "country",
            "amount",
            "status",
            "ingestion_run_id",
            "ingested_at",
        )
    )
    (
        silver.write.format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable(target)
    )
    log_event("silver_written", source=source, table=target, row_count=silver.count())


if __name__ == "__main__":
    main()

