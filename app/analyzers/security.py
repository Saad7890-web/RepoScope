import subprocess
import tempfile
from typing import Dict, Any, Optional

class SecurityAnalyzer:
    async def analyze(self, github_client, owner: str, repo: str, ref: str = ""):
        # Look for dependency files
        dep_files = ["requirements.txt", "Pipfile", "pyproject.toml", "package.json", "Gemfile"]
        vulnerabilities = []
        for filename in dep_files:
            content = await github_client.get_file_content(owner, repo, filename, ref)
            if content:
                # Save to temporary file and run safety (for Python deps)
                if filename == "requirements.txt":
                    with tempfile.NamedTemporaryFile(mode='w+', suffix='.txt') as f:
                        f.write(content)
                        f.flush()
                        result = subprocess.run(["safety", "check", "-r", f.name], capture_output=True, text=True)
                        if result.returncode != 0:
                            vulnerabilities.append({"file": filename, "output": result.stdout})
        return {
            "has_dependency_files": bool(vulnerabilities or any(await self._has_file(github_client, owner, repo, f, ref) for f in dep_files)),
            "vulnerabilities": vulnerabilities,
            "security_score": 0 if vulnerabilities else 1
        }

    async def _has_file(self, client, owner, repo, path, ref):
        try:
            await client.get_contents(owner, repo, path, ref)
            return True
        except:
            return False