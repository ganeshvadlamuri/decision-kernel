"""Train Meta-Learner on few-shot learning benchmarks."""

from pathlib import Path
from typing import Any

try:
    import torch
    import torch.nn as nn
    from torch.utils.data import DataLoader, Dataset
    PYTORCH_AVAILABLE = True
except ImportError:
    PYTORCH_AVAILABLE = False


class MetaDataset(Dataset):
    """Dataset for meta-learning (tasks with few examples)."""

    def __init__(self, num_tasks: int, examples_per_task: int, input_dim: int):
        self.num_tasks = num_tasks
        self.examples_per_task = examples_per_task
        self.input_dim = input_dim

    def __len__(self) -> int:
        return self.num_tasks

    def __getitem__(self, idx: int) -> dict[str, torch.Tensor]:
        # Generate synthetic task
        # Support set (for adaptation)
        support_x = torch.randn(self.examples_per_task, self.input_dim)
        support_y = torch.randint(0, 2, (self.examples_per_task,))

        # Query set (for evaluation)
        query_x = torch.randn(self.examples_per_task, self.input_dim)
        query_y = torch.randint(0, 2, (self.examples_per_task,))

        return {
            "support_x": support_x,
            "support_y": support_y,
            "query_x": query_x,
            "query_y": query_y,
        }


class MetaLearnerModel(nn.Module):
    """MAML-style meta-learner."""

    def __init__(self, input_dim: int, hidden_dim: int, output_dim: int):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, output_dim),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.network(x)


class MetaLearnerTrainer:
    """Train meta-learner using MAML algorithm."""

    def __init__(self, model_path: str = "models/meta_learner.pt"):
        if not PYTORCH_AVAILABLE:
            raise ImportError("PyTorch not installed. Run: pip install torch numpy")

        self.model_path = Path(model_path)
        self.model_path.parent.mkdir(parents=True, exist_ok=True)

    def adapt(self, model: nn.Module, support_x: torch.Tensor, support_y: torch.Tensor,
              steps: int = 5, lr: float = 0.01) -> nn.Module:
        """Adapt model to new task using support set."""
        # Clone model for task-specific adaptation
        adapted_model = MetaLearnerModel(
            input_dim=model.network[0].in_features,
            hidden_dim=model.network[0].out_features,
            output_dim=model.network[-1].out_features,
        )
        adapted_model.load_state_dict(model.state_dict())

        optimizer = torch.optim.SGD(adapted_model.parameters(), lr=lr)
        criterion = nn.CrossEntropyLoss()

        # Inner loop: adapt to task
        for _ in range(steps):
            optimizer.zero_grad()
            logits = adapted_model(support_x)
            loss = criterion(logits, support_y)
            loss.backward()
            optimizer.step()

        return adapted_model

    def train(self, epochs: int = 100, num_tasks: int = 1000, batch_size: int = 4,
              inner_lr: float = 0.01, outer_lr: float = 0.001) -> dict[str, Any]:
        """Train meta-learner using MAML."""
        print(f"🧠 Generating {num_tasks} meta-learning tasks...")

        # Create dataset
        dataset = MetaDataset(num_tasks=num_tasks, examples_per_task=5, input_dim=32)
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

        # Create model
        model = MetaLearnerModel(input_dim=32, hidden_dim=64, output_dim=2)
        meta_optimizer = torch.optim.Adam(model.parameters(), lr=outer_lr)
        criterion = nn.CrossEntropyLoss()

        # Training loop
        print(f"\n🚀 Meta-training for {epochs} epochs...")

        for epoch in range(epochs):
            total_loss = 0.0
            total_accuracy = 0.0
            num_batches = 0

            for batch in dataloader:
                meta_optimizer.zero_grad()
                batch_loss = 0.0
                batch_accuracy = 0.0

                # Process each task in batch
                for i in range(batch["support_x"].size(0)):
                    support_x = batch["support_x"][i]
                    support_y = batch["support_y"][i]
                    query_x = batch["query_x"][i]
                    query_y = batch["query_y"][i]

                    # Inner loop: adapt to task
                    adapted_model = self.adapt(model, support_x, support_y, steps=5, lr=inner_lr)

                    # Outer loop: evaluate on query set
                    logits = adapted_model(query_x)
                    loss = criterion(logits, query_y)
                    batch_loss += loss

                    # Calculate accuracy
                    _, predicted = logits.max(1)
                    accuracy = (predicted == query_y).float().mean()
                    batch_accuracy += accuracy

                # Meta-update
                batch_loss = batch_loss / batch["support_x"].size(0)
                batch_loss.backward()
                meta_optimizer.step()

                total_loss += batch_loss.item()
                total_accuracy += (batch_accuracy / batch["support_x"].size(0)).item()
                num_batches += 1

            avg_loss = total_loss / num_batches
            avg_accuracy = 100.0 * total_accuracy / num_batches

            if (epoch + 1) % 10 == 0:
                print(f"Epoch {epoch+1}/{epochs} - Loss: {avg_loss:.4f}, Accuracy: {avg_accuracy:.2f}%")

        # Save model
        torch.save({
            "model_state_dict": model.state_dict(),
            "input_dim": 32,
            "hidden_dim": 64,
            "output_dim": 2,
        }, self.model_path)

        print(f"\n✅ Model saved to {self.model_path}")

        return {
            "final_loss": avg_loss,
            "final_accuracy": avg_accuracy,
            "num_tasks": num_tasks,
        }


if __name__ == "__main__":
    trainer = MetaLearnerTrainer()
    results = trainer.train(epochs=100, num_tasks=1000)
    print(f"\n📊 Training Results: {results}")
