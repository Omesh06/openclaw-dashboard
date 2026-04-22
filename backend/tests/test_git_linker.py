import unittest
from app.services.git_linker_service import GitLinkerService

class TestGitLinker(unittest.TestCase):
    def test_extract_tickets(self):
        service = GitLinkerService(repo_path="/tmp")
        text = "Fixing issue PROJ-123 and updating PROJ-456"
        tickets = service.extract_jira_tickets(text)
        self.assertIn("PROJ-123", tickets)
        self.assertIn("PROJ-456", tickets)
        self.assertEqual(len(tickets), 2)

    def test_extract_no_tickets(self):
        service = GitLinkerService(repo_path="/tmp")
        text = "Just a normal commit message"
        tickets = service.extract_jira_tickets(text)
        self.assertEqual(len(tickets), 0)

if __name__ == "__main__":
    unittest.main()
