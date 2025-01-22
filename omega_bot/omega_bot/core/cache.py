# omega_bot/core/cache.py
from typing import Any, Optional
from datetime import datetime, timedelta
import asyncio
from dataclasses import dataclass
from ..utils.logger import get_logger

logger = get_logger(__name__)

@dataclass
class CacheConfig:
    max_size: int = 100
    ttl: int = 3600  # Time to live in seconds
    cleanup_interval: int = 300  # Cleanup interval in seconds

class LRUCache:
    def __init__(self, config: Optional[CacheConfig] = None):
        self.config = config or CacheConfig()
        self.cache: Dict[str, Any] = {}
        self.timestamps: Dict[str, datetime] = {}
        self.access_count: Dict[str, int] = {}
        self._lock = asyncio.Lock()
        self._start_cleanup_task()
        
    def _start_cleanup_task(self):
        """Start periodic cache cleanup task."""
        asyncio.create_task(self._periodic_cleanup())
        
    async def _periodic_cleanup(self):
        """Periodically clean up expired cache entries."""
        while True:
            await asyncio.sleep(self.config.cleanup_interval)
            await self.cleanup()
            
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        async with self._lock:
            if key not in self.cache:
                return None
                
            if self._is_expired(key):
                await self.remove(key)
                return None
                
            self.access_count[key] += 1
            self.timestamps[key] = datetime.utcnow()
            return self.cache[key]
            
    async def set(self, key: str, value: Any) -> None:
        """Set value in cache."""
        async with self._lock:
            if len(self.cache) >= self.config.max_size:
                await self._evict_lru()
                
            self.cache[key] = value
            self.timestamps[key] = datetime.utcnow()
            self.access_count[key] = 0
            
    async def remove(self, key: str) -> None:
        """Remove item from cache."""
        async with self._lock:
            if key in self.cache:
                del self.cache[key]
                del self.timestamps[key]
                del self.access_count[key]
                
    async def cleanup(self) -> None:
        """Clean up expired cache entries."""
        async with self._lock:
            now = datetime.utcnow()
            expired_keys = [
                key for key, timestamp in self.timestamps.items()
                if (now - timestamp).total_seconds() > self.config.ttl
            ]
            
            for key in expired_keys:
                await self.remove(key)
                
    def _is_expired(self, key: str) -> bool:
        """Check if cache entry is expired."""
        age = datetime.utcnow() - self.timestamps[key]
        return age.total_seconds() > self.config.ttl
        
    async def _evict_lru(self) -> None:
        """Evict least recently used item from cache."""
        if not self.cache:
            return
            
        # Find least recently used item
        lru_key = min(
            self.timestamps.keys(),
            key=lambda k: (self.access_count[k], self.timestamps[k])
        )
        await self.remove(lru_key)
