# Rollback Guide

## When to Roll Back
- Critical bug in production
- Failed smoke tests post-deployment
- Business decision to revert

## Steps
1. Go to Azure DevOps → Pipelines → Runs
2. Find the last known good run
3. Click Re-run stages → Deploy to Production
4. Monitor logs and verify after rollback

## Hotfix Process
```bash
git checkout -b hotfix/issue-name
# make fix
git push origin hotfix/issue-name
# open PR → merge → pipeline triggers
```
