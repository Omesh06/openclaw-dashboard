import json
import os
from typing import Dict

class RulesEngineService:
    def __init__(self, config_path: str = "backend/app/core/merge_rules.json"):
        self.config_path = config_path
        self.rules = self._load_rules()

    def _load_rules(self) -> Dict:
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as f:
                return json.load(f)
        # Default rules if config doesn't exist
        return {
            "auto_merge_whitespace": True,
            "auto_merge_docs": True,
            "require_approval_for_logic": True,
            "critical_paths": ["api/core", "backend/app/core"]
        }

    def should_auto_merge(self, file_path: str) -> bool:
        """
        Determine if a file change can be auto-merged based on the rules engine.
        """
        # Rule 1: Whitespace only is handled by git, but we can define logical rules here
        if self.rules.get("auto_merge_docs") and ("docs/" in file_path or file_path.endswith(".md")):
            return True
            
        # Rule 2: Check for critical paths
        for path in self.rules.get("critical_paths", []):
            if path in file_path:
                return False
                
        return not self.rules.get("require_approval_for_logic", True)

    def update_rule(self, rule_name: str, value: any):
        self.rules[rule_name] = value
        with open(self.config_path, "w") as f:
            json.dump(self.rules, f, indent=4)
