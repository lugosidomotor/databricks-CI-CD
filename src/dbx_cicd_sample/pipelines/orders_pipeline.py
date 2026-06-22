# Databricks notebook source
"""Standalone, optional declarative pipeline example.

The ``import dlt`` name is a backward-compatible API. The current product name is
Lakeflow Spark Declarative Pipelines.
"""

import dlt
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.getActiveSession()
if spark is None:
    raise RuntimeError("An active SparkSession is required to run the pipeline.")


@dlt.table(name="pipeline_raw_orders", comment="Raw sample data for the pipeline")
def raw_orders():
    rows = [
        ("P-1001", "2026-01-15T08:30:00Z", "HU", 100.0),
        ("P-1002", "2026-01-15T09:10:00Z", "DE", 50.0),
        ("P-1003", "2026-01-16T10:00:00Z", "HU", 25.0),
        ("P-1004", "invalid", "AT", -1.0),
    ]
    schema = "order_id STRING, order_ts STRING, country STRING, amount DOUBLE"
    return spark.createDataFrame(rows, schema=schema)


@dlt.table(name="pipeline_clean_orders", comment="Orders cleaned with expectations")
@dlt.expect_or_drop("valid_amount", "amount > 0")
@dlt.expect_or_drop("valid_timestamp", "order_timestamp IS NOT NULL")
def clean_orders():
    return dlt.read("pipeline_raw_orders").withColumn("order_timestamp", F.to_timestamp("order_ts"))


@dlt.table(name="pipeline_country_summary", comment="Order aggregates by country")
def country_summary():
    return (
        dlt.read("pipeline_clean_orders")
        .groupBy("country")
        .agg(
            F.countDistinct("order_id").alias("order_count"),
            F.round(F.sum("amount"), 2).alias("revenue"),
        )
    )
