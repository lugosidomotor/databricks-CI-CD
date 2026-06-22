"""A wheel taskok közös, Spark nélkül is tesztelhető segédfüggvényei."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from typing import TYPE_CHECKING, Sequence

if TYPE_CHECKING:
    from pyspark.sql import SparkSession


@dataclass(frozen=True)
class TaskConfig:
    """Minden medallion task azonos futási konfigurációja."""

    catalog: str
    schema: str
    run_id: str

    def table(self, name: str) -> str:
        """Biztonságosan idézett, háromrészes Unity Catalog táblanév."""
        return ".".join(quote_identifier(part) for part in (self.catalog, self.schema, name))

    @property
    def schema_ref(self) -> str:
        return ".".join(quote_identifier(part) for part in (self.catalog, self.schema))


def quote_identifier(value: str) -> str:
    """Spark SQL identifier idézése; üres név nem engedélyezett."""
    stripped = value.strip()
    if not stripped:
        raise ValueError("A catalog/schema/table neve nem lehet üres.")
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
    """A runtime-beli SparkSession lekérése, lokális importtal."""
    from pyspark.sql import SparkSession

    return SparkSession.builder.appName(app_name).getOrCreate()


def ensure_schema(spark: SparkSession, config: TaskConfig) -> None:
    spark.sql(f"CREATE SCHEMA IF NOT EXISTS {config.schema_ref}")


def log_event(event: str, **fields: object) -> None:
    """Egyszerű strukturált log, amelyet a job run outputban könnyű keresni."""
    print(json.dumps({"event": event, **fields}, sort_keys=True, default=str))

