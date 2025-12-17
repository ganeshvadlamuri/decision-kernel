"""Deadline awareness - Must finish by time."""

from datetime import datetime, timedelta
from typing import Any


class DeadlineManager:
    """'Must finish by 3 PM'."""

    def check_deadline(self, deadline: datetime, estimated_duration: float) -> dict[str, Any]:
        """Check if deadline can be met."""
        now = datetime.now()
        time_remaining = (deadline - now).total_seconds()

        can_meet = time_remaining >= estimated_duration
        urgency = 1.0 - (time_remaining / estimated_duration) if estimated_duration > 0 else 1.0

        return {
            "deadline": deadline.isoformat(),
            "time_remaining": time_remaining,
            "estimated_duration": estimated_duration,
            "can_meet_deadline": can_meet,
            "urgency": min(max(urgency, 0.0), 1.0),
        }

    def latest_start_time(self, deadline: datetime, duration: float) -> datetime:
        """Calculate latest time to start."""
        return deadline - timedelta(seconds=duration)
