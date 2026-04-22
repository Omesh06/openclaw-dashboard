import uuid
from datetime import datetime
from typing import List, Dict, Optional

class HITLQueueService:
    """
    Manages the Human-in-the-Loop queue for AI-generated conflict reports.
    """
    def __init__(self):
        # In-memory storage for the prototype. Would be a DB (e.g., PostgreSQL) in production.
        self._queue: List[Dict] = []

    def add_report(self, repo: str, branches: List[str], conflict_details: Dict, priority: str = "medium"):
        report_id = str(uuid.uuid4())
        report = {
            "id": report_id,
            "repo": repo,
            "branches": branches,
            "details": conflict_details,
            "priority": priority,
            "status": "pending",
            "created_at": datetime.now().isoformat()
        }
        self._queue.append(report)
        return report_id

    def get_pending(self) -> List[Dict]:
        return [r for r in self._queue if r["status"] == "pending"]

    def resolve_report(self, report_id: str, resolution: str):
        for r in self._queue:
            if r["id"] == report_id:
                r["status"] = "resolved"
                r["resolution"] = resolution
                return True
        return False

    def clear_queue(self):
        self._queue = []
