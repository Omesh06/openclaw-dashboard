import subprocess
import os
from typing import Dict, List

class DiffService:
    def __init__(self, repo_path: str):
        self.repo_path = repo_path

    def get_3way_diff(self, branch_a: str, branch_b: str, proposal_branch: str) -> Dict:
        """
        Generates content for the 3-way diff viewer and calculates confidence.
        """
        try:
            # ... (existing diff logic) ...
            merge_base = subprocess.run(
                ["git", "merge-base", branch_a, branch_b],
                cwd=self.repo_path, capture_output=True, text=True, check=True
            ).stdout.strip()

            diff_a = subprocess.run(["git", "diff", f"{merge_base}..{branch_a}"], cwd=self.repo_path, capture_output=True, text=True, check=True).stdout
            diff_b = subprocess.run(["git", "diff", f"{merge_base}..{branch_b}"], cwd=self.repo_path, capture_output=True, text=True, check=True).stdout
            diff_proposal = subprocess.run(["git", "diff", f"{merge_base}..{proposal_branch}"], cwd=self.repo_path, capture_output=True, text=True, check=True).stdout

            # CONFIDENCE SCORE LOGIC
            # Higher confidence if the proposal diff is small compared to the sum of branch diffs.
            # Or if there are no conflicting lines (simple additive merge).
            lines_a = len(diff_a.splitlines())
            lines_b = len(diff_b.splitlines())
            lines_p = len(diff_proposal.splitlines())
            
            # Simple heuristic: Confidence is high if the proposal is a clean combination.
            confidence = 100 - (abs(lines_p - (lines_a + lines_b)) // 10)
            confidence = max(10, min(98, confidence)) # Clamp between 10% and 98%

            return {
                "base_commit": merge_base,
                "branch_a_diff": diff_a,
                "branch_b_diff": diff_b,
                "proposal_diff": diff_proposal,
                "confidence_score": f"{confidence}%"
            }
        except Exception as e:
            raise Exception(f"Diff generation failed: {str(e)}")

    def get_file_content(self, branch: str, file_path: str) -> str:
        """Fetch the raw content of a file from a specific branch."""
        try:
            return subprocess.run(
                ["git", "show", f"{branch}:{file_path}"],
                cwd=self.repo_path, capture_output=True, text=True, check=True
            ).stdout
        except subprocess.CalledProcessError:
            return ""
