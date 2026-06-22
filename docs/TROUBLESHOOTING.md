# Troubleshooting

## `databricks: command not found`

Install the current Go-based Databricks CLI rather than the legacy `databricks-cli`
Python package. Check it with `databricks version`. The minimum version is declared in
`databricks.yml`.

## Bundle validation has no host or credentials

Select a local authentication profile:

```bash
export DATABRICKS_CONFIG_PROFILE=dev
databricks auth profiles
databricks bundle validate --target dev
```

In CI, check the GitHub Environment variables, `id-token: write` permission, and the
subject configured in the Databricks federation policy.

## The node type does not exist

The default is Azure-specific. Override it with an available workspace node:

```bash
export BUNDLE_VAR_node_type_id=<available-workspace-node>
```

## The job cannot create a schema

Tasks execute `CREATE SCHEMA IF NOT EXISTS`. Grant `USE CATALOG` and `CREATE SCHEMA`, or
pre-create a schema owned by the runtime identity or covered by appropriate grants.

## The report job cannot find its table

Run `medallion_job` successfully first, using the same target and parameters. The report
job is a separate resource and does not depend on another job; this is intentional.

## Serverless pipeline compute is unavailable

Remove `resources/declarative_pipeline.yml` from the bundle include pattern for this
exercise, or replace its compute configuration with settings supported by the workspace.
The wheel-based jobs are independent of this pipeline.

## Tables remain after `bundle destroy`

This is expected. A table created by runtime code is not a bundle-managed resource.
Remove the training schemas separately with the cleanup SQL in the README.

