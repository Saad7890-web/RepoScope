from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional
import uuid

from .github_client import GitHubClient
from .analyzers.code_quality import CodeQualityAnalyzer
from .analyzers.security import SecurityAnalyzer
from .analyzers.activity import ActivityAnalyzer
from .analyzers.best_practices import BestPracticesAnalyzer
from .reports import json_renderer, pdf_renderer

app = FastAPI(title="RepoScope", description="Analyze GitHub repositories", version="1.0.0")

class AnalyzeRequest(BaseModel):
    repo_url: str
    format: str = "json"  # json or pdf
    github_token: Optional[str] = None

@app.post("/analyze")
async def analyze(request: AnalyzeRequest, background_tasks: BackgroundTasks):
    # Parse repo_url
    parts = request.repo_url.rstrip('/').split('/')
    if len(parts) < 2 or 'github.com' not in parts[-2]:
        raise HTTPException(status_code=400, detail="Invalid GitHub repository URL")
    owner, repo = parts[-2], parts[-1]

    client = GitHubClient(token=request.github_token)

    # Run analyses in parallel (asyncio.gather)
    import asyncio
    try:
        code_quality_task = CodeQualityAnalyzer().analyze(client, owner, repo)
        security_task = SecurityAnalyzer().analyze(client, owner, repo)
        activity_task = ActivityAnalyzer().analyze(client, owner, repo)
        best_practices_task = BestPracticesAnalyzer().analyze(client, owner, repo)

        results = await asyncio.gather(
            code_quality_task,
            security_task,
            activity_task,
            best_practices_task,
            return_exceptions=True
        )
        # Check for exceptions
        for r in results:
            if isinstance(r, Exception):
                raise r

        code_quality, security, activity, best_practices = results

        # Combine data
        report_data = {
            "repo_url": request.repo_url,
            "code_quality": code_quality,
            "security": security,
            "activity": activity,
            "best_practices": best_practices
        }

        if request.format == "pdf":
            pdf_bytes = pdf_renderer.render_pdf(report_data)
            # For simplicity, we'll return PDF as response (could also save to file)
            from fastapi.responses import Response
            return Response(content=pdf_bytes, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=report.pdf"})
        else:
            return json_renderer.render_json(report_data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await client.close()