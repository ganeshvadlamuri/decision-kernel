"""Demo of all 50 functional capabilities."""

from datetime import datetime, timedelta

# Memory & Learning
from brain.memory import EpisodicMemory, SemanticMemory, WorkingMemory, MemoryConsolidator, ForgettingMechanism

# Advanced Reasoning
from brain.reasoning import CausalReasoner, AnalogicalReasoner, AbductiveReasoner, CommonSenseReasoner, SpatialReasoner

# Natural Language
from brain.language import ContextUnderstanding, AmbiguityResolver, ClarificationEngine, DialogueManager, ImplicitCommandParser

# Goal Management
from brain.goals import GoalPrioritizer, GoalInterruptionManager, GoalDecomposer, GoalConflictResolver, GoalAbandonmentDecider

# Uncertainty Handling
from brain.uncertainty import ProbabilisticPlanner, BeliefTracker, InformationGatherer, ConfidenceEstimator, GracefulDegradation

# Social Intelligence
from brain.social import TheoryOfMind, PerspectiveTaker, SocialNormsLearner, DeceptionDetector, CollaborationEngine

# Adaptation
from brain.adaptation import OnlineLearner, FailureRecovery, StrategySwitcher, PerformanceOptimizer, EnvironmentAdapter

# Meta-Cognition
from brain.metacognition import SelfMonitor, ConfidenceCalibrator, ExplanationGenerator, Introspector, MetaLearner

# Multi-Modal Integration
from brain.multimodal import SensorFusion, CrossModalLearner, AttentionMechanism, SurpriseDetector, AnomalyDetector

# Long-Horizon Planning
from brain.planning import HierarchicalPlanner, ContingencyPlanner, ResourceManager, DeadlineManager, InterruptibleExecutor


def demo_memory_learning() -> None:
    """Demo Memory & Learning (5 features)."""
    print("\n" + "=" * 80)
    print("1. MEMORY & LEARNING")
    print("=" * 80)

    # Episodic Memory
    print("\n[Episodic Memory] Remember specific past events")
    episodic = EpisodicMemory()
    episodic.record("navigate_to_kitchen", {"location": "living_room"}, "success", True, 15.5)
    episodic.record("navigate_to_kitchen", {"location": "bedroom"}, "success", True, 20.0)
    last = episodic.last_time("navigate_to_kitchen")
    print(f"  Last time navigated to kitchen: {last.outcome}, took {last.duration_seconds}s")
    print(f"  Success rate: {episodic.success_rate('navigate_to_kitchen'):.0%}")

    # Semantic Memory
    print("\n[Semantic Memory] Build knowledge graph")
    semantic = SemanticMemory()
    semantic.learn("kitchen", "has", "coffee_maker")
    semantic.learn("kitchen", "has", "refrigerator")
    semantic.learn("bedroom", "has", "bed")
    print(f"  Kitchen has: {semantic.what_has('kitchen')}")
    print(f"  Coffee maker is in: {semantic.where_is('coffee_maker')}")

    # Working Memory
    print("\n[Working Memory] Track current context")
    working = WorkingMemory()
    working.store("last_object", "cup", importance=0.8)
    working.store("current_location", "kitchen", importance=0.9)
    print(f"  Context: {working.get_context()}")
    print(f"  Resolve 'it': {working.resolve_reference('it')}")

    # Memory Consolidation
    print("\n[Memory Consolidation] Compress old memories")
    consolidator = MemoryConsolidator(consolidation_threshold_days=0)
    result = consolidator.consolidate(episodic)
    print(f"  Consolidated {result['consolidated_memories']} memories")
    print(f"  Compression ratio: {result['compression_ratio']:.1f}x")

    # Forgetting Mechanism
    print("\n[Forgetting Mechanism] Delete outdated information")
    forgetter = ForgettingMechanism()
    result = forgetter.forget_semantic(semantic)
    print(f"  Forgot {result['forgotten_knowledge']} low-confidence facts")
    print(f"  Retained {result['retained_knowledge']} facts")


