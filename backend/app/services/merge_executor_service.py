import subprocess
import os

class MergeExecutorService:
    def __init__(self, repo_path: str):
        self.repo_path = repo_path

    def finalize_merge(self, source_branch: str, target_branch: str):
        """
        Executes the final merge of the approved proposal into the target branch (SIT/UAT).
        """
        try:
            # 1. Checkout target
            subprocess.run(["git", "checkout", target_branch], cwd=self.repo_path, check=True, capture_output=True)
            
            # 2. Merge the source (the approved proposal branch)
            # Use --no-ff to ensure a merge commit is created for auditability
            subprocess.run(["git", "merge", "--no-ff", source_branch, "-m", f"AI-Assisted merge of {source_branch} into {target_branch}"], 
                           cwd=self.repo_path, check=True, capture_output=True)
            
            # 3. Push to remote
            subprocess.run(["git", "push", "origin", target_branch], cwd=self.repo_path, check=True, capture_output=True)
            
            return {"status": "success", "message": f"Successfully merged {source_branch} into {target_branch}"}
        except subprocess.CalledProcessError as e:
            return {"status": "error", "message": f"Merge failed: {e.stderr.decode() if e.stderr else str(e)}"}

    def apply_developer_tweak(self, branch_name: str, file_path: str, new_content: str):
        """
        Allows the developer to manually edit a file in the proposal branch.
        """
        try:
            # Write content to file
            full_path = os.path.join(self.repo_path, file_path)
            with open(full_path, "w") as f:
                f.write(new_content)
            
            # Commit the tweak
            subprocess.run(["git", "checkout", branch_name], cwd=self.repo_path, check=True, capture_output=True)
            subprocess.run(["git", "add", file_path], cwd=self.repo_path, check=True, capture_output=True)
            subprocess.run(["git", "commit", "-m", f"Developer tweak to {file_path}"], cwd=self.repo_path, check=True, capture_output=True)
            
            return {"status": "success", "message": "Tweak applied and committed."}
        except Exception as e:
            return {"status": "error", "message": str(e)}
