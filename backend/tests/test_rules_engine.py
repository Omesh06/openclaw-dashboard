import unittest
from app.services.rules_engine_service import RulesEngineService

class TestRulesEngine(unittest.TestCase):
    def setUp(self):
        self.service = RulesEngineService(config_path="/tmp/rules.json")

    def test_auto_merge_docs(self):
        self.assertTrue(self.service.should_auto_merge("docs/api.md"))
        self.assertTrue(self.service.should_auto_merge("README.md"))

    def test_critical_path_block(self):
        # Ensure core logic is NOT auto-merged
        self.assertFalse(self.service.should_auto_merge("api/core/engine.py"))

if __name__ == "__main__":
    unittest.main()