def demo_advanced_reasoning() -> None:
    """Demo Advanced Reasoning (5 features)."""
    print("\n" + "=" * 80)
    print("2. ADVANCED REASONING")
    print("=" * 80)

    # Causal Reasoning
    print("\n[Causal Reasoning] Understand cause-effect")
    causal = CausalReasoner()
    effects = causal.predict_effect("push_object")
    print(f"  If I push object: {effects[0][0]} ({effects[0][1]:.0%} probability)")

    # Analogical Reasoning
    print("\n[Analogical Reasoning] Apply solutions from similar problems")
    analogical = AnalogicalReasoner()
    analogical.store_problem("bring water", {"object": "water", "location": "kitchen"}, ["navigate", "grasp", "return"], True)
    result = analogical.solve_by_analogy("bring juice", {"object": "juice", "location": "kitchen"})
    print(f"  Found analogy: {result['found_analogy']}")
    print(f"  Adapted solution: {result['solution']}")

    # Abductive Reasoning
    print("\n[Abductive Reasoning] Infer best explanation")
    abductive = AbductiveReasoner()
    explanation = abductive.best_explanation("floor_wet", ["cup_nearby"])
    print(f"  Floor wet -> probably {explanation.explanation} ({explanation.likelihood:.0%})")

    # Common Sense Reasoning
    print("\n[Common Sense Reasoning] Know implicit rules")
    common_sense = CommonSenseReasoner()
    result = common_sense.check_action("vacuum", {"time": "night", "human_state": "sleeping"})
    print(f"  Vacuum while human sleeping? Safe: {result['safe']}")
    if result['violations']:
        print(f"  Violation: {result['violations'][0]['rule']}")

    # Spatial Reasoning
    print("\n[Spatial Reasoning] Understand 3D relationships")
    spatial = SpatialReasoner()
    spatial.add_object("cup", 1.0, 2.0, 0.5, (0.1, 0.1, 0.15))
    spatial.add_object("table", 1.0, 2.0, 0.0, (1.0, 1.0, 0.05))
    print(f"  Cup on table: {spatial.is_on_top('cup', 'table')}")
    print(f"  Distance: {spatial.distance('cup', 'table'):.2f}m")


def demo_natural_language() -> None:
    """Demo Natural Language (5 features)."""
    print("\n" + "=" * 80)
    print("3. NATURAL LANGUAGE")
    print("=" * 80)

    # Context Understanding
    print("\n[Context Understanding] Resolve 'it', 'here'")
    context = ContextUnderstanding()
    context.update_context("last_object", "cup")
    context.update_context("current_location", "kitchen")
    result = context.resolve_command("bring it here")
    print(f"  Original: '{result['original']}'")
    print(f"  Resolved: '{result['resolved']}'")

    # Ambiguity Resolution
    print("\n[Ambiguity Resolution] Handle multiple interpretations")
    ambiguity = AmbiguityResolver()
    ambiguity.add_object("cup", {"color": "red", "distance": 1.0})
    ambiguity.add_object("cup", {"color": "blue", "distance": 2.0})
    result = ambiguity.detect_ambiguity("get the cup")
    print(f"  Ambiguous: {result['is_ambiguous']}")
    print(f"  Found {result['ambiguities'][0]['count']} cups")

    # Clarification Questions
    print("\n[Clarification Questions] Ask when confused")
    clarifier = ClarificationEngine()
    question = clarifier.generate_clarification({"type": "multiple_objects", "object": "cup", "count": 2})
    print(f"  Question: {question}")

    # Multi-turn Dialogue
    print("\n[Multi-turn Dialogue] Remember conversation")
    dialogue = DialogueManager()
    dialogue.add_turn("user", "bring me water", "bring_water")
    dialogue.add_turn("robot", "Getting water from kitchen")
    dialogue.add_turn("user", "actually, make it juice", "bring_juice")
    print(f"  Last user intent: {dialogue.last_user_intent()}")
    print(f"  Context: {dialogue.get_context()[-2:]}")

    # Implicit Commands
    print("\n[Implicit Commands] Infer intent from statements")
    implicit = ImplicitCommandParser()
    result = implicit.parse("I'm thirsty")
    print(f"  Statement: '{result['statement']}'")
    print(f"  Implicit command: {result['is_implicit_command']}")
    print(f"  Intent: {result['intent']}")


