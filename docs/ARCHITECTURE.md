# Architecture and Design Decisions

## Lakeflow Jobs and declarative pipelines serve different purposes

| Question | Lakeflow Jobs | Lakeflow Spark Declarative Pipelines |
|---|---|---|
| Primary role | General DAG and orchestration | Declarative batch or streaming data flow |
| Execution unit | Task | Materialized view or table |
| Supported code | Wheel, script, notebook, SQL, dbt, pipeline task | Python or SQL pipeline API |
| Dependencies | Explicit `depends_on` edges | Inferred from table reads |
| Data quality | Custom quality task or external check | Built-in expectations |

This repository demonstrates both models:

- `medallion_job` is an explicit task DAG using Python wheel entry points.
- `orders_declarative_pipeline` uses declarative tables and expectations.
- `pipeline_orchestrator_job` shows how a Job starts a pipeline update.

## Why use a wheel instead of loose Python files?

A wheel is a versioned artifact that can be tested locally. The job does not perform a
Git checkout; it executes the build uploaded during deployment. This provides several
useful properties:

1. The same code passes CI and is deployed to the workspace.
2. Imports and entry points use standard Python packaging mechanisms.
3. Production execution does not depend on GitHub availability.
4. A previous commit can reproduce an earlier artifact for rollback.

## Environment isolation

The bundle identity consists of its name, target, and workspace. Development mode uses
a developer-specific resource prefix and isolated bundle state. This project also adds
the developer short name to Unity Catalog schemas because resource-level isolation alone
would not isolate tables created by task code.

Staging and production use a stable `/Workspace/Shared/.bundle/...` root and a service
principal `run_as` identity. The deployment identity and runtime identity may be
different service principals with different permissions.

## Compute

The three transformation tasks and quality gate share one `job_cluster_key`. One cluster
therefore starts per job run rather than one cluster per task. The sample uses a
single-node Azure configuration to reduce training costs. Override `node_type_id` or the
complete `new_cluster` block for another cloud, policy, or workload size.

The declarative pipeline requests serverless compute. If the workspace does not support
it, configure classic pipeline compute or remove that example resource.

## Idempotency

Every sample layer is written in `overwrite` mode, so repeated runs with the same input
produce the same business result. This is useful for training but is not a default
production recommendation. Large production datasets typically require incremental
ingestion, checkpoints, `MERGE`, Auto Loader, or declarative streaming tables.

## Parameters and secrets

- Bundle variable: non-sensitive environment configuration resolved during deployment.
- Job parameter: business or runtime value that can be overridden for one run.
- Secret scope: runtime retrieval of passwords, tokens, and keys.
- GitHub OIDC: short-lived CI authentication without a stored Databricks client secret.

Never place a secret value in `databricks.yml`, `.env.example`, task parameters, or logs.

