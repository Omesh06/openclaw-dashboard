import unittest
from app.services.hitl_service import HITLQueueService

class TestHITLQueue(unittest.TestCase):
    def setUp(self):
        self.service = HITLQueueService()

    def test_add_and_get_pending(self):
        report_id = self.service.add_report("repo1", ["b1", "b2"], {"conflict": "logic"}, "high")
        pending = self.service.get_pending()
        self.assertEqual(len(pending), 1)
        self.assertEqual(pending[0]["id"], report_id)
        self.assertEqual(pending[0]["priority"], "high")

    def test_resolve_report(self):
        report_id = self.service.add_report("repo1", ["b1", "b2"], {"conflict": "logic"})
        success = self.service.resolve_report(report_id, "Merged manually")
        self.assertTrue(success)
        self.assertEqual(len(self.service.get_pending()), 0)

if __name__ == "__main__":
    unittest.main()
