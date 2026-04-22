import unittest
from unittest.mock import MagicMock, patch
from app.services.jira_service import JiraService

class TestJiraIntegration(unittest.TestCase):
    def setUp(self):
        # Mock the config to avoid needing a real file during unit tests
        with patch("os.path.exists", return_value=True), \
             patch("builtins.open", unittest.mock.mock_open(read_data="JIRA_DOMAIN=test.atlassian.net\nJIRA_EMAIL=test@test.com\nJIRA_API_TOKEN=token")):
            self.service = JiraService()

    @patch("requests.get")
    def test_get_issue_success(self, mock_get):
        # Setup mock response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"key": "PROJ-1", "fields": {"summary": "Test Issue"}}
        
        result = self.service.get_issue("PROJ-1")
        self.assertEqual(result["key"], "PROJ-1")
        self.assertEqual(result["fields"]["summary"], "Test Issue")

    @patch("requests.get")
    def test_get_issue_failure(self, mock_get):
        mock_get.return_value.status_code = 404
        with self.assertRaises(Exception):
            self.service.get_issue("INVALID-1")

if __name__ == "__main__":
    unittest.main()
