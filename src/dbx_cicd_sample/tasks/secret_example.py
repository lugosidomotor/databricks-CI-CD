"""Use a secret scope from a wheel task without logging the secret value."""

from __future__ import annotations

import argparse

from dbx_cicd_sample.common import get_spark, log_event


def main() -> None:
    parser = argparse.ArgumentParser(description="Databricks secret scope sample")
    parser.add_argument("--scope", required=True)
    parser.add_argument("--key", required=True)
    args = parser.parse_args()

    from pyspark.dbutils import DBUtils

    secret = DBUtils(get_spark("dbx-cicd-sample-secret")).secrets.get(
        scope=args.scope,
        key=args.key,
    )
    if not secret:
        raise RuntimeError("The secret exists but is empty.")
    log_event("secret_read_successfully", scope=args.scope, key=args.key)


if __name__ == "__main__":
    main()
