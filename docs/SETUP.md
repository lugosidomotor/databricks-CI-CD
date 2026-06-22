# Workspace Setup

## 1. Permissions

The developer or runtime service principal needs at least:

- Workspace access and permission to create jobs.
- Permission to use the configured compute policy or create clusters.
- `USE CATALOG` on the selected catalog.
- `CREATE SCHEMA` on the catalog.
- Permission to use and write the resulting schemas and tables.
- Serverless pipeline access for the declarative pipeline example.

Do not grant account-admin or workspace-admin permissions to the CI identity in a real
production setup.

## 2. Cloud-specific compute

The default node type targets Azure:

```bash
export BUNDLE_VAR_node_type_id=Standard_D4s_v5
```

Choose a node type available in your workspace when using AWS or GCP. If a cluster
policy is mandatory, add its `policy_id` to each `new_cluster` block. Do not override
fields that the policy fixes to specific values.

## 3. Secret example

Secret scope creation is an administrative operation. Do not put the secret value in
shell history. After creating the scope and key, override their non-sensitive names if
needed:

```bash
export BUNDLE_VAR_secret_scope=dbx-cicd-sample
export BUNDLE_VAR_secret_key=sample-secret
databricks bundle deploy --target dev
databricks bundle run --target dev secret_example_job
```

The job run identity needs `READ` access to the scope. A Python wheel task does not
receive the notebook-global `dbutils` object, so this example creates a
`pyspark.dbutils.DBUtils` instance explicitly.

## 4. Production run identity

The bundle contains a sentinel default so `dev` validation does not require a production
service principal. Always override it for `staging` and `prod`:

```bash
export BUNDLE_VAR_service_principal_id=<application-id>
databricks bundle validate --target prod
databricks bundle deploy --target prod
```

The deployment identity must be allowed to use the configured service principal. Give
the runtime service principal only the data and compute permissions it needs; it should
not receive unrelated administrative permissions.
