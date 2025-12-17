"""Retry mechanisms with exponential backoff and adaptive strategies."""

import time
from collections.abc import Callable
from typing import Any

from .exceptions import PermanentException, TransientException


class RetryMechanism:
    """Exponential backoff retry with jitter."""

    def __init__(
        self,
        max_attempts: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        exponential_base: float = 2.0,
    ) -> None:
        self.max_attempts = max_attempts
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base

    def execute_with_retry(
        self, action: Callable[[], Any], action_name: str = "action"
    ) -> dict[str, Any]:
        """Execute action with exponential backoff retry."""
        last_error = None

        for attempt in range(self.max_attempts):
            try:
                result = action()
                return {
                    "success": True,
                    "result": result,
                    "attempts": attempt + 1,
                }
            except PermanentException as e:
                # Don't retry permanent errors
                return {
                    "success": False,
                    "error": str(e),
                    "error_type": "permanent",
                    "attempts": attempt + 1,
                }
            except TransientException as e:
                last_error = e
                if attempt < self.max_attempts - 1:
                    delay = self._calculate_delay(attempt)
                    time.sleep(delay)
            except Exception as e:
                last_error = e
                if attempt < self.max_attempts - 1:
                    delay = self._calculate_delay(attempt)
                    time.sleep(delay)

        return {
            "success": False,
            "error": str(last_error),
            "error_type": "max_retries_exceeded",
            "attempts": self.max_attempts,
        }

    def _calculate_delay(self, attempt: int) -> float:
        """Calculate exponential backoff delay with jitter."""
        delay = min(
            self.base_delay * (self.exponential_base**attempt), self.max_delay
        )
        # Add jitter (±20%)
        import random

        jitter = delay * 0.2 * (random.random() - 0.5)
        return delay + jitter
