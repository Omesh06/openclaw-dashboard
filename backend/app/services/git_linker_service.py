import re
import subprocess

class GitLinkerService:
    def __init__(self, repo_path):
        self.repo_path = repo_path

    def get_commits_for_branch(self, branch_name):
        """Fetch commit logs for a specific branch."""
        try:
            result = subprocess.run(
                ["git", "log", branch_name, "--pretty=format:%s"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.split("\n")
        except subprocess.CalledProcessError as e:
            raise Exception(f"Git error: {e.stderr}")

    def extract_jira_tickets(self, text):
        """
        Extract Jira ticket IDs (e.g., PROJ-123) from text.
        Regex looks for uppercase letters followed by a hyphen and numbers.
        """
        pattern = r'([A-Z][A-Z0-9]+-\d+)'
        return list(set(re.findall(pattern, text)))

    def find_tickets_for_branch(self, branch_name):
        """
        Scan all commits on a branch and return a unique list of linked Jira tickets.
        """
        commits = self.get_commits_for_branch(branch_name)
        all_tickets = []
        for commit in commits:
            all_tickets.extend(self.extract_jira_tickets(commit))
        
        return list(set(all_tickets))
