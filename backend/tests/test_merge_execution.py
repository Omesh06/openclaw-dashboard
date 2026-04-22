import unittest
from unittest.mock import patch, MagicMock
from app.services.merge_executor_service import MergeExecutorService

class TestMergeExecution(unittest.TestCase):
    def setUp(self):
        self.service = MergeExecutorService("/tmp/repo")

    @patch("subprocess.run")
    def test_finalize_merge_success(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0)
        res = self.service.finalize_merge("feat1", "main")
        self.assertEqual(res["status"], "success")

    @patch("subprocess.run")
    def test_apply_tweak_success(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0)
        # Mock open to avoid file system errors
        with patch("builtins.open", unittest.mock.mock_open()):
            res = self.service.apply_developer_tweak("proposal", "file.py", "print(1)")
            self.assertEqual(res["status"], "success")

if __name__ == "__main__":
    unittest.main()
