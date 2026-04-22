import os
import requests
from requests.auth import HTTPBasicAuth

class JiraService:
    def __init__(self, config_path=None):
        if config_path is None:
            config_path = os.path.expanduser("~/.openclaw/workspace/.jira_config")
        
        self.config = self._load_config(config_path)
        self.domain = self.config.get("JIRA_DOMAIN", "").replace("https://", "").replace("/", "")
        self.email = self.config.get("JIRA_EMAIL")
        self.token = self.config.get("JIRA_API_TOKEN")
        
        if not all([self.domain, self.email, self.token]):
            raise ValueError("Missing Jira configuration in .jira_config")
            
        self.base_url = f"https://{self.domain}/rest/api/3"
        self.auth = HTTPBasicAuth(self.email, self.token)
        self.headers = {"Accept": "application/json", "Content-Type": "application/json"}

    def _load_config(self, path):
        config = {}
        if not os.path.exists(path):
            raise FileNotFoundError(f"Config file not found at {path}")
        with open(path, "r") as f:
            for line in f:
                if "=" in line:
                    k, v = line.strip().split("=", 1)
                    config[k] = v
        return config

    def get_issue(self, issue_id):
        """Fetch a single Jira issue's details."""
        url = f"{self.base_url}/issue/{issue_id}"
        resp = requests.get(url, auth=self.auth, headers=self.headers)
        if resp.status_code == 200:
            return resp.json()
        else:
            raise Exception(f"Error fetching issue {issue_id}: {resp.status_code} - {resp.text}")

    def search_issues(self, jql, max_results=50):
        """Search issues using JQL."""
        url = f"{self.base_url}/search"
        params = {
            "jql": jql,
            "maxResults": max_results,
            "startAt": 0
        }
        resp = requests.get(url, auth=self.auth, headers=self.headers, params=params)
        if resp.status_code == 200:
            return resp.json().get("issues", [])
        else:
            raise Exception(f"Error searching issues: {resp.status_code} - {resp.text}")

    def get_issue_context(self, issue_id):
        """
        Specifically extract User Story, Acceptance Criteria, and comments 
        to feed into the AI Intent Translation.
        """
        issue = self.get_issue(issue_id)
        fields = issue.get("fields", {})
        
        # In Jira, description often contains the story/AC
        description = fields.get("description", "")
        if isinstance(description, dict):
            # Extract text from ADF (Atlassian Document Format)
            text_parts = []
            def extract_text(node):
                if node.get("type") == "text":
                    text_parts.append(node.get("text", ""))
                for child in node.get("content", []):
                    extract_text(child)
            
            extract_text(description)
            description = " ".join(text_parts)

        # Fetch comments
        comments_url = f"{self.base_url}/issue/{issue_id}/comment"
        c_resp = requests.get(comments_url, auth=self.auth, headers=self.headers)
        comments = []
        if c_resp.status_code == 200:
            for c in c_resp.json().get("comments", []):
                body = c.get("body", "")
                if isinstance(body, dict):
                    text_parts = []
                    def extract_text_comment(node):
                        if node.get("type") == "text":
                            text_parts.append(node.get("text", ""))
                        for child in node.get("content", []):
                            extract_text_comment(child)
                    extract_text_comment(body)
                    body = " ".join(text_parts)
                comments.append(body)

        return {
            "issue_id": issue_id,
            "summary": fields.get("summary"),
            "description": description,
            "comments": comments
        }