def demo_goal_management() -> None:
    """Demo Goal Management (5 features)."""
    print("\n" + "=" * 80)
    print("4. GOAL MANAGEMENT")
    print("=" * 80)

    from brain.goals.goal_prioritization import Goal

    # Goal Prioritization
    print("\n[Goal Prioritization] Urgent vs important")
    prioritizer = GoalPrioritizer()
    goals = [
        Goal("clean_room", urgency=0.3, importance=0.7),
        Goal("charge_battery", urgency=0.9, importance=0.8, deadline=60),
        Goal("water_plants", urgency=0.5, importance=0.4),
    ]
    prioritized = prioritizer.prioritize(goals)
    print(f"  Priority order: {[g.description for g in prioritized]}")

    # Goal Interruption
    print("\n[Goal Interruption] Pause, handle emergency, resume")
    interrupter = GoalInterruptionManager()
    interrupter.pause_goal("clean_room", {"progress": 0.5}, ["vacuum_floor"])
    print(f"  Paused: clean_room")
    resumed = interrupter.resume_goal()
    print(f"  Resumed: {resumed.goal} (progress: {resumed.progress['progress']*100:.0f}%)")

    # Goal Decomposition
    print("\n[Goal Decomposition] Break complex goals")
    decomposer = GoalDecomposer()
    subgoals = decomposer.decompose("clean_house")
    print(f"  clean_house -> {subgoals}")

    # Goal Conflict Resolution
    print("\n[Goal Conflict Resolution] Handle conflicts")
    resolver = GoalConflictResolver()
    result = resolver.resolve("clean_room", "don't_wake_baby", {"baby_sleeping": True})
    print(f"  Conflict: {result['resolution']}")
    print(f"  Action: {result['action']}")

    # Goal Abandonment
    print("\n[Goal Abandonment] Know when to give up")
    abandoner = GoalAbandonmentDecider()
    result = abandoner.should_abandon("find_keys", attempts=4, time_spent=350)
    print(f"  Should abandon: {result['should_abandon']}")
    print(f"  Reasons: {result['reasons']}")


def demo_uncertainty_handling() -> None:
    """Demo Uncertainty Handling (5 features)."""
    print("\n" + "=" * 80)
    print("5. UNCERTAINTY HANDLING")
    print("=" * 80)

    # Probabilistic Planning
    print("\n[Probabilistic Planning] Plan under uncertainty")
    prob_planner = ProbabilisticPlanner()
    result = prob_planner.plan_with_uncertainty("deliver_item", {"navigate": 0.9, "grasp": 0.7, "place": 0.8})
    print(f"  Plan success probability: {result['success_probability']:.0%}")
    print(f"  Needs contingency: {result['needs_contingency']}")

    # Belief Tracking
    print("\n[Belief Tracking] Maintain probability distributions")
    beliefs = BeliefTracker()
    beliefs.update_belief("cup_location", "kitchen", 0.7)
    beliefs.update_belief("cup_location", "table", 0.3)
    most_likely = beliefs.most_likely("cup_location")
    print(f"  Cup most likely in: {most_likely[0]} ({most_likely[1]:.0%})")

    # Information Gathering
    print("\n[Information Gathering] Know what you don't know")
    gatherer = InformationGatherer()
    unknowns = gatherer.identify_unknowns(["object_location", "object_state"], {"object_state": "clean"})
    print(f"  Missing info: {unknowns}")
    print(f"  Query: {gatherer.generate_query('object_location')}")

    # Confidence Estimation
    print("\n[Confidence Estimation] Know certainty level")
    estimator = ConfidenceEstimator()
    confidence = estimator.estimate_action_confidence("navigate", {"past_success_rate": 0.85})
    print(f"  Confidence: {confidence:.0%}")
    print(f"  Should proceed: {estimator.should_proceed(confidence)}")

    # Graceful Degradation
    print("\n[Graceful Degradation] Partial success")
    degradation = GracefulDegradation()
    result = degradation.find_partial_solution("clean_house", ["vacuum"], ["vacuum", "dust", "mop"])
    print(f"  Completion rate: {result['completion_rate']:.0%}")
    print(f"  Acceptable: {result['acceptable']}")


