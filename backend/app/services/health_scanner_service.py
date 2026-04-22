import subprocess
import os
from typing import List, Dict

class RepoHealthScanner:
    def __init__(self, repos: List[str]):
        """
        :param repos: List of absolute paths to the repositories to scan.
        """
        self.repos = repos

    def get_modified_files(self, repo_path: str, branch_a: str, branch_b: str) -> List[str]:
        """
        Find files that have changed in both branch_a and branch_b relative to a common ancestor.
        """
        try:
            # Find common ancestor
            merge_base = subprocess.run(
                ["git", "merge-base", branch_a, branch_b],
                cwd=repo_path, capture_output=True, text=True, check=True
            ).stdout.strip()

            # Files changed in branch_a since merge_base
            files_a = subprocess.run(
                ["git", "diff", "--name-only", f"{merge_base}..{branch_a}"],
                cwd=repo_path, capture_output=True, text=True, check=True
            ).stdout.splitlines()

            # Files changed in branch_b since merge_base
            files_b = subprocess.run(
                ["git", "diff", "--name-only", f"{merge_base}..{branch_b}"],
                cwd=repo_path, capture_output=True, text=True, check=True
            ).stdout.splitlines()

            # Return intersection (the overlapping files)
            return list(set(files_a) & set(files_b))
        except Exception as e:
            print(f"Error scanning repo {repo_path}: {e}")
            return []

    def calculate_health(self, repo_path: str, feature_branches: List[str], target_branch: str = "main") -> Dict:
        """
        Analyzes conflicts between multiple feature branches.
        - Green: No overlaps.
        - Yellow: Few overlaps, mostly in non-critical files (e.g., docs, tests).
        - Red: Significant overlaps in core logic files.
        """
        overlaps = []
        all_overlapping_files = set()

        # Compare every pair of branches
        for i in range(len(feature_branches)):
            for j in range(i + 1, len(feature_branches)):
                b1, b2 = feature_branches[i], feature_branches[j]
                conflicting_files = self.get_modified_files(repo_path, b1, b2)
                if conflicting_files:
                    overlaps.append({
                        "branches": [b1, b2],
                        "files": conflicting_files
                    })
                    all_overlapping_files.update(conflicting_files)

        if not overlaps:
            status = "Green"
            score = 100
        elif len(all_overlapping_files) < 3:
            status = "Yellow"
            score = 60
        else:
            status = "Red"
            score = 30

        return {
            "repo": os.path.basename(repo_path),
            "status": status,
            "health_score": score,
            "overlaps": overlaps,
            "total_conflicts": len(overlaps)
        }

    def get_global_status(self, repo_configs: List[Dict]) -> List[Dict]:
        """
        repo_configs should be: [{"path": "/path/to/repo", "branches": ["feat1", "feat2"], "target": "main"}]
        """
        results = []
        for config in repo_configs:
            res = self.calculate_health(
                config["path"], 
                config["branches"], 
                config.get("target", "main")
            )
            results.append(res)
        return results
