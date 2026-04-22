from fastapi import APIRouter
from app.services.audit_service import AuditService

router = APIRouter()
audit_service = AuditService()

@router.get("/metrics")
async def get_metrics():
    """
    Returns aggregated metrics for the Command Center Audit Log.
    """
    return {"status": "success", "metrics": audit_service.get_metrics()}

@router.get("/logs")
async def get_audit_logs():
    """
    Returns the raw history of actions.
    """
    from app.core.database import get_db_connection
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM audit_log ORDER BY timestamp DESC LIMIT 100")
    logs = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return {"status": "success", "logs": logs}
