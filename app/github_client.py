import httpx
from typing import Dict, Any, List, Optional
from urllib.parse import urlparse

class GitHubClient:
    BASE_URL = "https://api.github.com"

    def __init__(self, token: Optional[str] = None):
        self.client = httpx.AsyncClient(
            base_url=self.BASE_URL,
            headers={"Authorization": f"token {token}"} if token else {},
            timeout=30.0
        )

    async def close(self):
        await self.client.aclose()

    async def get_repo(self, owner: str, repo: str) -> Dict[str, Any]:
        response = await self.client.get(f"/repos/{owner}/{repo}")
        response.raise_for_status()
        return response.json()

    async def get_contents(self, owner: str, repo: str, path: str = "", ref: str = "") -> List[Dict[str, Any]]:
        url = f"/repos/{owner}/{repo}/contents/{path}"
        params = {}
        if ref:
            params["ref"] = ref
        response = await self.client.get(url, params=params)
        response.raise_for_status()
        return response.json()

    async def get_file_content(self, owner: str, repo: str, path: str, ref: str = "") -> Optional[str]:
        data = await self.get_contents(owner, repo, path, ref)
        if isinstance(data, list):
            # If path is a directory, we can't fetch a single file
            return None
        import base64
        content = data.get("content", "")
        if content:
            return base64.b64decode(content).decode("utf-8")
        return None

    async def get_pulls(self, owner: str, repo: str, state: str = "all") -> List[Dict[str, Any]]:
        response = await self.client.get(f"/repos/{owner}/{repo}/pulls", params={"state": state})
        response.raise_for_status()
        return response.json()

    async def get_issues(self, owner: str, repo: str, state: str = "all") -> List[Dict[str, Any]]:
        response = await self.client.get(f"/repos/{owner}/{repo}/issues", params={"state": state})
        response.raise_for_status()
        return response.json()

    async def get_commits(
        self,
        owner: str,
        repo: str,
        branch: Optional[str] = None,
        per_page: int = 30
    ) -> List[Dict[str, Any]]:
        params = {"per_page": per_page}
        if branch:
            params["sha"] = branch

        return await self._get(f"/repos/{owner}/{repo}/commits", params)