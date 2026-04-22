import uuid
import json
from datetime import datetime
from typing import List, Dict, Optional
from app.core.database import get_db_connection

class HITLQueueService:
    """
    Manages the Human-in-the-Loop queue using SQLite persistence.
    """
    def add_report(self, repo: str, branches: List[str], conflict_details: Dict, priority: str = "medium"):
        report_id = str(uuid.uuid4())
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO hitl_queue (id, repo, branches, details, priority, status, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (report_id, repo, json.dumps(branches), json.dumps(conflict_details), priority, "pending", datetime.now().isoformat())
        )
        conn.commit()
        conn.close()
        return report_id

    def get_pending(self) -> List[Dict]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM hitl_queue WHERE status = 'pending'")
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]

    def resolve_report(self, report_id: str, resolution: str):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE hitl_queue SET status = 'resolved', resolution = ? WHERE id = ?", (resolution, report_id))
        conn.commit()
        changed = cursor.rowcount > 0
        conn.close()
        return changed

    def clear_queue(self):
        conn = get_db_connection()
        conn.execute("DELETE FROM hitl_queue")
        conn.commit()
        conn.close()