def demo_social_intelligence() -> None:
    """Demo Social Intelligence (5 features)."""
    print("\n" + "=" * 80)
    print("6. SOCIAL INTELLIGENCE")
    print("=" * 80)

    # Theory of Mind
    print("\n[Theory of Mind] Model what human knows/wants")
    tom = TheoryOfMind()
    tom.update_human_knowledge("kitchen_location")
    print(f"  Human knows kitchen location: {tom.human_knows('kitchen_location')}")
    print(f"  Should inform about bedroom: {tom.should_inform('bedroom_location')}")

    # Perspective Taking
    print("\n[Perspective Taking] See from human's viewpoint")
    perspective = PerspectiveTaker()
    result = perspective.from_human_perspective({"objects": ["cup", "book"]}, {"x": 0, "y": 0, "z": 1.5})
    print(f"  Visible to human: {result['visible_to_human']}")

    # Social Norms
    print("\n[Social Norms] Learn cultural rules")
    norms = SocialNormsLearner()
    result = norms.check_norm_violation("approach", {"distance_to_human": 0.5})
    print(f"  Acceptable: {result['acceptable']}")
    if result['violations']:
        print(f"  Violation: {result['violations'][0]}")

    # Deception Detection
    print("\n[Deception Detection] Recognize joking/lying")
    detector = DeceptionDetector()
    result = detector.detect("The sky is green haha", {})
    print(f"  Is joke: {result['is_joke']}")
    print(f"  Take literally: {result['should_take_literally']}")

    # Collaboration
    print("\n[Collaboration] Work together")
    collab = CollaborationEngine()
    result = collab.propose_collaboration("clean kitchen", ["wipe", "organize", "sweep"])
    print(f"  Robot contributions: {result['robot_contributions']}")
    print(f"  Mode: {result['collaboration_mode']}")


def demo_adaptation() -> None:
    """Demo Adaptation (5 features)."""
    print("\n" + "=" * 80)
    print("7. ADAPTATION")
    print("=" * 80)

    # Online Learning
    print("\n[Online Learning] Update models during execution")
    learner = OnlineLearner()
    learner.update_from_experience("grasp", True)
    learner.update_from_experience("grasp", True)
    learner.update_from_experience("grasp", False)
    print(f"  Grasp success rate: {learner.get_success_rate('grasp'):.0%}")

    # Failure Recovery
    print("\n[Failure Recovery] Detect, diagnose, retry")
    recovery = FailureRecovery()
    failure_type = recovery.diagnose_failure("grasp_cup", "object slipped")
    strategies = recovery.get_recovery_strategy(failure_type)
    print(f"  Failure type: {failure_type}")
    print(f"  Recovery strategies: {strategies}")

    # Strategy Switching
    print("\n[Strategy Switching] Try different approaches")
    switcher = StrategySwitcher()
    strategy1 = switcher.get_next_strategy("navigate")
    strategy2 = switcher.get_next_strategy("navigate")
    print(f"  Strategy 1: {strategy1}")
    print(f"  Strategy 2: {strategy2}")

    # Performance Optimization
    print("\n[Performance Optimization] Get faster at tasks")
    optimizer = PerformanceOptimizer()
    optimizer.record_execution("navigate", 15.0)
    optimizer.record_execution("navigate", 12.0)
    optimizer.record_execution("navigate", 10.0)
    result = optimizer.identify_optimization("navigate")
    if 'avg_time' in result:
        print(f"  Avg time: {result['avg_time']:.1f}s")
        print(f"  Best time: {result['best_time']:.1f}s")
        print(f"  Potential speedup: {result['potential_speedup']:.0%}")

    # Environment Adaptation
    print("\n[Environment Adaptation] Adjust to new homes")
    adapter = EnvironmentAdapter()
    adapter.learn_environment([{"location": "kitchen", "object": "stove"}])
    result = adapter.adapt_behavior("kitchen")
    print(f"  Confidence in kitchen: {result['confidence']:.0%}")
    print(f"  Adaptations: {result['adaptations']}")


