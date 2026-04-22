import unittest
from unittest.mock import patch, MagicMock
from app.services.health_scanner_service import RepoHealthScanner

class TestHealthScanner(unittest.TestCase):
    def setUp(self):
        self.scanner = RepoHealthScanner(repos=["/tmp/repo"])

    @patch("subprocess.run")
    def test_get_modified_files_overlap(self, mock_run):
        # Mock merge-base
        mock_run.side_effect = [
            MagicMock(stdout="base_commit_id"), # merge-base
            MagicMock(stdout="file1.py\nfile2.py"), # branch_a diff
            MagicMock(stdout="file2.py\nfile3.py"), # branch_b diff
        ]
        
        overlaps = self.scanner.get_modified_files("/tmp/repo", "feat1", "feat2")
        self.assertEqual(overlaps, ["file2.py"])

    def test_calculate_health_green(self):
        # Mock get_modified_files to return empty list (no overlap)
        with patch.object(RepoHealthScanner, 'get_modified_files', return_value=[]):
            res = self.scanner.calculate_health("/tmp/repo", ["feat1", "feat2"])
            self.assertEqual(res["status"], "Green")
            self.assertEqual(res["health_score"], 100)

    def test_calculate_health_red(self):
        # Mock get_modified_files to return many overlapping files
        with patch.object(RepoHealthScanner, 'get_modified_files', return_value=["f1.py", "f2.py", "f3.py", "f4.py"]):
            res = self.scanner.calculate_health("/tmp/repo", ["feat1", "feat2"])
            self.assertEqual(res["status"], "Red")
            self.assertEqual(res["health_score"], 30)

if __name__ == "__main__":
    unittest.main()
