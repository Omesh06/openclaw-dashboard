from fastapi import APIRouter
from app.services.health_scanner_service import RepoHealthScanner

router = APIRouter()

# Mock config for demonstration (In production, this comes from a DB or config file)
REPO_CONFIGS = [
    {
        "path": "/home/ubuntu/.openclaw/workspace/sorch_ai_analysis",
        "branches": ["main", "develop", "staging"],
        "target": "main"
    }
]

@router.get("/status")
async def get_health_status():
    """
    Returns the 'Traffic Light' status for all tracked repositories.
    """
    scanner = RepoHealthScanner(repos=[c["path"] for c in REPO_CONFIGS])
    status = scanner.get_global_status(REPO_CONFIGS)
    return {"status": "success", "data": status}
