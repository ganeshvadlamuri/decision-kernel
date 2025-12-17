"""Train all ML models with open-source datasets."""

import sys
from pathlib import Path

# Check PyTorch availability
try:
    import torch
    print(f"✅ PyTorch {torch.__version__} detected")
except ImportError:
    print("❌ PyTorch not installed!")
    print("\nInstall with:")
    print("  pip install torch torchvision")
    print("  pip install datasets transformers")
    sys.exit(1)

from brain.ml.training import (
    IntentTransformerTrainer,
    NeuralPolicyTrainer,
    VisionLanguageTrainer,
    MetaLearnerTrainer,
)


def main() -> None:
    """Train all models."""
    print("=" * 80)
    print("🚀 DECISION KERNEL - ML MODEL TRAINING")
    print("=" * 80)
    print("\nTraining 4 revolutionary ML models on open-source datasets:")
    print("  1. Intent Transformer (daily_dialog dataset)")
    print("  2. Neural Policy (synthetic robot demonstrations)")
    print("  3. Vision-Language Model (COCO captions)")
    print("  4. Meta-Learner (synthetic few-shot tasks)")
    print("\n" + "=" * 80)
    
    results = {}
    
    # 1. Intent Transformer
    print("\n\n📝 [1/4] TRAINING INTENT TRANSFORMER")
    print("-" * 80)
    try:
        trainer = IntentTransformerTrainer()
        results["intent"] = trainer.train(epochs=10, batch_size=32)
    except Exception as e:
        print(f"❌ Failed: {e}")
        results["intent"] = {"error": str(e)}
    
    # 2. Neural Policy
    print("\n\n🤖 [2/4] TRAINING NEURAL POLICY")
    print("-" * 80)
    try:
        trainer = NeuralPolicyTrainer()
        results["policy"] = trainer.train(epochs=20, batch_size=64)
    except Exception as e:
        print(f"❌ Failed: {e}")
        results["policy"] = {"error": str(e)}
    
    # 3. Vision-Language Model
    print("\n\n👁️ [3/4] TRAINING VISION-LANGUAGE MODEL")
    print("-" * 80)
    try:
        trainer = VisionLanguageTrainer()
        results["vision_language"] = trainer.train(epochs=15, batch_size=32)
    except Exception as e:
        print(f"❌ Failed: {e}")
        results["vision_language"] = {"error": str(e)}
    
    # 4. Meta-Learner
    print("\n\n🧠 [4/4] TRAINING META-LEARNER")
    print("-" * 80)
    try:
        trainer = MetaLearnerTrainer()
        results["meta"] = trainer.train(epochs=100, num_tasks=1000)
    except Exception as e:
        print(f"❌ Failed: {e}")
        results["meta"] = {"error": str(e)}
    
    # Summary
    print("\n\n" + "=" * 80)
    print("📊 TRAINING SUMMARY")
    print("=" * 80)
    
    for model_name, result in results.items():
        print(f"\n{model_name.upper()}:")
        if "error" in result:
            print(f"  ❌ Failed: {result['error']}")
        else:
            for key, value in result.items():
                print(f"  {key}: {value}")
    
    print("\n✅ Training complete! Models saved to models/ directory")
    print("\nNext steps:")
    print("  1. Test models: python -m demos.ml_models_demo")
    print("  2. Deploy to robot: Integrate trained models into adapters")
    print("  3. Fine-tune: Collect real robot data and continue training")


if __name__ == "__main__":
    main()
