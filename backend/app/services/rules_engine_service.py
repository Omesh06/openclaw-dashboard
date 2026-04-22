import json
import os
from typing import Dict
from app.core.database import get_db_connection

class RulesEngineService:
    def __init__(self, config_path: str = "backend/app/core/merge_rules.json"):
        # Now we use the DB as primary, and the JSON as a fallback/backup
        self.config_path = config_path

    def _load_rules(self) -> Dict:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT rule_name, rule_value FROM merge_rules")
        rows = cursor.fetchall()
        conn.close()
        
        if rows:
            return {row["rule_name"]: row["rule_value"] == "True" for row in rows}
        
        # Fallback to defaults if DB is empty
        return {
            "auto_merge_whitespace": True,
            "auto_merge_docs": True,
            "require_approval_for_logic": True,
            "critical_paths": "['api/core', 'backend/app/core']"
        }

    def should_auto_merge(self, file_path: str) -> bool:
        rules = self._load_rules()
        if rules.get("auto_merge_docs") and ("docs/" in file_path or file_path.endswith(".md")):
            return True
            
        critical_paths = eval(rules.get("critical_paths", "[]"))
        for path in critical_paths:
            if path in file_path:
                return False
                
        return not rules.get("require_approval_for_logic", True)

    def update_rule(self, rule_name: str, value: bool):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO merge_rules (rule_name, rule_value) VALUES (?, ?)",
            (rule_name, str(value))
        )
        conn.commit()
        conn.close()
