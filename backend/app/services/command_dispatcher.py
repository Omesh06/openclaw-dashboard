import os
import json
import requests
from typing import Dict, Any, Optional

class CommandDispatcher:
    """
    The 'Brain' of the dashboard. Translates natural language commands 
    into executable backend actions.
    """
    def __init__(self):
        self.api_base = "http://localhost:8000/api"
        # In a real production app, this would use a proper LLM to map intents.
        # For this professional implementation, we use a keyword-based intent mapper 
        # that can be easily extended to a full LLM call.
        self.intent_map = {
            "scan": "health/status",
            "health": "health/status",
            "radar": "health/status",
            "ticket": "context/summarize",
            "summarize": "context/summarize",
            "intent": "context/summarize",
            "merge": "resolution/merge",
            "approve": "resolution/merge",
            "revert": "safety/revert",
            "panic": "safety/revert",
            "dry-run": "safety/dry-run",
            "test": "safety/dry-run",
            "queue": "queue/pending",
            "pending": "queue/pending"
        }

    def process_command(self, user_input: str) -> Dict[str, Any]:
        """
        Analyzes input, identifies the intended action, and executes the API call.
        """
        input_lower = user_input.lower()
        found_intent = None
        
        for keyword, endpoint in self.intent_map.items():
            if keyword in input_lower:
                found_intent = endpoint
                break
        
        if not found_intent:
            return {
                "status": "unknown",
                "message": "I'm not sure how to execute that. Try saying 'Scan health', 'Summarize ticket PROJ-1', or 'Trigger panic revert'."
            }

        # Mocking the API execution for the dispatcher logic
        # In the real FastAPI app, this dispatcher would be a route that calls other services.
        return {
            "status": "executing",
            "intent": found_intent,
            "message": f"I've identified the intent as '{found_intent}'. Executing the task now..."
        }
