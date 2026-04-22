import subprocess
import os
from datetime import datetime
from app.core.database import get_db_connection

class AuditService:
    def log_action(self, action: str, repo: str, branch: str, user: str, status: str, details: str):
        """Records an action in the audit log for metrics and compliance."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO audit_log (action, repo, branch, user, timestamp, status, details) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (action, repo, branch, user, datetime.now().isoformat(), status, details)
        )
        conn.commit()
        conn.close()

    def get_metrics(self):
        """Fetches aggregated metrics for the dashboard."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Total successful merges
        cursor.execute("SELECT COUNT(*) FROM audit_log WHERE action = 'merge' AND status = 'success'")
        success_count = cursor.fetchone()[0]
        
        # Total rollbacks
        cursor.execute("SELECT COUNT(*) FROM audit_log WHERE action = 'revert'")
        revert_count = cursor.fetchone()[0]
        
        conn.close()
        return {
            "total_successful_merges": success_count,
            "total_rollbacks": revert_count,
            "success_rate": (success_count / (success_count + revert_count * 2)) * 100 if (success_count + revert_count) > 0 else 100
        }
