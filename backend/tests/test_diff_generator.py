import unittest
from unittest.mock import patch, MagicMock
from app.services.diff_service import DiffService

class TestDiffGenerator(unittest.TestCase):
    def setUp(self):
        self.service = DiffService("/tmp/repo")

    @patch("subprocess.run")
    def test_get_3way_diff_success(self, mock_run):
        # Mock merge-base, diff_a, diff_b, diff_proposal
        mock_run.side_effect = [
            MagicMock(stdout="base_id"),
            MagicMock(stdout="diff_a_content"),
            MagicMock(stdout="diff_b_content"),
            MagicMock(stdout="proposal_content"),
        ]
        
        res = self.service.get_3way_diff("feat1", "feat2", "proposal")
        self.assertEqual(res["branch_a_diff"], "diff_a_content")
        self.assertEqual(res["branch_b_diff"], "diff_b_content")
        self.assertEqual(res["proposal_diff"], "proposal_content")

if __name__ == "__main__":
    unittest.main()
