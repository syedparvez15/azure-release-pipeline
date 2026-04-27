# Pipeline Architecture

## Overview

This repository implements a two-pipeline CI/CD strategy for Azure DevOps — a CI pipeline that validates every pull request, and a CD pipeline that manages staged deployments through to production.

---

## CI Pipeline

**File:** `pipelines/azure-pipelines-ci.yml`

**Trigger:** All pull requests targeting `main` or `develop`

**Stages:**

```
PR Opened
    │
    ▼
Install Dependencies
    │
    ▼
Lint (flake8)
    │
    ▼
Run Tests (pytest + coverage)
    │
    ▼
Publish Results to Azure DevOps
```

**Purpose:** Catch issues early — before any code reaches the main branch. Every PR must pass lint and tests before it can be merged.

---

## CD Pipeline

**File:** `pipelines/azure-pipelines-cd.yml`

**Trigger:** Merge to `main`

**Stages:**

```
Merge to main
    │
    ▼
Build & Package
(run tests, zip artifact)
    │
    ▼
Deploy → Staging
(automated, smoke test after deploy)
    │
    ▼
Manual Approval Gate
(required approver in Azure DevOps Environments)
    │
    ▼
Deploy → Production
```

**Purpose:** Ensure every production deployment is intentional, tested, and approved.

---

## Pre-flight Script

**File:** `scripts/deploy.py`

Run locally before triggering a release to validate the environment is clean:

```bash
python scripts/deploy.py staging
python scripts/deploy.py production
```

**Checks performed:**
- No uncommitted Git changes
- Correct branch for the target environment
- Full test suite passes
- Manual confirmation prompt for production deployments

---

## Environment Variables

| Variable | Used In | Description |
|----------|---------|-------------|
| `AZURE_SUBSCRIPTION` | CD pipeline | Azure service connection name |
| `BUILD_ARTIFACTSTAGINGDIRECTORY` | CD pipeline | Azure DevOps built-in artifact path |

---

## Design Decisions

**Why a separate CI and CD pipeline?**
Keeping them separate makes each pipeline easier to maintain, debug, and update independently. CI runs on every PR; CD only runs on merges to main — they serve different purposes and different audiences.

**Why a manual approval gate before production?**
Automated deployments to staging catch most issues. But production deployments carry business risk — a human approval step ensures a developer has consciously reviewed the staging outcome before proceeding.

**Why a pre-flight script?**
The script acts as a local safeguard before a release is even triggered. It prevents common mistakes like deploying uncommitted changes or deploying from the wrong branch.
