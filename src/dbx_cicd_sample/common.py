"""Shared wheel-task helpers that can be tested without Spark."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pyspark.sql import SparkSession


@dataclass(frozen=True)
class TaskConfig:
    """Shared runtime configuration for every medallion task."""

    catalog: str
    schema: str
    run_id: str

    def table(self, name: str) -> str:
        """Return a safely quoted three-part Unity Catalog table name."""
        return ".".join(quote_identifier(part) for part in (self.catalog, self.schema, name))

    @property
    def schema_ref(self) -> str:
        return ".".join(quote_identifier(part) for part in (self.catalog, self.schema))


def quote_identifier(value: str) -> str:
    """Quote a Spark SQL identifier; blank names are rejected."""
    stripped = value.strip()
    if not stripped:
        raise ValueError("Catalog, schema, and table names cannot be blank.")
    return f"`{stripped.replace('`', '``')}`"


def parse_task_config(argv: Sequence[str] | None = None) -> TaskConfig:
    parser = argparse.ArgumentParser(description="Databricks sample medallion task")
    parser.add_argument("--catalog", required=True)
    parser.add_argument("--schema", required=True)
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args(argv)
    return TaskConfig(
        catalog=args.catalog.strip(),
        schema=args.schema.strip(),
        run_id=args.run_id.strip(),
    )


def get_spark(app_name: str) -> SparkSession:
    """Get the runtime SparkSession using a local import."""
    from pyspark.sql import SparkSession

    return SparkSession.builder.appName(app_name).getOrCreate()


def ensure_schema(spark: SparkSession, config: TaskConfig) -> None:
    spark.sql(f"CREATE SCHEMA IF NOT EXISTS {config.schema_ref}")


def log_event(event: str, **fields: object) -> None:
    """Write a simple structured log that is easy to search in job output."""
    print(json.dumps({"event": event, **fields}, sort_keys=True, default=str))
