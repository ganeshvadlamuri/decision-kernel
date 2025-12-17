"""Anomaly detection - Detect unusual patterns."""

import statistics
from typing import Any


class AnomalyDetector:
    """'This doesn't look right'."""

    def __init__(self, threshold: float = 2.0) -> None:
        self.threshold = threshold  # Standard deviations
        self.history: dict[str, list[float]] = {}

    def record(self, metric: str, value: float) -> None:
        """Record metric value."""
        if metric not in self.history:
            self.history[metric] = []
        self.history[metric].append(value)

        # Keep last 100 values
        if len(self.history[metric]) > 100:
            self.history[metric] = self.history[metric][-100:]

    def is_anomaly(self, metric: str, value: float) -> dict[str, Any]:
        """Check if value is anomalous."""
        if metric not in self.history or len(self.history[metric]) < 3:
            return {"is_anomaly": False, "reason": "insufficient_data"}

        values = self.history[metric]
        mean = statistics.mean(values)
        stdev = statistics.stdev(values) if len(values) > 1 else 0.0

        if stdev == 0:
            is_anomaly = value != mean
            z_score = 0.0
        else:
            z_score = abs(value - mean) / stdev
            is_anomaly = z_score > self.threshold

        return {
            "is_anomaly": is_anomaly,
            "z_score": z_score,
            "mean": mean,
            "stdev": stdev,
            "value": value,
        }
