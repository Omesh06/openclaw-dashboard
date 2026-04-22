import unittest
from app.services.intent_service import IntentTranslationService

class TestIntentSummary(unittest.TestCase):
    def setUp(self):
        self.service = IntentTranslationService(llm_provider="mock")

    def test_summarize_intent_mock(self):
        context = {
            "summary": "Fix Login Bug",
            "description": "Users cannot login with special characters in password.",
            "comments": ["Confirmed by QA", "Fixed in dev"]
        }
        result = self.service.summarize_intent(context)
        self.assertIn("[MOCK AI]", result)
        self.assertIn("fix login bug", result.lower())

if __name__ == "__main__":
    unittest.main()
