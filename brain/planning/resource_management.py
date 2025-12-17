"""Resource management - Track battery, time, materials."""

from typing import Any


class ResourceManager:
    """Track battery, time, materials."""

    def __init__(self, battery: float = 100.0, time_budget: float = 3600.0) -> None:
        self.battery = battery
        self.time_budget = time_budget
        self.materials: dict[str, int] = {}

    def check_resources(self, plan: list[str], costs: dict[str, dict[str, float]]) -> dict[str, Any]:
        """Check if resources are sufficient for plan."""
        total_battery = sum(costs.get(action, {}).get("battery", 0) for action in plan)
        total_time = sum(costs.get(action, {}).get("time", 0) for action in plan)

        return {
            "sufficient_battery": total_battery <= self.battery,
            "sufficient_time": total_time <= self.time_budget,
            "battery_required": total_battery,
            "time_required": total_time,
            "battery_available": self.battery,
            "time_available": self.time_budget,
        }

    def consume(self, resource: str, amount: float) -> None:
        """Consume resource."""
        if resource == "battery":
            self.battery -= amount
        elif resource == "time":
            self.time_budget -= amount
