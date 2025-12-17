"""Circuit breaker pattern to prevent cascading failures."""

import time
from collections.abc import Callable
from typing import Any


class CircuitBreaker:
    """Prevent repeated attempts when system is failing."""

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 60.0,
        half_open_attempts: int = 1,
    ) -> None:
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_attempts = half_open_attempts

        self.failure_count = 0
        self.last_failure_time = 0.0
        self.state = "closed"  # closed, open, half_open
        self.half_open_successes = 0

    def execute(self, action: Callable[[], Any]) -> dict[str, Any]:
        """Execute action through circuit breaker."""
        if self.state == "open":
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = "half_open"
                self.half_open_successes = 0
            else:
                return {
                    "success": False,
                    "error": "Circuit breaker is open",
                    "circuit_state": "open",
                }

        try:
            result = action()
            self._on_success()
            return {"success": True, "result": result, "circuit_state": self.state}
        except Exception as e:
            self._on_failure()
            return {
                "success": False,
                "error": str(e),
                "circuit_state": self.state,
            }

    def _on_success(self) -> None:
        """Handle successful execution."""
        if self.state == "half_open":
            self.half_open_successes += 1
            if self.half_open_successes >= self.half_open_attempts:
                self.state = "closed"
                self.failure_count = 0
        elif self.state == "closed":
            self.failure_count = 0

    def _on_failure(self) -> None:
        """Handle failed execution."""
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.failure_count >= self.failure_threshold:
            self.state = "open"

    def reset(self) -> None:
        """Manually reset circuit breaker."""
        self.state = "closed"
        self.failure_count = 0
        self.half_open_successes = 0
