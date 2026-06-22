# CI/CD Process

## Branch and environment model

```text
feature/* -> pull request -> CI
develop   -> dev deployment -> medallion smoke run
main      -> prod approval -> prod deployment -> medallion smoke run
```

The staging target remains manually controlled. A useful follow-up exercise is adding a
release workflow between the `develop` and `main` branches.

## GitHub Environments

Create GitHub Environments named `dev` and `prod`. Add required reviewers to `prod` and
define these environment variables in both environments:

| Name | Example | Sensitive? |
|---|---|---|
| `DATABRICKS_HOST` | `https://adb-...azuredatabricks.net` | No |
| `DATABRICKS_CLIENT_ID` | Service principal application ID | Not a secret |
| `DATABRICKS_CATALOG` | `main` or a dedicated catalog | No |

The environments can point to different workspaces and service principals.

## OIDC workload identity federation

1. Create separate dev and prod service principals.
2. Add each principal to the appropriate Databricks workspace.
3. Create a GitHub federation policy for the repository and environment subject.
4. Grant the GitHub workflow `id-token: write` permission.
5. Set `DATABRICKS_AUTH_TYPE=github-oidc` in the workflow.

The included workflows already contain the required GitHub-side settings. They do not
need a `DATABRICKS_CLIENT_SECRET`. If the organization cannot use OIDC yet, OAuth M2M
with a client secret is possible, but requires short expiration, rotation, and protected
GitHub Environment secrets.

## Execution boundaries

- The CI job does not connect to a workspace; it lints, tests, and builds the wheel.
- Deployment workflows repeat the quality gate, then authenticate, validate, and deploy.
  They cannot deploy while their own quality checks are failing.
- A smoke run starts Databricks compute and therefore has a cost.
- Production environment approval occurs before deployment and compute startup.

## Rollback

Bundles manage declarative state but do not provide a separate `rollback` command.
Revert to the desired Git commit or release branch, rerun the full CI process, and deploy
that revision to the same target. The sample regenerates its data because tasks use
`overwrite`; production data recovery requires a separate operational procedure.

