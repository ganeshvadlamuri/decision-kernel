"""Train Intent Transformer on conversational datasets."""

from pathlib import Path
from typing import Any

try:
    import torch
    import torch.nn as nn
    from datasets import load_dataset  # HuggingFace datasets
    from torch.utils.data import DataLoader, Dataset
    PYTORCH_AVAILABLE = True
except ImportError:
    PYTORCH_AVAILABLE = False


class IntentDataset(Dataset):
    """Dataset for intent classification."""

    def __init__(self, texts: list[str], intents: list[str], vocab: dict[str, int]):
        self.texts = texts
        self.intents = intents
        self.vocab = vocab
        self.intent_to_idx = {intent: idx for idx, intent in enumerate(set(intents))}

    def __len__(self) -> int:
        return len(self.texts)

    def __getitem__(self, idx: int) -> dict[str, Any]:
        text = self.texts[idx]
        intent = self.intents[idx]

        # Tokenize
        tokens = text.lower().split()[:32]  # Max 32 tokens
        token_ids = [self.vocab.get(t, 0) for t in tokens]

        # Pad to 32
        token_ids += [0] * (32 - len(token_ids))

        return {
            "input_ids": torch.tensor(token_ids, dtype=torch.long),
            "label": torch.tensor(self.intent_to_idx[intent], dtype=torch.long),
        }


class IntentTransformerModel(nn.Module):
    """PyTorch transformer for intent classification."""

    def __init__(self, vocab_size: int, embed_dim: int, num_heads: int, num_intents: int):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.transformer = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(d_model=embed_dim, nhead=num_heads, batch_first=True),
            num_layers=2,
        )
        self.classifier = nn.Linear(embed_dim, num_intents)

    def forward(self, input_ids: torch.Tensor) -> torch.Tensor:
        x = self.embedding(input_ids)
        x = self.transformer(x)
        x = x.mean(dim=1)  # Pool
        return self.classifier(x)


class IntentTransformerTrainer:
    """Train intent transformer on open-source datasets."""

    def __init__(self, model_path: str = "models/intent_transformer.pt"):
        if not PYTORCH_AVAILABLE:
            raise ImportError("PyTorch not installed. Run: pip install torch datasets transformers")

        self.model_path = Path(model_path)
        self.model_path.parent.mkdir(parents=True, exist_ok=True)

    def download_dataset(self) -> tuple[list[str], list[str]]:
        """Download daily_dialog dataset from HuggingFace."""
        print("📥 Downloading daily_dialog dataset...")
        dataset = load_dataset("daily_dialog", split="train[:5000]")  # 5K samples

        texts = []
        intents = []

        intent_map = {
            0: "inform",
            1: "question",
            2: "directive",
            3: "commissive",
        }

        for example in dataset:
            dialog = example["dialog"]
            acts = example["act"]

            for utterance, act in zip(dialog, acts):
                if utterance.strip():
                    texts.append(utterance)
                    intents.append(intent_map.get(act, "inform"))

        print(f"✅ Downloaded {len(texts)} examples")
        return texts, intents

    def build_vocab(self, texts: list[str], min_freq: int = 2) -> dict[str, int]:
        """Build vocabulary from texts."""
        from collections import Counter

        word_counts: Counter[str] = Counter()
        for text in texts:
            word_counts.update(text.lower().split())

        vocab = {"<PAD>": 0, "<UNK>": 1}
        for word, count in word_counts.items():
            if count >= min_freq:
                vocab[word] = len(vocab)

        print(f"📚 Vocabulary size: {len(vocab)}")
        return vocab

    def train(self, epochs: int = 10, batch_size: int = 32, lr: float = 0.001) -> dict[str, Any]:
        """Train intent transformer."""
        # Download data
        texts, intents = self.download_dataset()

        # Build vocab
        vocab = self.build_vocab(texts)

        # Create dataset
        dataset = IntentDataset(texts, intents, vocab)
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

        # Create model
        num_intents = len(set(intents))
        model = IntentTransformerModel(
            vocab_size=len(vocab),
            embed_dim=128,
            num_heads=4,
            num_intents=num_intents,
        )

        optimizer = torch.optim.Adam(model.parameters(), lr=lr)
        criterion = nn.CrossEntropyLoss()

        # Training loop
        print(f"\n🚀 Training for {epochs} epochs...")
        model.train()

        for epoch in range(epochs):
            total_loss = 0.0
            correct = 0
            total = 0

            for batch in dataloader:
                input_ids = batch["input_ids"]
                labels = batch["label"]

                optimizer.zero_grad()
                outputs = model(input_ids)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()

                total_loss += loss.item()
                _, predicted = outputs.max(1)
                correct += (predicted == labels).sum().item()
                total += labels.size(0)

            accuracy = 100.0 * correct / total
            avg_loss = total_loss / len(dataloader)
            print(f"Epoch {epoch+1}/{epochs} - Loss: {avg_loss:.4f}, Accuracy: {accuracy:.2f}%")

        # Save model
        torch.save({
            "model_state_dict": model.state_dict(),
            "vocab": vocab,
            "num_intents": num_intents,
        }, self.model_path)

        print(f"\n✅ Model saved to {self.model_path}")

        return {
            "final_accuracy": accuracy,
            "final_loss": avg_loss,
            "vocab_size": len(vocab),
            "num_intents": num_intents,
        }


if __name__ == "__main__":
    trainer = IntentTransformerTrainer()
    results = trainer.train(epochs=10)
    print(f"\n📊 Training Results: {results}")
