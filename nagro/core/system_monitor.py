"""
NAGRO 4.1 — System Monitor.

Tracks system resources, model performance, and usage statistics.
"""

from __future__ import annotations
import os
import sys
import time
import platform
from dataclasses import dataclass, field


@dataclass
class RequestMetrics:
    """Metrics for a single request."""
    task_type: str
    processing_time: float
    input_tokens: int = 0
    output_tokens: int = 0
    timestamp: float = field(default_factory=time.time)


class SystemMonitor:
    """Monitors system resources and NAGRO performance."""

    def __init__(self):
        self.start_time = time.time()
        self.request_history: list[RequestMetrics] = []
        self.total_requests = 0
        self.error_count = 0

    def record_request(self, metrics: RequestMetrics):
        self.request_history.append(metrics)
        self.total_requests += 1
        if len(self.request_history) > 1000:
            self.request_history = self.request_history[-500:]

    def record_error(self):
        self.error_count += 1

    def get_system_info(self) -> dict:
        """Get current system information."""
        try:
            import psutil
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage("/")
            ram_info = {
                "total_gb": round(memory.total / (1024**3), 1),
                "used_gb": round(memory.used / (1024**3), 1),
                "available_gb": round(memory.available / (1024**3), 1),
                "percent": memory.percent,
            }
            disk_info = {
                "total_gb": round(disk.total / (1024**3), 1),
                "used_gb": round(disk.used / (1024**3), 1),
                "free_gb": round(disk.free / (1024**3), 1),
            }
        except ImportError:
            cpu_percent = -1
            ram_info = {"note": "Install psutil for detailed RAM info"}
            disk_info = {"note": "Install psutil for disk info"}

        gpu_info = self._get_gpu_info()

        return {
            "platform": platform.system(),
            "platform_version": platform.version(),
            "python_version": sys.version.split()[0],
            "cpu_cores": os.cpu_count(),
            "cpu_percent": cpu_percent,
            "ram": ram_info,
            "disk": disk_info,
            "gpu": gpu_info,
        }

    def _get_gpu_info(self) -> dict:
        """Detect GPU availability."""
        try:
            import torch
            if torch.cuda.is_available():
                return {
                    "available": True,
                    "name": torch.cuda.get_device_name(0),
                    "vram_gb": round(torch.cuda.get_device_properties(0).total_mem / (1024**3), 1),
                    "cuda_version": torch.version.cuda or "N/A",
                }
            return {"available": False, "reason": "CUDA not available"}
        except ImportError:
            return {"available": False, "reason": "PyTorch not installed"}

    def get_performance_stats(self) -> dict:
        """Get NAGRO performance statistics."""
        uptime = time.time() - self.start_time

        if not self.request_history:
            return {
                "uptime_seconds": round(uptime),
                "total_requests": 0,
                "avg_response_time": 0,
                "requests_per_minute": 0,
            }

        times = [r.processing_time for r in self.request_history]
        task_breakdown = {}
        for r in self.request_history:
            task_breakdown[r.task_type] = task_breakdown.get(r.task_type, 0) + 1

        return {
            "uptime_seconds": round(uptime),
            "uptime_human": self._format_duration(uptime),
            "total_requests": self.total_requests,
            "error_count": self.error_count,
            "error_rate": round(self.error_count / max(self.total_requests, 1) * 100, 1),
            "avg_response_time": round(sum(times) / len(times), 3),
            "min_response_time": round(min(times), 3),
            "max_response_time": round(max(times), 3),
            "requests_per_minute": round(self.total_requests / max(uptime / 60, 1), 1),
            "task_breakdown": task_breakdown,
        }

    def _format_duration(self, seconds: float) -> str:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        if hours > 0:
            return f"{hours}h {minutes}m {secs}s"
        if minutes > 0:
            return f"{minutes}m {secs}s"
        return f"{secs}s"

    def get_full_report(self) -> dict:
        return {
            "system": self.get_system_info(),
            "performance": self.get_performance_stats(),
            "model": "NAGRO 4.1",
            "version": "4.1.0",
        }
