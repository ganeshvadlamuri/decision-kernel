
from brain.planner.actions import Action


class SimulationAdapter:
    """Simulation environment adapter (stub only)"""

    def __init__(self):
        raise NotImplementedError("Simulation adapter not yet implemented")

    def execute(self, plan: list[Action]):
        raise NotImplementedError("Simulation execution not yet implemented")
