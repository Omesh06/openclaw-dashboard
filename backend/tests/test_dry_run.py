import unittest
from unittest.mock import patch, MagicMock
from app.services.safety_service import SafetyService

class TestSafetyService(unittest.TestCase):
    def setUp(self):
        self.service = SafetyService("/tmp/repo")

    @patch("subprocess.run")
    def test_create_dry_run_success(self, mock_run):
        mock_run.side_effect = [
            MagicMock(stdout="base_id"), # merge-base
            MagicMock(stdout=""), # checkout target
            MagicMock(stdout=""), # checkout -b sandbox
            MagicMock(returncode=0, stdout="Merge made by recursive") # merge
        ]
        res = self.service.create_dry_run_sandbox("feat1", "main")
        self.assertTrue(res["merge_success"])
        self.assertIn("sandbox-dryrun-", res["sandbox_branch"])

    @patch("subprocess.run")
    def test_panic_revert(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout="Reverted")
        res = self.service.execute_panic_revert("main")
        self.assertEqual(res["status"], "success")

if __name__ == "__main__":
    unittest.main()
