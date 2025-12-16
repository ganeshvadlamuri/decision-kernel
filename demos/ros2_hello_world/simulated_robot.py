"""Simulated ROS2 robot data publisher (no ROS2 dependency)"""

from dataclasses import dataclass


@dataclass
class Transform:
    """Simulated /tf transform"""

    frame_id: str
    child_frame_id: str
    x: float
    y: float
    z: float


@dataclass
class Odometry:
    """Simulated /odom message"""

    frame_id: str
    x: float
    y: float
    theta: float


class SimulatedROS2Robot:
    """Simulates ROS2 topics without requiring ROS2 installation"""

    def __init__(self):
        self.tf_data = [
            Transform("world", "base_link", 1.0, 2.0, 0.0),
            Transform("world", "kitchen", 5.0, 3.0, 0.0),
        ]
        self.odom_data = Odometry("odom", 1.0, 2.0, 0.0)

    def get_tf(self) -> list[Transform]:
        """Simulate reading /tf topic"""
        return self.tf_data

    def get_odom(self) -> Odometry:
        """Simulate reading /odom topic"""
        return self.odom_data

    def publish_cmd_vel(self, linear: float, angular: float):
        """Simulate publishing to /cmd_vel"""
        print(f"[SIM] /cmd_vel: linear={linear}, angular={angular}")

    def publish_gripper_command(self, position: float):
        """Simulate publishing to /gripper/command"""
        print(f"[SIM] /gripper/command: position={position}")