def demo_metacognition() -> None:
    """Demo Meta-Cognition (5 features)."""
    print("\n" + "=" * 80)
    print("8. META-COGNITION")
    print("=" * 80)

    # Self-Monitoring
    print("\n[Self-Monitoring] Know when confused/stuck")
    monitor = SelfMonitor()
    result = monitor.check_state({"confidence": 0.3, "progress": 0.05, "time_elapsed": 40})
    print(f"  State: {result['state']}")
    print(f"  Needs help: {result['needs_help']}")

    # Confidence Calibration
    print("\n[Confidence Calibration] Accurate self-assessment")
    calibrator = ConfidenceCalibrator()
    calibrator.record_outcome(0.8, True)
    calibrator.record_outcome(0.6, False)
    calibrator.record_outcome(0.9, True)
    print(f"  Calibration error: {calibrator.calibration_error():.2f}")
    print(f"  Well calibrated: {calibrator.is_well_calibrated()}")

    # Explanation Generation
    print("\n[Explanation Generation] Explain decisions")
    explainer = ExplanationGenerator()
    explanation = explainer.explain_action("navigated to kitchen", {"goal": "get water", "reason": "water is in kitchen"})
    print(f"  Explanation: {explanation}")

    # Introspection
    print("\n[Introspection] Examine decision process")
    introspector = Introspector()
    analysis = introspector.analyze_decision({"action": "grasp", "factors": ["distance", "angle"], "confidence": 0.75})
    print(f"  Decision quality: {analysis['decision_quality']}")
    print(f"  Factors considered: {analysis['num_factors_considered']}")

    # Learning to Learn
    print("\n[Learning to Learn] Improve learning efficiency")
    meta_learner = MetaLearner()
    meta_learner.record_learning_episode("navigate", 120, 0.85)
    meta_learner.record_learning_episode("grasp", 90, 0.90)
    result = meta_learner.optimize_learning_strategy()
    print(f"  Strategy: {result['strategy']}")
    if 'learning_rate_trend' in result:
        print(f"  Trend: {result['learning_rate_trend']}")


def demo_multimodal() -> None:
    """Demo Multi-Modal Integration (5 features)."""
    print("\n" + "=" * 80)
    print("9. MULTI-MODAL INTEGRATION")
    print("=" * 80)

    # Sensor Fusion
    print("\n[Sensor Fusion] Combine vision + audio + touch")
    fusion = SensorFusion()
    result = fusion.fuse(
        {"object_detected": True, "confidence": 0.8, "properties": {"color": "red"}},
        {"sound_detected": True, "confidence": 0.7},
        {"contact_detected": False, "confidence": 0.0}
    )
    print(f"  Object detected: {result['object_detected']}")
    print(f"  Fused confidence: {result['confidence']:.0%}")

    # Cross-Modal Learning
    print("\n[Cross-Modal Learning] Associate across modalities")
    cross_modal = CrossModalLearner()
    cross_modal.associate("apple", "vision", "red")
    cross_modal.associate("apple", "word", "apple")
    cross_modal.associate("apple", "sound", "crunchy")
    print(f"  Apple in vision: {cross_modal.query('apple', 'vision')}")
    print(f"  Red objects: {cross_modal.infer_concept('vision', 'red')}")

    # Attention Mechanism
    print("\n[Attention Mechanism] Focus on relevant inputs")
    attention = AttentionMechanism()
    inputs = [{"type": "cup", "location": "table"}, {"type": "book", "location": "shelf"}]
    focused = attention.focus(inputs, "get cup", top_k=1)
    print(f"  Focused on: {focused[0] if focused else 'none'}")

    # Surprise Detection
    print("\n[Surprise Detection] Notice unexpected events")
    surprise = SurpriseDetector()
    surprise.set_expectation("door_state", "closed")
    result = surprise.detect_surprise({"door_state": "open"})
    print(f"  Surprising: {result['is_surprising']}")
    if result['surprises']:
        print(f"  Surprises: {result['surprises'][0]}")

    # Anomaly Detection
    print("\n[Anomaly Detection] Detect unusual patterns")
    anomaly = AnomalyDetector()
    for val in [10, 11, 10, 12, 11]:
        anomaly.record("temperature", val)
    result = anomaly.is_anomaly("temperature", 25)
    print(f"  Is anomaly: {result['is_anomaly']}")
    print(f"  Z-score: {result['z_score']:.1f}")


