# omega_bot/utils/monitoring.py
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import asyncio
import psutil
import json
import aiofiles
from pathlib import Path
from prometheus_client import (
    Counter, Gauge, Histogram, start_http_server,
    CollectorRegistry, multiprocess
)
from .logger import get_logger
from ..utils.error_handler import BotError

logger = get_logger(__name__)

class MetricsCollector:
    """Comprehensive metrics collection and monitoring system."""
    
    def __init__(
        self,
        metrics_dir: str = "metrics",
        export_interval: int = 60,
        retention_days: int = 7,
        enable_prometheus: bool = True,
        prometheus_port: int = 9090
    ):
        self.metrics_dir = Path(metrics_dir)
        self.metrics_dir.mkdir(parents=True, exist_ok=True)
        self.export_interval = export_interval
        self.retention_days = retention_days
        self.enable_prometheus = enable_prometheus
        self.prometheus_port = prometheus_port
        
        # Initialize metrics storage
        self.metrics: Dict[str, Any] = {
            "requests": {
                "total": 0,
                "success": 0,
                "failed": 0,
                "by_command": {},
                "by_user": {}
            },
            "generation_times": [],
            "cache": {
                "hits": 0,
                "misses": 0
            },
            "errors": {},
            "rate_limits": {
                "total": 0,
                "by_user": {}
            },
            "resource_usage": {
                "cpu": [],
                "memory": [],
                "disk": [],
                "gpu": [] if self._has_gpu() else None
            },
            "model_usage": {},
            "daily_stats": {}
        }
        
        # Initialize Prometheus metrics if enabled
        if self.enable_prometheus:
            self._init_prometheus_metrics()
            
    def _init_prometheus_metrics(self) -> None:
        """Initialize Prometheus metrics collectors."""
        self.registry = CollectorRegistry()
        
        # Counter metrics
        self.request_counter = Counter(
            'bot_requests_total',
            'Total number of requests',
            ['command', 'status'],
            registry=self.registry
        )
        
        self.error_counter = Counter(
            'bot_errors_total',
            'Total number of errors',
            ['type'],
            registry=self.registry
        )
        
        # Gauge metrics
        self.active_users_gauge = Gauge(
            'bot_active_users',
            'Number of active users',
            registry=self.registry
        )
        
        self.resource_usage_gauge = Gauge(
            'bot_resource_usage',
            'System resource usage',
            ['resource_type'],
            registry=self.registry
        )
        
        # Histogram metrics
        self.generation_time_histogram = Histogram(
            'bot_generation_time_seconds',
            'Image generation time in seconds',
            buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0],
            registry=self.registry
        )
        
        # Start Prometheus HTTP server
        start_http_server(self.prometheus_port, registry=self.registry)
        
    async def start_collection(self) -> None:
        """Start periodic metrics collection and maintenance tasks."""
        await asyncio.gather(
            self._collect_system_metrics(),
            self._export_metrics(),
            self._cleanup_old_metrics()
        )
        
    async def _collect_system_metrics(self) -> None:
        """Collect system resource usage metrics periodically."""
        while True:
            try:
                # CPU usage
                cpu_percent = psutil.cpu_percent(interval=1)
                self.metrics["resource_usage"]["cpu"].append({
                    "timestamp": datetime.utcnow().isoformat(),
                    "value": cpu_percent
                })
                
                # Memory usage
                memory = psutil.virtual_memory()
                self.metrics["resource_usage"]["memory"].append({
                    "timestamp": datetime.utcnow().isoformat(),
                    "value": memory.percent
                })
                
                # Disk usage
                disk = psutil.disk_usage('/')
                self.metrics["resource_usage"]["disk"].append({
                    "timestamp": datetime.utcnow().isoformat(),
                    "value": disk.percent
                })
                
                # GPU metrics if available
                if self._has_gpu():
                    gpu_usage = self._get_gpu_usage()
                    self.metrics["resource_usage"]["gpu"].append({
                        "timestamp": datetime.utcnow().isoformat(),
                        "value": gpu_usage
                    })
                    
                # Update Prometheus metrics
                if self.enable_prometheus:
                    self.resource_usage_gauge.labels('cpu').set(cpu_percent)
                    self.resource_usage_gauge.labels('memory').set(memory.percent)
                    self.resource_usage_gauge.labels('disk').set(disk.percent)
                    
            except Exception as e:
                logger.error(f"Error collecting system metrics: {str(e)}")
                
            await asyncio.sleep(60)  # Collect every minute
            
    async def record_request(
        self,
        command: str,
        user_id: int,
        success: bool = True
    ) -> None:
        """Record a bot request."""
        self.metrics["requests"]["total"] += 1
        self.metrics["requests"]["success"] += 1 if success else 0
        self.metrics["requests"]["failed"] += 0 if success else 1
        
        # Update command stats
        if command not in self.metrics["requests"]["by_command"]:
            self.metrics["requests"]["by_command"][command] = {
                "total": 0,
                "success": 0,
                "failed": 0
            }
        self.metrics["requests"]["by_command"][command]["total"] += 1
        self.metrics["requests"]["by_command"][command]["success"] += 1 if success else 0
        self.metrics["requests"]["by_command"][command]["failed"] += 0 if success else 1
        
        # Update user stats
        user_id_str = str(user_id)
        if user_id_str not in self.metrics["requests"]["by_user"]:
            self.metrics["requests"]["by_user"][user_id_str] = {
                "total": 0,
                "success": 0,
                "failed": 0
            }
        self.metrics["requests"]["by_user"][user_id_str]["total"] += 1
        self.metrics["requests"]["by_user"][user_id_str]["success"] += 1 if success else 0
        self.metrics["requests"]["by_user"][user_id_str]["failed"] += 0 if success else 1
        
        # Update Prometheus metrics
        if self.enable_prometheus:
            status = "success" if success else "failed"
            self.request_counter.labels(command=command, status=status).inc()
            
    async def record_generation(
        self,
        user_id: int,
        prompt: str,
        generation_time: float,
        success: bool,
        model_id: Optional[str] = None
    ) -> None:
        """Record image generation metrics."""
        self.metrics["generation_times"].append({
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": user_id,
            "generation_time": generation_time,
            "success": success
        })
        
        if model_id:
            if model_id not in self.metrics["model_usage"]:
                self.metrics["model_usage"][model_id] = {
                    "total": 0,
                    "success": 0,
                    "failed": 0,
                    "avg_generation_time": 0
                }
            
            model_stats = self.metrics["model_usage"][model_id]
            model_stats["total"] += 1
            model_stats["success"] += 1 if success else 0
            model_stats["failed"] += 0 if success else 1
            
            # Update average generation time
            prev_avg = model_stats["avg_generation_time"]
            model_stats["avg_generation_time"] = (
                (prev_avg * (model_stats["total"] - 1) + generation_time) /
                model_stats["total"]
            )
            
        # Update Prometheus metrics
        if self.enable_prometheus and success:
            self.generation_time_histogram.observe(generation_time)
            
    async def record_error(self, error: str, error_type: Optional[str] = None) -> None:
        """Record an error occurrence."""
        error_type = error_type or "unknown"
        if error_type not in self.metrics["errors"]:
            self.metrics["errors"][error_type] = []
            
        self.metrics["errors"][error_type].append({
            "timestamp": datetime.utcnow().isoformat(),
            "error": error
        })
        
        # Update Prometheus metrics
        if self.enable_prometheus:
            self.error_counter.labels(type=error_type).inc()
            
    async def record_cache_hit(self) -> None:
        """Record a cache hit."""
        self.metrics["cache"]["hits"] += 1
        
    async def record_cache_miss(self) -> None:
        """Record a cache miss."""
        self.metrics["cache"]["misses"] += 1
        
    async def get_statistics(self) -> Dict[str, Any]:
        """Get current statistics summary."""
        total_requests = self.metrics["requests"]["total"]
        successful_requests = self.metrics["requests"]["success"]
        
        return {
            "total_requests": total_requests,
            "success_rate": (successful_requests / total_requests * 100) if total_requests > 0 else 0,
            "avg_generation_time": self._calculate_avg_generation_time(),
            "cache_hit_rate": self._calculate_cache_hit_rate(),
            "active_models": len(self.metrics["model_usage"]),
            "cpu_usage": self._get_latest_resource_usage("cpu"),
            "memory_usage": self._get_latest_resource_usage("memory"),
            "disk_usage": self._get_latest_resource_usage("disk"),
            "error_rate": self._calculate_error_rate()
        }
        
    async def _export_metrics(self) -> None:
        """Export metrics to file periodically."""
        while True:
            try:
                current_time = datetime.utcnow()
                filename = self.metrics_dir / f"metrics_{current_time.strftime('%Y%m%d')}.json"
                
                async with aiofiles.open(filename, 'w') as f:
                    await f.write(json.dumps(self.metrics, indent=2))
                    
            except Exception as e:
                logger.error(f"Error exporting metrics: {str(e)}")
                
            await asyncio.sleep(self.export_interval)
            
    async def _cleanup_old_metrics(self) -> None:
        """Clean up old metrics files."""
        while True:
            try:
                current_time = datetime.utcnow()
                retention_limit = current_time - timedelta(days=self.retention_days)
                
                for metrics_file in self.metrics_dir.glob("metrics_*.json"):
                    file_date = datetime.strptime(
                        metrics_file.stem.split('_')[1],
                        '%Y%m%d'
                    )
                    if file_date < retention_limit:
                        metrics_file.unlink()
                        
            except Exception as e:
                logger.error(f"Error cleaning up old metrics: {str(e)}")
                
            await asyncio.sleep(86400)  # Run daily
            
    def _calculate_avg_generation_time(self) -> float:
        """Calculate average generation time."""
        if not self.metrics["generation_times"]:
            return 0.0
        return sum(
            g["generation_time"] for g in self.metrics["generation_times"]
        ) / len(self.metrics["generation_times"])
        
    def _calculate_cache_hit_rate(self) -> float:
        """Calculate cache hit rate."""
        total = self.metrics["cache"]["hits"] + self.metrics["cache"]["misses"]
        if total == 0:
            return 0.0
        return (self.metrics["cache"]["hits"] / total) * 100
        
    def _calculate_error_rate(self) -> float:
        """Calculate error rate."""
        if self.metrics["requests"]["total"] == 0:
            return 0.0
        return (self.metrics["requests"]["failed"] / self.metrics["requests"]["total"]) * 100
        
    def _get_latest_resource_usage(self, resource_type: str) -> float:
        """Get latest resource usage value."""
        if not self.metrics["resource_usage"][resource_type]:
            return 0.0
        return self.metrics["resource_usage"][resource_type][-1]["value"]
        
    def _has_gpu(self) -> bool:
        """Check if GPU is available."""
        try:
            import torch
            return torch.cuda.is_available()
        except ImportError:
            return False
            
    def _get_gpu_usage(self) -> float:
        """Get GPU usage percentage."""
        try:
            import torch
            if not torch.cuda.is_available():
                return 0.0
            
            # Get GPU memory usage
            gpu_memory_used = torch.cuda.memory_allocated(0)
            gpu_memory_total = torch.cuda.get_device_properties(0).total_memory
            return (gpu_memory_used / gpu_memory_total) * 100
            
        except Exception:
            return 0.0
