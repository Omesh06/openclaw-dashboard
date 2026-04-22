from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.jira_service import JiraService
from app.services.intent_service import IntentTranslationService

router = APIRouter()
jira_service = JiraService()
intent_service = IntentTranslationService(llm_provider="mock") # Using mock for verification phase

class SummarizeRequest(BaseModel):
    ticket_id: str

@router.post("/summarize")
async def summarize_intent(request: SummarizeRequest):
    """
    Fetch Jira context and translate it into a plain-English 'Intent Summary'.
    """
    try:
        # 1. Fetch context from Jira
        context = jira_service.get_issue_context(request.ticket_id)
        
        # 2. Translate context to intent
        summary = intent_service.summarize_intent(context)
        
        return {
            "ticket_id": request.ticket_id,
            "intent_summary": summary,
            "context_used": context
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
