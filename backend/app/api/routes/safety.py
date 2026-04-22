from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from app.services.safety_service import SafetyService
from app.services.rules_engine_service import RulesEngineService

router = APIRouter()

# Mock repo path for prototype. In production, this would be dynamic.
REPO_PATH = "/home/ubuntu/.openclaw/workspace/sorch_ai_analysis"
safety_service = SafetyService(REPO_PATH)
rules_service = RulesEngineService()

class DryRunRequest(BaseModel):
    source_branch: str
    target_branch: str
    test_command: List[str] = ["python3", "-m", "pytest"]

@router.post("/dry-run")
async def perform_dry_run(request: DryRunRequest):
    """
    Create sandbox, attempt merge, and run tests.
    """
    # 1. Create sandbox and merge
    sandbox_res = safety_service.create_dry_run_sandbox(request.source_branch, request.target_branch)
    if "error" in sandbox_res:
        raise HTTPException(status_code=500, detail=sandbox_res["error"])
    
    sandbox_branch = sandbox_res["sandbox_branch"]
    
    try:
        # 2. Run tests
        test_passed = safety_service.run_sandbox_tests(sandbox_branch, request.test_command)
        return {
            "sandbox_branch": sandbox_branch,
            "merge_success": sandbox_res["merge_success"],
            "tests_passed": test_passed,
            "output": sandbox_res["output"]
        }
    finally:
        # 3. Always cleanup
        safety_service.cleanup_sandbox(sandbox_branch)

@router.post("/revert")
async def panic_revert(target_branch: str):
    """
    Trigger the Panic Button: Revert the last merge commit on the target branch.
    """
    result = safety_service.execute_panic_revert(target_branch)
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    return result

@router.get("/rules")
async def get_rules():
    return {"rules": rules_service.rules}

@router.post("/rules/update")
async def update_rule(rule_name: str, value: bool):
    rules_service.update_rule(rule_name, value)
    return {"status": "success", "updated_rule": rule_name}
