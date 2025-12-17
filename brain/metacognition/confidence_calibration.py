"""Confidence calibration - Accurate self-assessment."""


class ConfidenceCalibrator:
    """Accurate self-assessment."""

    def __init__(self) -> None:
        self.predictions: list[tuple[float, bool]] = []  # (confidence, actual_success)

    def record_outcome(self, predicted_confidence: float, actual_success: bool) -> None:
        """Record prediction and outcome."""
        self.predictions.append((predicted_confidence, actual_success))

    def calibration_error(self) -> float:
        """Calculate calibration error."""
        if not self.predictions:
            return 0.0

        # Group by confidence bins
        bins = {i: [] for i in range(10)}
        for conf, success in self.predictions:
            bin_idx = min(int(conf * 10), 9)
            bins[bin_idx].append(1.0 if success else 0.0)

        # Calculate error
        total_error = 0.0
        for bin_idx, outcomes in bins.items():
            if outcomes:
                predicted = (bin_idx + 0.5) / 10
                actual = sum(outcomes) / len(outcomes)
                total_error += abs(predicted - actual)

        return total_error / 10

    def is_well_calibrated(self) -> bool:
        """Check if confidence is well calibrated."""
        return self.calibration_error() < 0.15
