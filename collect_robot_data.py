"""Collect robot data for training."""

import json
from datetime import datetime
from pathlib import Path


class RobotDataCollector:
    """Collect robot execution data for ML training."""

    def __init__(self, data_dir: str = "data/robot_logs"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.intent_log = self.data_dir / "intents.jsonl"
        self.policy_log = self.data_dir / "trajectories.jsonl"

    def log_intent(self, command: str, intent: str, entities: dict) -> None:
        """Log human command and parsed intent."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "command": command,
            "intent": intent,
            "entities": entities,
        }

        with open(self.intent_log, "a") as f:
            f.write(json.dumps(entry) + "\n")

        print(f"✅ Logged intent: {command} -> {intent}")

    def log_trajectory(self, state: dict, action: str, reward: float) -> None:
        """Log robot state, action, and reward."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "state": state,
            "action": action,
            "reward": reward,
        }

        with open(self.policy_log, "a") as f:
            f.write(json.dumps(entry) + "\n")

        print(f"✅ Logged trajectory: {action} (reward: {reward})")

    def get_stats(self) -> dict:
        """Get collection statistics."""
        intent_count = 0
        if self.intent_log.exists():
            with open(self.intent_log) as f:
                intent_count = sum(1 for _ in f)

        trajectory_count = 0
        if self.policy_log.exists():
            with open(self.policy_log) as f:
                trajectory_count = sum(1 for _ in f)

        return {
            "intents_collected": intent_count,
            "trajectories_collected": trajectory_count,
            "data_dir": str(self.data_dir),
        }


# Example usage
if __name__ == "__main__":
    collector = RobotDataCollector()

    print("🤖 Robot Data Collector")
    print("=" * 60)
    print("\nCollecting sample data...\n")

    # Collect intent examples
    collector.log_intent("bring me water", "fetch_object", {"object": "water"})
    collector.log_intent("clean the kitchen", "clean_area", {"area": "kitchen"})
    collector.log_intent("go to bedroom", "navigate", {"location": "bedroom"})

    # Collect trajectory examples
    collector.log_trajectory(
        state={"x": 0, "y": 0, "battery": 100},
        action="move_forward",
        reward=1.0,
    )
    collector.log_trajectory(
        state={"x": 1, "y": 0, "battery": 99},
        action="turn_left",
        reward=0.5,
    )

    # Show stats
    stats = collector.get_stats()
    print("\n" + "=" * 60)
    print("📊 Collection Stats:")
    for key, value in stats.items():
        print(f"  {key}: {value}")

    print("\n✅ Data saved! Use this data to train models:")
    print("  python train_with_custom_data.py")
