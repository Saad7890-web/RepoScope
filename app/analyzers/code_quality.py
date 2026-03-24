import os
from typing import Dict, Any, List

class CodeQualityAnalyzer:
    async def analyze(self, github_client, owner: str, repo: str, ref: str = ""):
        # Check for test directory
        test_paths = ["test/", "tests/", "test.py", "tests.py"]
        found_tests = False
        for path in test_paths:
            try:
                contents = await github_client.get_contents(owner, repo, path, ref)
                if isinstance(contents, list) or (isinstance(contents, dict) and "name" in contents):
                    found_tests = True
                    break
            except httpx.HTTPStatusError:
                continue

        # Check for CI config files
        ci_files = [".github/workflows/", ".gitlab-ci.yml", "circle.yml", "travis.yml", "Jenkinsfile"]
        found_ci = False
        for ci_file in ci_files:
            try:
                await github_client.get_contents(owner, repo, ci_file, ref)
                found_ci = True
                break
            except httpx.HTTPStatusError:
                continue

        return {
            "has_tests": found_tests,
            "has_ci": found_ci,
            "test_score": 1 if found_tests else 0,
            "ci_score": 1 if found_ci else 0,
            # Could add more like linting config presence
        }