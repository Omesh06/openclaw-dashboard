from fastapi import APIRouter, HTTPException
from app.services.jira_service import JiraService

router = APIRouter()
jira_service = JiraService()

@router.get("/ticket/{ticket_id}")
async def get_ticket_context(ticket_id: str):
    """
    Fetch the full context of a Jira ticket, including description and comments.
    """
    try:
        context = jira_service.get_issue_context(ticket_id)
        return context
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
