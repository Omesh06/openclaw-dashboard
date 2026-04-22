from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.services.diff_service import DiffService
from app.services.merge_executor_service import MergeExecutorService

router = APIRouter()

# Mock repo path for prototype.
REPO_PATH = "/home/ubuntu/.openclaw/workspace/sorch_ai_analysis"
diff_service = DiffService(REPO_PATH)
merge_service = MergeExecutorService(REPO_PATH)

class DiffRequest(BaseModel):
    branch_a: str
    branch_b: str
    proposal_branch: str

class TweakRequest(BaseModel):
    branch_name: str
    file_path: str
    new_content: str

class MergeRequest(BaseModel):
    source_branch: str
    target_branch: str

@router.get("/diff")
async def get_resolution_diff(req: DiffRequest):
    """
    Generates the 3-way diff for the resolution workspace.
    """
    try:
        return diff_service.get_3way_diff(req.branch_a, req.branch_b, req.proposal_branch)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/update-proposal")
async def update_proposal(req: TweakRequest):
    """
    Updates the proposed code in the sandbox branch with developer tweaks.
    """
    result = merge_service.apply_developer_tweak(req.branch_name, req.file_path, req.new_content)
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    return result

@router.post("/merge")
async def execute_final_merge(req: MergeRequest):
    """
    Executes the final merge of the approved proposal into SIT/UAT.
    """
    result = merge_service.finalize_merge(req.source_branch, req.target_branch)
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    return result
