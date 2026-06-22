"""Gold task: napi, országonkénti üzleti aggregáció."""

from __future__ import annotations

from dbx_cicd_sample.common import get_spark, log_event, parse_task_config


def main() -> None:
    config = parse_task_config()
    spark = get_spark("dbx-cicd-sample-gold")

    from pyspark.sql import functions as F

    source = config.table("silver_orders")
    target = config.table("gold_daily_sales")
    gold = (
        spark.table(source)
        .withColumn("order_date", F.to_date("order_timestamp"))
        .groupBy("order_date", "country")
        .agg(
            F.countDistinct("order_id").alias("order_count"),
            F.round(F.sum("amount"), 2).alias("revenue"),
            F.round(F.avg("amount"), 2).alias("average_order_value"),
        )
        .withColumn("calculated_at", F.current_timestamp())
    )
    (
        gold.write.format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable(target)
    )
    log_event("gold_written", source=source, table=target, row_count=gold.count())


if __name__ == "__main__":
    main()

