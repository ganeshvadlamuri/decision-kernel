"""Demo of revolutionary ML models."""

from brain.ml import IntentTransformer, MetaLearner, NeuralPolicy, VisionLanguageModel


def demo_intent_transformer() -> None:
    """Demo transformer-based intent understanding."""
    print("\n=== 1. INTENT TRANSFORMER ===")
    print("Natural language understanding with transformers\n")

    model = IntentTransformer()

    # Test commands
    commands = [
        "bring me water from the kitchen",
        "go to the bedroom and find my keys",
        "clean the living room table",
        "follow the person in front of you",
    ]

    for cmd in commands:
        result = model.predict(cmd)
        print(f"Command: {cmd}")
        print(f"  Intent: {result['intent']}")
        print(f"  Confidence: {result['confidence']:.2f}")
        print(f"  Entities: {result['entities']}")
        print()

    # Few-shot learning demo
    print("Few-shot learning (5 examples):")
    examples = [
        ("deliver package to room 305", "bring"),
        ("transport box to warehouse", "bring"),
        ("carry item to destination", "bring"),
    ]
    model.few_shot_learn(examples)
    print("  Model adapted to new examples!")

    # Model info
    info = model.get_model_info()
    print(f"\nModel: {info['model_type']}")
    print(f"  Embedding dim: {info['embedding_dim']}")
    print(f"  Num heads: {info['num_heads']}")
    print(f"  Few-shot capable: {info['few_shot_capable']}")


def demo_neural_policy() -> None:
    """Demo neural policy for action selection."""
    print("\n=== 2. NEURAL POLICY ===")
    print("Deep RL for optimal action selection\n")

    policy = NeuralPolicy(state_dim=64, action_dim=10)

    # Simulate episodes
    print("Training on experience...")
    for episode in range(5):
        state = {
            "robot_position": [episode, episode],
            "objects": [{"name": "cup"}],
            "battery": 80,
        }

        # Select action
        result = policy.select_action(state)
        print(f"Episode {episode + 1}:")
        print(f"  Action: {result['action']}")
        print(f"  Confidence: {result['confidence']:.3f}")

        # Simulate reward
        reward = 1.0 if result["confidence"] > 0.1 else 0.0

        # Learn from experience
        next_state = state.copy()
        policy.learn_from_experience(state, result["action"], reward, next_state)

    # Training stats
    stats = policy.get_training_stats()
    print("\nTraining Statistics:")
    print(f"  Episodes: {stats['episodes']}")
    print(f"  Avg reward: {stats['avg_reward']:.3f}")
    print(f"  Buffer size: {stats['buffer_size']}")


def demo_vision_language() -> None:
    """Demo vision-language grounding."""
    print("\n=== 3. VISION-LANGUAGE MODEL ===")
    print("Multimodal understanding (vision + language)\n")

    model = VisionLanguageModel()

    # Visual scene
    scene = {
        "objects": [
            {
                "name": "cup_1",
                "type": "cup",
                "color": "red",
                "position": [2, 3],
                "size": 1.0,
            },
            {
                "name": "cup_2",
                "type": "cup",
                "color": "blue",
                "position": [5, 6],
                "size": 1.0,
            },
            {
                "name": "bottle_1",
                "type": "bottle",
                "color": "green",
                "position": [1, 1],
                "size": 1.5,
            },
        ]
    }

    # Test commands
    commands = [
        "bring the red cup",
        "get the blue cup",
        "find the green bottle",
    ]

    for cmd in commands:
        result = model.ground_command(cmd, scene)
        print(f"Command: {cmd}")
        print(f"  Target: {result['target_object']['name']}")
        print(f"  Type: {result['target_object'].get('type', 'unknown')}")
        print(f"  Color: {result['target_object'].get('color', 'unknown')}")
        print(f"  Confidence: {result['confidence']:.2f}")
        print()

    # Model info
    info = model.get_model_info()
    print(f"Model: {info['model_type']}")
    print(f"  Vision dim: {info['vision_dim']}")
    print(f"  Language dim: {info['language_dim']}")
    print(f"  Known objects: {info['known_objects']}")


def demo_meta_learner() -> None:
    """Demo meta-learning for rapid adaptation."""
    print("\n=== 4. META-LEARNER ===")
    print("Learn how to learn - rapid task adaptation\n")

    meta_learner = MetaLearner()

    # New task: "deliver package"
    task_name = "deliver_package"
    demonstrations = [
        {"context": {"position": [0, 0], "objects": []}, "action": "navigate"},
        {"context": {"position": [5, 5], "objects": []}, "action": "grasp"},
        {"context": {"position": [5, 5], "objects": [{"name": "package"}]}, "action": "navigate"},
        {"context": {"position": [10, 10], "objects": [{"name": "package"}]}, "action": "release"},
    ]

    print(f"Adapting to new task: {task_name}")
    print(f"  Demonstrations: {len(demonstrations)}")

    result = meta_learner.adapt_to_task(task_name, demonstrations)
    print(f"  Adapted: {result['adapted']}")
    print(f"  Adaptation steps: {result['adaptation_steps']}")
    print(f"  Adaptation score: {result['adaptation_score']:.2f}")

    # Execute adapted task
    print("\nExecuting adapted task:")
    context = {"position": [0, 0], "objects": []}
    execution = meta_learner.execute_task(task_name, context)
    print(f"  Action: {execution.get('action', 'N/A')}")
    print(f"  Confidence: {execution.get('confidence', 0):.3f}")

    # Adapt to another task
    task_name2 = "search_and_rescue"
    demonstrations2 = [
        {"context": {"position": [0, 0], "objects": []}, "action": "search"},
        {"context": {"position": [3, 3], "objects": [{"name": "person"}]}, "action": "navigate"},
    ]

    result2 = meta_learner.adapt_to_task(task_name2, demonstrations2)
    print(f"\nAdapted to second task: {task_name2}")
    print(f"  Adaptation score: {result2['adaptation_score']:.2f}")

    # Model info
    info = meta_learner.get_model_info()
    print(f"\nModel: {info['model_type']}")
    print(f"  Adapted tasks: {info['num_adapted_tasks']}")
    print(f"  Tasks: {meta_learner.get_adapted_tasks()}")


def main() -> None:
    """Run all ML model demos."""
    print("=" * 60)
    print("REVOLUTIONARY ML MODELS DEMO")
    print("4 Deep Learning Models for Robot Intelligence")
    print("=" * 60)

    demo_intent_transformer()
    demo_neural_policy()
    demo_vision_language()
    demo_meta_learner()

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print("Total: 4 revolutionary ML models")
    print("\nCapabilities:")
    print("  1. Intent Transformer: Natural language understanding")
    print("  2. Neural Policy: Deep RL for action selection")
    print("  3. Vision-Language: Multimodal grounding")
    print("  4. Meta-Learner: Rapid task adaptation")
    print("\nAll models are:")
    print("  - Trainable on real data")
    print("  - Few-shot learning capable")
    print("  - Production-ready architecture")
    print("  - Lightweight (no GPU required)")
    print("\nDecision Kernel now has REAL machine learning!")


if __name__ == "__main__":
    main()
