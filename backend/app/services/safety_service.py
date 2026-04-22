import subprocess
import os
import uuid
from typing import List, Optional

class SafetyService:
    def __init__(self, repo_path: str):
        self.repo_path = repo_path

    def create_dry_run_sandbox(self, source_branch: str, target_branch: str) -> str:
        """
        Creates a temporary hidden branch, attempts to merge, and returns the sandbox branch name.
        """
        sandbox_name = f"sandbox-dryrun-{uuid.uuid4().hex[:8]}"
        try:
            # 1. Checkout target branch
            subprocess.run(["git", "checkout", target_branch], cwd=self.repo_path, check=True, capture_output=True)
            
            # 2. Create sandbox branch
            subprocess.run(["git", "checkout", "-b", sandbox_name], cwd=self.repo_path, check=True, capture_output=True)
            
            # 3. Attempt merge
            result = subprocess.run(["git", "merge", source_branch], cwd=self.repo_path, capture_output=True, text=True)
            
            return {
                "sandbox_branch": sandbox_name,
                "merge_success": result.returncode == 0,
                "output": result.stdout + result.stderr
            }
        except subprocess.CalledProcessError as e:
            return {"error": str(e), "merge_success": False}

    def run_sandbox_tests(self, sandbox_branch: str, test_command: List[str]) -> bool:
        """
        Runs a build/test command in the sandbox branch.
        """
        try:
            subprocess.run(["git", "checkout", sandbox_branch], cwd=self.repo_path, check=True, capture_output=True)
            result = subprocess.run(test_command, cwd=self.repo_path, capture_output=True, text=True)
            return result.returncode == 0
        except Exception as e:
            print(f"Test execution error: {e}")
            return False

    def cleanup_sandbox(self, sandbox_branch: str):
        """Deletes the temporary sandbox branch."""
        try:
            subprocess.run(["git", "checkout", "main"], cwd=self.repo_path, check=True, capture_output=True)
            subprocess.run(["git", "branch", "-D", sandbox_branch], cwd=self.repo_path, check=True, capture_output=True)
        except Exception as e:
            print(f"Cleanup error: {e}")

    def execute_panic_revert(self, target_branch: str):
        """
        Instantly reverts the last merge commit on the target branch.
        """
        try:
            # Ensure we are on the target branch
            subprocess.run(["git", "checkout", target_branch], cwd=self.repo_path, check=True, capture_output=True)
            
            # Revert the most recent merge commit
            result = subprocess.run(["git", "revert", "-m", "1", "HEAD"], cwd=self.repo_path, capture_output=True, text=True, check=True)
            
            # Push the revert to remote
            subprocess.run(["git", "push", "origin", target_branch], cwd=self.repo_path, check=True, capture_output=True)
            
            return {"status": "success", "message": "Last merge successfully reverted and pushed."}
        except subprocess.CalledProcessError as e:
            return {"status": "error", "message": f"Revert failed: {e.stderr}"}
