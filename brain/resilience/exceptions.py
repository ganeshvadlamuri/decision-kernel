"""Robot-specific exceptions for error handling."""


class RobotException(Exception):  # noqa: N818
    """Base exception for all robot errors."""

    pass


class HardwareException(RobotException):
    """Hardware-related errors."""

    pass


class SensorException(HardwareException):
    """Sensor failures."""

    pass


class ActuatorException(HardwareException):
    """Motor/actuator failures."""

    pass


class PerceptionException(RobotException):
    """Perception/vision errors."""

    pass


class NavigationException(RobotException):
    """Navigation errors."""

    pass


class ManipulationException(RobotException):
    """Grasping/manipulation errors."""

    pass


class PlanningException(RobotException):
    """Planning failures."""

    pass


class SafetyException(RobotException):
    """Safety violations."""

    pass


class TransientException(RobotException):
    """Temporary errors that may succeed on retry."""

    pass


class PermanentException(RobotException):
    """Permanent errors that won't succeed on retry."""

    pass
