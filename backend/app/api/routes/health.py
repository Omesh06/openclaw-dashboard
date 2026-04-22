from fastapi import APIRouter
from app.services.health_cache_service import HealthCacheService

router = APIRouter()

# Mock config for demonstration
REPO_CONFIGS = [
    {
        "path": "/home/ubuntu/.openclaw/workspace/sorch_ai_analysis",
        "branches": ["main", "develop", "staging"],
        "target": "main"
    }
]

# Initialize cache service
cache_service = HealthCacheService(REPO_CONFIGS)

@router.get("/status")
async def get_health_status():
    """
    Returns the cached 'Traffic Light' status for all tracked repositories.
    """
    status = cache_service.get_status()
    return {"status": "success", "data": status}
