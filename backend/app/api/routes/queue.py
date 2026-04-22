from fastapi import APIRouter
from app.services.hitl_service import HITLQueueService

router = APIRouter()
# Singleton instance for the prototype
hitl_service = HITLQueueService()

@router.get("/pending")
async def get_pending_reports():
    """
    Returns a prioritized list of AI-generated conflict reports waiting for human approval.
    """
    reports = hitl_service.get_pending()
    return {"status": "success", "data": reports}

@router.post("/resolve/{report_id}")
async def resolve_report(report_id: str, resolution: str):
    """
    Mark a conflict report as resolved.
    """
    if hitl_service.resolve_report(report_id, resolution):
        return {"status": "success", "message": "Report resolved"}
    return {"status": "error", "message": "Report not found"}, 404
