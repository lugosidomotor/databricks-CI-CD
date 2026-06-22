"""Bronze task: nyers mintaadat idempotens betöltése Delta táblába."""

from __future__ import annotations

from dbx_cicd_sample.common import ensure_schema, get_spark, log_event, parse_task_config
from dbx_cicd_sample.sample_data import RAW_ORDER_SCHEMA, sample_orders


def main() -> None:
    config = parse_task_config()
    spark = get_spark("dbx-cicd-sample-bronze")
    ensure_schema(spark, config)

    from pyspark.sql import functions as F

    rows = sample_orders()
    bronze = (
        spark.createDataFrame(rows, schema=RAW_ORDER_SCHEMA)
        .withColumn("ingestion_run_id", F.lit(config.run_id))
        .withColumn("ingested_at", F.current_timestamp())
    )
    target = config.table("bronze_orders")
    (
        bronze.write.format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable(target)
    )
    log_event("bronze_written", table=target, row_count=len(rows), run_id=config.run_id)


if __name__ == "__main__":
    main()

