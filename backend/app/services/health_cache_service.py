import time
import threading
import logging
from typing import Dict, List
from app.services.health_scanner_service import RepoHealthScanner

logger = logging.getLogger("openclaw_dashboard")

class HealthCacheService:
    """
    Background service to cache repository health status, 
    preventing slow Git operations on every dashboard refresh.
    """
    def __init__(self, repo_configs: List[Dict]):
        self.repo_configs = repo_configs
        self.scanner = RepoHealthScanner(repos=[c["path"] for c in repo_configs])
        self._cache = {}
        self._last_updated = 0
        self._lock = threading.Lock()
        self._stop_event = threading.Event()

    def update_cache(self):
        """Performs the actual scan and updates the internal cache."""
        logger.info("Updating repository health cache...")
        try:
            status = self.scanner.get_global_status(self.repo_configs)
            with self._lock:
                self._cache = status
                self._last_updated = time.time()
            logger.info("Health cache updated successfully.")
        except Exception as e:
            logger.error(f"Cache update failed: {e}")

    def get_status(self) -> List[Dict]:
        """Returns the current cached status."""
        with self._lock:
            return self._cache

    def start_background_worker(self, interval: int = 300):
        """Starts a background thread to update cache every 'interval' seconds."""
        def worker():
            while not self._stop_event.is_set():
                self.update_cache()
                time.sleep(interval)

        self.thread = threading.Thread(target=worker, daemon=True)
        self.thread.start()

    def stop_worker(self):
        self._stop_event.set()
