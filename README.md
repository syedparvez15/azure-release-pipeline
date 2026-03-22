# 🚀 Azure Release Pipeline

![Azure DevOps](https://img.shields.io/badge/Azure_DevOps-0078D7?style=for-the-badge&logo=azure-devops&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![CI/CD](https://img.shields.io/badge/CI%2FCD-Pipeline-0089D6?style=for-the-badge&logo=microsoft-azure&logoColor=white)

A production-grade CI/CD pipeline configuration for Azure DevOps, with a Python pre-deployment checklist script. Built to support reliable, repeatable software releases across staging and production environments.

---

## 📌 What This Covers

- **CI Pipeline** — triggered on PRs and feature branches: install, lint, test, publish coverage
- **CD Pipeline** — triggered on merges to `main`: build → deploy staging → manual approval → deploy production
- **Pre-flight script** — Python CLI to run checks before triggering a release (git status, branch, tests, production confirmation)

---

## 🗂️ Project Structure

```
azure-release-pipeline/
│
├── pipelines/
│   ├── azure-pipelines-ci.yml    # CI — lint, test, coverage on PRs
│   └── azure-pipelines-cd.yml    # CD — staging + production deployment
│
├── scripts/
│   └── deploy.py                 # Pre-deployment checklist CLI
│
└── README.md
```

---

## ⚙️ Pipeline Overview

### CI Pipeline (`azure-pipelines-ci.yml`)

Triggers on all PRs targeting `main` or `develop`.

| Step | Description |
|------|-------------|
| Set Python version | Uses Python 3.11 |
| Cache pip packages | Speeds up subsequent runs |
| Install dependencies | From `requirements.txt` |
| Lint with flake8 | Enforces code style |
| Run tests | pytest with coverage reporting |
| Publish results | Test results + coverage to Azure DevOps |

### CD Pipeline (`azure-pipelines-cd.yml`)

Triggers on merge to `main`.

| Stage | Trigger | Notes |
|-------|---------|-------|
| Build & Package | Automatic | Runs tests, zips artifact |
| Deploy → Staging | Automatic | Smoke test after deploy |
| Deploy → Production | **Manual approval required** | Approval gate in Azure DevOps |

---

## 🛡️ Pre-flight Deployment Script

Run before triggering a release to validate your environment:

```bash
# Staging deployment check
python scripts/deploy.py staging

# Production deployment check (requires manual 'yes' confirmation)
python scripts/deploy.py production

# Skip test run (if CI already ran them)
python scripts/deploy.py staging --skip-tests

# Specify a different branch
python scripts/deploy.py production --branch release/v2.1
```

### Checks performed:
- ✅ No uncommitted Git changes
- ✅ Correct branch for environment
- ✅ Full test suite passes
- ✅ Manual confirmation for production

---

## 🔧 Setup

### 1. Import pipelines into Azure DevOps
- Go to **Pipelines → New Pipeline**
- Select your repo and point to the relevant YAML file

### 2. Configure environment approvals
- Go to **Environments → production**
- Add an **Approval** check with required approvers

### 3. Set pipeline variables
| Variable | Description |
|----------|-------------|
| `AZURE_SUBSCRIPTION` | Azure service connection name |

---

## 👤 Author

**Syed Parvez** — [LinkedIn](https://www.linkedin.com/in/syedparvez15/) | [GitHub](https://github.com/syedparvez15)
