# Pipeline Variables

This document lists all variables required to run the CI and CD pipelines in Azure DevOps.

---

## CI Pipeline Variables

| Variable | Type | Description |
|----------|------|-------------|
| `PYTHON_VERSION` | String | Python version to use (default: `3.11`) |
| `PIP_CACHE_DIR` | String | Directory for pip cache (default: `$(Pipeline.Workspace)/.pip`) |

---

## CD Pipeline Variables

| Variable | Type | Required | Description |
|----------|------|----------|-------------|
| `AZURE_SUBSCRIPTION` | Service Connection | ✅ Yes | Azure DevOps service connection name |
| `STAGING_APP_NAME` | String | ✅ Yes | Name of the staging app service |
| `PRODUCTION_APP_NAME` | String | ✅ Yes | Name of the production app service |
| `RESOURCE_GROUP` | String | ✅ Yes | Azure resource group name |
| `BUILD_ARTIFACT_NAME` | String | No | Name of the build artifact (default: `drop`) |

---

## How to Set Variables in Azure DevOps

1. Go to **Pipelines → your pipeline → Edit**
2. Click **Variables** (top right)
3. Add each variable with its value
4. For sensitive values, check **"Keep this value secret"**

For service connections:
1. Go to **Project Settings → Service connections**
2. Click **New service connection → Azure Resource Manager**
3. Follow the prompts and name it to match `AZURE_SUBSCRIPTION`

---

## Local Development (.env)

For running `scripts/deploy.py` locally, you can set environment variables directly:

```bash
export AZURE_SUBSCRIPTION="my-service-connection"
export STAGING_APP_NAME="my-app-staging"
export PRODUCTION_APP_NAME="my-app-prod"
export RESOURCE_GROUP="my-resource-group"
```

Or create a `.env` file (never commit this — it's in `.gitignore`):

```
AZURE_SUBSCRIPTION=my-service-connection
STAGING_APP_NAME=my-app-staging
PRODUCTION_APP_NAME=my-app-prod
RESOURCE_GROUP=my-resource-group
```
