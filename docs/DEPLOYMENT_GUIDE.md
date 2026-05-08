# Deployment Guide

This guide covers the end-to-end process for deploying applications using the Azure DevOps CI/CD pipelines in this repository.

---

## Prerequisites

Before triggering a deployment, ensure the following are in place:

- Azure DevOps project with pipeline access
- Service connection configured (see `docs/PIPELINE_VARIABLES.md`)
- Python 3.11+ installed locally
- Required environment variables set (see `.env.example`)
- All pull requests merged and CI pipeline passing on `main`

---

## Deployment Flow

```
Developer merges PR to main
        │
        ▼
CI Pipeline triggers automatically
(lint → test → coverage check)
        │
        ▼
CD Pipeline triggers on CI success
        │
        ▼
Stage 1: Build & Package
- Install dependencies
- Run full test suite
- Create deployment artifact
        │
        ▼
Stage 2: Deploy to Staging
- Upload artifact to Azure App Service (staging slot)
- Run smoke tests against staging URL
- Notify team on success/failure
        │
        ▼
Manual Approval Gate
- Designated approver reviews staging
- Approves or rejects in Azure DevOps Environments
        │
        ▼
Stage 3: Deploy to Production
- Upload artifact to Azure App Service (production slot)
- Run post-deployment smoke tests
- Notify team on completion
```

---

## Running the Pre-flight Script

Before triggering a release, run the pre-flight validation script locally:

```bash
# Validate staging environment
python scripts/deploy.py staging

# Validate production environment
python scripts/deploy.py production
```

The script checks:
- No uncommitted changes in working tree
- Correct branch (`main` for production)
- Full test suite passes locally
- Prompts for manual confirmation before production

---

## Staging Deployment

Staging deployments are **fully automated** — every merge to `main` triggers a staging deployment after a successful build.

To monitor a staging deployment:
1. Go to **Azure DevOps → Pipelines → Runs**
2. Select the latest run
3. Click **Deploy to Staging** stage to view logs

Staging URL should be verified manually before approving production.

---

## Production Deployment

Production deployments require **manual approval** from a designated reviewer.

Steps:
1. Staging deployment completes successfully
2. Reviewer receives notification in Azure DevOps
3. Reviewer checks staging environment
4. Reviewer approves (or rejects) in **Environments → Production**
5. Production deployment proceeds automatically after approval

To approve:
1. Go to **Azure DevOps → Pipelines → Runs → latest run**
2. Click the **Waiting for approval** banner
3. Review and click **Approve**

---

## Rolling Back a Deployment

If a production deployment causes issues:

**Option 1 — Re-deploy previous artifact:**
1. Go to **Pipelines → Runs**
2. Find the last known good run
3. Click **Re-run stages → Deploy to Production**

**Option 2 — Hotfix branch:**
```bash
git checkout -b hotfix/issue-description
# make fix
git push origin hotfix/issue-description
# open PR → merge → triggers new pipeline run
```

---

## Monitoring After Deployment

After each production deployment:
- Check application logs in **Azure Monitor**
- Verify key endpoints are responding
- Monitor error rates for 15–30 minutes post-deploy
- Confirm with stakeholders that business-critical flows are working

---

## Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| Pipeline fails at lint stage | flake8 violations | Run `flake8 .` locally and fix errors |
| Smoke test fails on staging | App not started yet | Wait 60 seconds and re-run smoke test |
| Manual approval timeout | Approver not notified | Check Azure DevOps notification settings |
| Artifact upload fails | Service connection expired | Renew service connection in Project Settings |
