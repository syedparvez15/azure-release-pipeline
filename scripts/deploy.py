#!/usr/bin/env python3
"""
deploy.py
---------
Pre-deployment checklist and deployment orchestration script.
Run this before triggering an Azure DevOps release pipeline to validate
the environment and confirm all pre-release conditions are met.
"""

import argparse
import logging
import subprocess
import sys
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

ENVIRONMENTS = ["staging", "production"]


def check_git_status() -> bool:
    """Ensure there are no uncommitted changes before deploying."""
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True, text=True
    )
    if result.stdout.strip():
        logger.error("Uncommitted changes detected. Commit or stash before deploying.")
        return False
    logger.info("Git status: clean ✓")
    return True


def check_branch(expected_branch: str) -> bool:
    """Ensure deployment is running from the correct branch."""
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True, text=True
    )
    current = result.stdout.strip()
    if current != expected_branch:
        logger.error(f"Expected branch '{expected_branch}', currently on '{current}'.")
        return False
    logger.info(f"Branch: {current} ✓")
    return True


def check_tests() -> bool:
    """Run test suite and fail deployment if tests don't pass."""
    logger.info("Running test suite...")
    result = subprocess.run(["pytest", "tests/", "-v", "--tb=short"], capture_output=False)
    if result.returncode != 0:
        logger.error("Tests failed. Deployment aborted.")
        return False
    logger.info("All tests passed ✓")
    return True


def confirm_deployment(environment: str) -> bool:
    """Require manual confirmation for production deployments."""
    if environment == "production":
        confirm = input(
            f"\n⚠️  You are about to deploy to PRODUCTION.\n"
            f"Type 'yes' to confirm: "
        ).strip().lower()
        if confirm != "yes":
            logger.info("Deployment cancelled by user.")
            return False
    return True


def run_preflight_checks(environment: str, branch: str, skip_tests: bool = False) -> bool:
    """
    Run all pre-deployment checks in sequence.
    Returns True only if all checks pass.
    """
    logger.info(f"Running pre-flight checks for '{environment}' deployment...")
    logger.info("-" * 50)

    checks = [
        ("Git status", check_git_status),
        ("Branch validation", lambda: check_branch(branch)),
    ]

    if not skip_tests:
        checks.append(("Test suite", check_tests))

    all_passed = True
    for name, check in checks:
        logger.info(f"Checking: {name}")
        if not check():
            logger.error(f"Pre-flight check FAILED: {name}")
            all_passed = False
            break

    return all_passed


def main():
    parser = argparse.ArgumentParser(description="Pre-deployment checklist runner")
    parser.add_argument("environment", choices=ENVIRONMENTS, help="Target environment")
    parser.add_argument("--branch", default="main", help="Expected Git branch (default: main)")
    parser.add_argument("--skip-tests", action="store_true", help="Skip test execution")
    args = parser.parse_args()

    logger.info("=" * 60)
    logger.info(f"Deployment Pre-flight: {args.environment.upper()}")
    logger.info(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 60)

    if not run_preflight_checks(args.environment, args.branch, args.skip_tests):
        logger.error("Pre-flight checks did not pass. Deployment blocked.")
        sys.exit(1)

    if not confirm_deployment(args.environment):
        sys.exit(0)

    logger.info("=" * 60)
    logger.info("All pre-flight checks passed. Triggering Azure DevOps pipeline...")
    logger.info("Navigate to Azure DevOps > Pipelines > Release to monitor progress.")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
