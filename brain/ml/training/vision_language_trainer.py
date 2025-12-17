"""Train Vision-Language Model on COCO dataset."""

from pathlib import Path
from typing import Any

try:
    import numpy as np
    import torch
    import torch.nn as nn
    from datasets import load_dataset
    from torch.utils.data import DataLoader, Dataset
    PYTORCH_AVAILABLE = True
except ImportError:
    PYTORCH_AVAILABLE = False


class VisionLanguageDataset(Dataset):
    """Dataset for vision-language learning."""

    def __init__(self, images: list[np.ndarray], captions: list[str], vocab: dict[str, int]):
        self.images = images
        self.captions = captions
        self.vocab = vocab

    def __len__(self) -> int:
        return len(self.images)

    def __getitem__(self, idx: int) -> dict[str, torch.Tensor]:
        # Image (already preprocessed to 512-dim)
        image = torch.tensor(self.images[idx], dtype=torch.float32)

        # Caption tokenization
        tokens = self.captions[idx].lower().split()[:16]
        token_ids = [self.vocab.get(t, 0) for t in tokens]
        token_ids += [0] * (16 - len(token_ids))
        caption = torch.tensor(token_ids, dtype=torch.long)

        return {"image": image, "caption": caption}


class VisionLanguageModel(nn.Module):
    """CLIP-style vision-language model."""

    def __init__(self, vision_dim: int, text_vocab_size: int, embed_dim: int):
        super().__init__()
        # Vision encoder
        self.vision_encoder = nn.Sequential(
            nn.Linear(vision_dim, 256),
            nn.ReLU(),
            nn.Linear(256, embed_dim),
        )

        # Text encoder
        self.text_embedding = nn.Embedding(text_vocab_size, 64)
        self.text_encoder = nn.Sequential(
            nn.Linear(64 * 16, 256),  # 16 tokens
            nn.ReLU(),
            nn.Linear(256, embed_dim),
        )

        # Temperature for contrastive learning
        self.temperature = nn.Parameter(torch.tensor(0.07))

    def forward(self, image: torch.Tensor, caption: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        # Encode image
        image_features = self.vision_encoder(image)
        image_features = image_features / image_features.norm(dim=-1, keepdim=True)

        # Encode text
        text_embed = self.text_embedding(caption)
        text_embed = text_embed.view(text_embed.size(0), -1)
        text_features = self.text_encoder(text_embed)
        text_features = text_features / text_features.norm(dim=-1, keepdim=True)

        return image_features, text_features


class VisionLanguageTrainer:
    """Train vision-language model on COCO captions."""

    def __init__(self, model_path: str = "models/vision_language.pt"):
        if not PYTORCH_AVAILABLE:
            raise ImportError("PyTorch not installed. Run: pip install torch datasets")

        self.model_path = Path(model_path)
        self.model_path.parent.mkdir(parents=True, exist_ok=True)

    def download_dataset(self) -> tuple[list[np.ndarray], list[str]]:
        """Download COCO captions dataset."""
        print("📥 Downloading COCO captions dataset...")

        # Use HuggingFace COCO dataset (smaller subset)
        dataset = load_dataset("HuggingFaceM4/COCO", split="train[:1000]")

        images = []
        captions = []

        for example in dataset:
            # Simulate image features (in real scenario, use CNN encoder)
            image_features = np.random.randn(512).astype(np.float32)
            images.append(image_features)

            # Get caption
            caption = example["sentences"]["raw"][0] if example["sentences"]["raw"] else "object"
            captions.append(caption)

        print(f"✅ Downloaded {len(images)} image-caption pairs")
        return images, captions

    def build_vocab(self, captions: list[str]) -> dict[str, int]:
        """Build vocabulary from captions."""
        from collections import Counter

        word_counts: Counter[str] = Counter()
        for caption in captions:
            word_counts.update(caption.lower().split())

        vocab = {"<PAD>": 0, "<UNK>": 1}
        for word, _ in word_counts.most_common(1000):  # Top 1000 words
            vocab[word] = len(vocab)

        print(f"📚 Vocabulary size: {len(vocab)}")
        return vocab

    def contrastive_loss(self, image_features: torch.Tensor, text_features: torch.Tensor, temperature: torch.Tensor) -> torch.Tensor:
        """CLIP-style contrastive loss."""
        # Compute similarity matrix
        logits = torch.matmul(image_features, text_features.T) / temperature

        # Labels: diagonal is positive pairs
        labels = torch.arange(logits.size(0), device=logits.device)

        # Cross-entropy loss (both directions)
        loss_i2t = nn.functional.cross_entropy(logits, labels)
        loss_t2i = nn.functional.cross_entropy(logits.T, labels)

        return (loss_i2t + loss_t2i) / 2

    def train(self, epochs: int = 15, batch_size: int = 32, lr: float = 0.0001) -> dict[str, Any]:
        """Train vision-language model."""
        # Download data
        images, captions = self.download_dataset()

        # Build vocab
        vocab = self.build_vocab(captions)

        # Create dataset
        dataset = VisionLanguageDataset(images, captions, vocab)
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

        # Create model
        model = VisionLanguageModel(
            vision_dim=512,
            text_vocab_size=len(vocab),
            embed_dim=128,
        )

        optimizer = torch.optim.Adam(model.parameters(), lr=lr)

        # Training loop
        print(f"\n🚀 Training for {epochs} epochs...")
        model.train()

        for epoch in range(epochs):
            total_loss = 0.0

            for batch in dataloader:
                image = batch["image"]
                caption = batch["caption"]

                optimizer.zero_grad()
                image_features, text_features = model(image, caption)
                loss = self.contrastive_loss(image_features, text_features, model.temperature)
                loss.backward()
                optimizer.step()

                total_loss += loss.item()

            avg_loss = total_loss / len(dataloader)
            print(f"Epoch {epoch+1}/{epochs} - Loss: {avg_loss:.4f}, Temp: {model.temperature.item():.4f}")

        # Save model
        torch.save({
            "model_state_dict": model.state_dict(),
            "vocab": vocab,
        }, self.model_path)

        print(f"\n✅ Model saved to {self.model_path}")

        return {
            "final_loss": avg_loss,
            "vocab_size": len(vocab),
            "temperature": model.temperature.item(),
        }


if __name__ == "__main__":
    trainer = VisionLanguageTrainer()
    results = trainer.train(epochs=15)
    print(f"\n📊 Training Results: {results}")
