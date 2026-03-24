class BestPracticesAnalyzer:
    async def analyze(self, github_client, owner: str, repo: str, ref: str = ""):
        files = ["README.md", "LICENSE", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md"]
        results = {}
        for file in files:
            try:
                await github_client.get_contents(owner, repo, file, ref)
                results[file.replace(".md", "")] = True
            except:
                results[file.replace(".md", "")] = False
        return results