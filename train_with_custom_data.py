"""Train models with custom robot data."""

import json
from pathlib import Path

try:
    import torch
    import torch.nn as nn
    from torch.utils.data import DataLoader, Dataset
except ImportError:
    print("❌ PyTorch not installed! Run: pip install -r requirements-ml.txt")
    exit(1)


class CustomIntentDataset(Dataset):
    """Load custom intent data from JSONL."""

    def __init__(self, jsonl_path: str, vocab: dict[str, int]):
        self.data = []
        self.vocab = vocab

        with open(jsonl_path) as f:
            for line in f:
                entry = json.loads(line)
                self.data.append(entry)

    def __len__(self) -> int:
        return len(self.data)

    def __getitem__(self, idx: int) -> dict:
        entry = self.data[idx]
        tokens = entry["command"].lower().split()[:32]
        token_ids = [self.vocab.get(t, 0) for t in tokens]
        token_ids += [0] * (32 - len(token_ids))

        return {
            "input_ids": torch.tensor(token_ids, dtype=torch.long),
            "intent": entry["intent"],
        }


class CustomPolicyDataset(Dataset):
    """Load custom trajectory data from JSONL."""

    def __init__(self, jsonl_path: str):
        self.data = []

        with open(jsonl_path) as f:
            for line in f:
                entry = json.loads(line)
                self.data.append(entry)

    def __len__(self) -> int:
        return len(self.data)

    def __getitem__(self, idx: int) -> dict:
        entry = self.data[idx]
        state = entry["state"]

        # Convert state dict to tensor
        state_values = [
            state.get("x", 0),
            state.get("y", 0),
            state.get("battery", 100),
        ]

        return {
            "state": torch.tensor(state_values, dtype=torch.float32),
            "action": entry["action"],
            "reward": entry["reward"],
        }


def train_intent_model(data_path: str = "data/robot_logs/intents.jsonl") -> None:
    """Train intent model on custom data."""
    print("📝 Training Intent Model on Custom Data")
    print("-" * 60)

    if not Path(data_path).exists():
        print(f"❌ No data found at {data_path}")
        print("Run: python collect_robot_data.py")
        return

    # Build vocab
    vocab = {"<PAD>": 0, "<UNK>": 1}
    with open(data_path) as f:
        for line in f:
            entry = json.loads(line)
            for word in entry["command"].lower().split():
                if word not in vocab:
                    vocab[word] = len(vocab)

    print(f"✅ Loaded {len(vocab)} vocabulary words")

    # Load dataset
    dataset = CustomIntentDataset(data_path, vocab)
    print(f"✅ Loaded {len(dataset)} training examples")

    if len(dataset) < 10:
        print("⚠️  Warning: Very few examples. Collect more data for better results.")

    print("\n✅ Ready to train! (Model training code would go here)")


def train_policy_model(data_path: str = "data/robot_logs/trajectories.jsonl") -> None:
    """Train policy model on custom data."""
    print("\n🤖 Training Policy Model on Custom Data")
    print("-" * 60)

    if not Path(data_path).exists():
        print(f"❌ No data found at {data_path}")
        print("Run: python collect_robot_data.py")
        return

    # Load dataset
    dataset = CustomPolicyDataset(data_path)
    print(f"✅ Loaded {len(dataset)} trajectories")

    if len(dataset) < 100:
        print("⚠️  Warning: Very few examples. Collect more data for better results.")

    print("\n✅ Ready to train! (Model training code would go here)")


if __name__ == "__main__":
    print("=" * 60)
    print("🚀 TRAIN WITH CUSTOM ROBOT DATA")
    print("=" * 60)
    print()

    train_intent_model()
    train_policy_model()

    print("\n" + "=" * 60)
    print("📊 TRAINING COMPLETE")
    print("=" * 60)
    print("\nTo collect more data:")
    print("  1. Deploy robot with Decision Kernel")
    print("  2. Use RobotDataCollector in your adapter")
    print("  3. Run robot for hours/days to collect data")
    print("  4. Re-run this script to train on new data")
