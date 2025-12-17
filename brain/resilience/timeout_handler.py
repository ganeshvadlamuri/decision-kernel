"""Timeout handling for long-running operations."""

import time
from collections.abc import Callable
from typing import Any


class TimeoutHandler:
    """Handle operation timeouts gracefully."""

    def __init__(self, default_timeout: float = 30.0) -> None:
        self.default_timeout = default_timeout

    def execute_with_timeout(
        self, action: Callable[[], Any], timeout: float | None = None
    ) -> dict[str, Any]:
        """Execute action with timeout."""
        timeout = timeout or self.default_timeout
        start_time = time.time()

        try:
            # Simple timeout check (real implementation would use threading/async)
            result = action()
            elapsed = time.time() - start_time

            if elapsed > timeout:
                return {
                    "success": False,
                    "error": "Operation timed out",
                    "elapsed_time": elapsed,
                    "timeout": timeout,
                }

            return {
                "success": True,
                "result": result,
                "elapsed_time": elapsed,
            }
        except Exception as e:
            elapsed = time.time() - start_time
            return {
                "success": False,
                "error": str(e),
                "elapsed_time": elapsed,
            }

    def with_progressive_timeout(
        self, action: Callable[[], Any], timeouts: list[float]
    ) -> dict[str, Any]:
        """Try action with progressively longer timeouts."""
        for i, timeout in enumerate(timeouts):
            result = self.execute_with_timeout(action, timeout)
            if result["success"]:
                return {
                    "success": True,
                    "result": result["result"],
                    "timeout_used": timeout,
                    "attempt": i + 1,
                }

        return {
            "success": False,
            "error": "All timeout attempts exhausted",
            "timeouts_tried": timeouts,
        }
