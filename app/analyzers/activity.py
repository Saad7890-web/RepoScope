import datetime
from typing import Dict, Any, List
from dateutil.parser import parse

class ActivityAnalyzer:
    async def analyze(self, github_client, owner: str, repo: str):
       
        pulls = await github_client.get_pulls(owner, repo, state="closed")
        if len(pulls) > 30:
            pulls = pulls[:30]  

      
        merge_times = []
        for pr in pulls:
            if pr.get("merged_at"):
                created = parse(pr["created_at"])
                merged = parse(pr["merged_at"])
                merge_times.append((merged - created).total_seconds() / 86400)
        avg_merge_time = sum(merge_times) / len(merge_times) if merge_times else None

        repo_data = await github_client.get_repo(owner, repo)
    

        return {
            "total_pulls": len(pulls),
            "average_merge_time_days": avg_merge_time,
           
        }