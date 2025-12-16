
from brain.planner.actions import Action


class ROSAdapter:
    """ROS integration adapter (stub only)"""

    def __init__(self):
        raise NotImplementedError("ROS adapter not yet implemented")

    def execute(self, plan: list[Action]):
        raise NotImplementedError("ROS execution not yet implemented")
