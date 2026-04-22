import subprocess
import os
from typing import Dict, List

class DiffService:
    def __init__(self, repo_path: str):
        self.repo_path = repo_path

    def get_3way_diff(self, branch_a: str, branch_b: str, proposal_branch: str) -> Dict:
        """
        Generates content for the 3-way diff viewer.
        - Branch A: Changes from the common ancestor to branch_a.
        - Branch B: Changes from the common ancestor to branch_b.
        - Proposal: The final merged state proposed by the AI.
        """
        try:
            # 1. Find common ancestor
            merge_base = subprocess.run(
                ["git", "merge-base", branch_a, branch_b],
                cwd=self.repo_path, capture_output=True, text=True, check=True
            ).stdout.strip()

            # 2. Get diff for Branch A
            diff_a = subprocess.run(
                ["git", "diff", f"{merge_base}..{branch_a}"],
                cwd=self.repo_path, capture_output=True, text=True, check=True
            ).stdout

            # 3. Get diff for Branch B
            diff_b = subprocess.run(
                ["git", "diff", f"{merge_base}..{branch_b}"],
                cwd=self.repo_path, capture_output=True, text=True, check=True
            ).stdout

            # 4. Get the proposed merged state (as a full file or a diff)
            # For the UI, we often need the final state of the files.
            # Here we provide the diff of the proposal relative to the base.
            diff_proposal = subprocess.run(
                ["git", "diff", f"{merge_base}..{proposal_branch}"],
                cwd=self.repo_path, capture_output=True, text=True, check=True
            ).stdout

            return {
                "base_commit": merge_base,
                "branch_a_diff": diff_a,
                "branch_b_diff": diff_b,
                "proposal_diff": diff_proposal
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