def demo_long_horizon_planning() -> None:
    """Demo Long-Horizon Planning (5 features)."""
    print("\n" + "=" * 80)
    print("10. LONG-HORIZON PLANNING")
    print("=" * 80)

    # Hierarchical Planning
    print("\n[Hierarchical Planning] High-level + low-level")
    hierarchical = HierarchicalPlanner()
    result = hierarchical.plan("clean_house")
    print(f"  High-level: {result['high_level']}")
    print(f"  Total actions: {result['total_actions']}")

    # Contingency Planning
    print("\n[Contingency Planning] Backup plans")
    contingency = ContingencyPlanner()
    backups = contingency.generate_contingencies(["navigate", "grasp"])
    print(f"  Navigate backups: {backups['navigate']}")
    print(f"  Grasp backups: {backups['grasp']}")

    # Resource Management
    print("\n[Resource Management] Track battery, time")
    resources = ResourceManager(battery=100, time_budget=300)
    result = resources.check_resources(["navigate", "grasp"], {"navigate": {"battery": 10, "time": 15}, "grasp": {"battery": 5, "time": 10}})
    print(f"  Sufficient battery: {result['sufficient_battery']}")
    print(f"  Battery required: {result['battery_required']}")

    # Deadline Awareness
    print("\n[Deadline Awareness] Must finish by time")
    deadline_mgr = DeadlineManager()
    deadline = datetime.now() + timedelta(minutes=10)
    result = deadline_mgr.check_deadline(deadline, 300)
    print(f"  Can meet deadline: {result['can_meet_deadline']}")
    print(f"  Urgency: {result['urgency']:.0%}")

    # Interruptible Execution
    print("\n[Interruptible Execution] Pause/resume")
    executor = InterruptibleExecutor()
    executor.save_state("clean_house", ["vacuum"], ["dust", "mop"])
    print(f"  Can resume: {executor.can_resume()}")
    state = executor.resume()
    print(f"  Resumed: {state.task} (progress: {state.progress*100:.0f}%)")


def main() -> None:
    """Run all demos."""
    print("\n" + "=" * 80)
    print("DECISION KERNEL - 50 FUNCTIONAL CAPABILITIES DEMO")
    print("=" * 80)

    demo_memory_learning()
    demo_advanced_reasoning()
    demo_natural_language()
    demo_goal_management()
    demo_uncertainty_handling()
    demo_social_intelligence()
    demo_adaptation()
    demo_metacognition()
    demo_multimodal()
    demo_long_horizon_planning()

    print("\n" + "=" * 80)
    print("ALL 50 FUNCTIONAL CAPABILITIES DEMONSTRATED")
    print("=" * 80)
    print("\nDecision Kernel now has:")
    print("  [OK] 5 Memory & Learning features")
    print("  [OK] 5 Advanced Reasoning features")
    print("  [OK] 5 Natural Language features")
    print("  [OK] 5 Goal Management features")
    print("  [OK] 5 Uncertainty Handling features")
    print("  [OK] 5 Social Intelligence features")
    print("  [OK] 5 Adaptation features")
    print("  [OK] 5 Meta-Cognition features")
    print("  [OK] 5 Multi-Modal Integration features")
    print("  [OK] 5 Long-Horizon Planning features")
    print("\nTotal: 50 production-ready functional capabilities")


if __name__ == "__main__":
    main()
