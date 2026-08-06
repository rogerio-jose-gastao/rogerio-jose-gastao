"""
Persistent caching engine to safeguard API calls against rate limits and network errors.
"""

from __future__ import annotations

import json
import logging
import time
from pathlib import Path
from typing import Any, Optional

from scripts.core.utils import get_project_root

logger = logging.getLogger("readme_engine")


class CacheEngine:
    """Manages file-backed JSON caching for external API responses."""

    def __init__(self, cache_file: str = "data/cache.json", default_ttl_seconds: int = 3600) -> None:
        self.cache_path = get_project_root() / cache_file
        self.default_ttl = default_ttl_seconds
        self._ensure_cache_dir()

    def _ensure_cache_dir(self) -> None:
        """Create parent directory for cache if missing."""
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.cache_path.exists():
            self._write_cache_file({})

    def _read_cache_file(self) -> dict[str, Any]:
        """Read cache payload from disk safely."""
        try:
            with open(self.cache_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return {}

    def _write_cache_file(self, data: dict[str, Any]) -> None:
        """Write cache payload to disk."""
        try:
            with open(self.cache_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except OSError as exc:
            logger.warning("Could not save cache to %s: %s", self.cache_path, exc)

    def get(self, key: str) -> Optional[Any]:
        """Retrieve value if unexpired, else return None."""
        data = self._read_cache_file()
        if key not in data:
            return None

        entry = data[key]
        timestamp = entry.get("timestamp", 0)
        ttl = entry.get("ttl", self.default_ttl)

        if time.time() - timestamp > ttl:
            logger.debug("Cache entry for key '%s' has expired.", key)
            return None

        return entry.get("value")

    def get_stale_or_default(self, key: str, default: Any = None) -> Any:
        """Retrieve cached value regardless of expiry (for emergency offline fallback)."""
        data = self._read_cache_file()
        if key in data:
            return data[key].get("value")
        return default

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Store value with timestamp and TTL."""
        data = self._read_cache_file()
        data[key] = {
            "timestamp": time.time(),
            "ttl": ttl if ttl is not None else self.default_ttl,
            "value": value,
        }
        self._write_cache_file(data)
