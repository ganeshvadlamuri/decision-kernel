"""Demo of all 10 creative thinking features."""

from brain.creativity import (
    AnalogicalReasoning,
    CausalReasoningCreative,
    ConceptualBlending,
    ConstraintRelaxation,
    GoalReframing,
    HypothesisTesting,
    MetaStrategy,
    PerspectiveShifting,
    SerendipityEngine,
    ToolImprovisation,
)


def demo_analogical_reasoning() -> None:
    """Demo analogical reasoning."""
    print("\n=== 1. ANALOGICAL REASONING ===")
    print("Solve new problems by adapting past solutions\n")

    reasoner = AnalogicalReasoning()

    problem = {
        "goal": "transport",
        "context": ["book", "library"],
        "constraints": ["graspable"],
        "target": "book",
        "location": "library",
    }

    result = reasoner.solve_novel_problem(problem)
    print("Problem: Transport book to library")
    print(f"Solution found: {result['success']}")
    print(f"Adapted from: {result.get('source_case', 'N/A')}")
    print(f"Confidence: {result.get('confidence', 0):.0%}")
    print(f"Actions: {len(result.get('solution', []))} steps")


def demo_constraint_relaxation() -> None:
    """Demo constraint relaxation."""
    print("\n=== 2. CONSTRAINT RELAXATION ===")
    print("Find creative solutions by relaxing constraints\n")

    relaxer = ConstraintRelaxation()

    goal = {"type": "transport", "object": "package", "source": "A", "destination": "B"}
    constraints = [
        {"type": "time", "value": 30},
        {"type": "cost", "value": 5.0},
        {"type": "max_actions", "value": 3},
    ]

    result = relaxer.plan_with_relaxation(goal, constraints)
    print("Goal: Transport package from A to B")
    print(f"Success: {result['success']}")
    print(f"Message: {result['message']}")
    print(f"Relaxed: {len(result['relaxed_constraints'])} constraints")


def demo_tool_improvisation() -> None:
    """Demo tool improvisation."""
    print("\n=== 3. TOOL IMPROVISATION ===")
    print("Use objects in unexpected ways\n")

    improviser = ToolImprovisation()

    available = [
        {"name": "card", "properties": ["rigid", "sharp"]},
        {"name": "string", "properties": ["flexible", "long"]},
        {"name": "book", "properties": ["rigid", "known_size"]},
    ]

    result = improviser.find_alternative_tool("cut", available)
    print("Need: Cut paper (no scissors available)")
    print(f"Found alternative: {result['success']}")
    if result["success"]:
        alt = result["alternative"]
        print(f"Use: {alt['object']}")
        print(f"Method: {alt['method']}")
        print(f"Confidence: {alt['confidence']:.0%}")
        print(f"Improvised: {alt['improvised']}")


def demo_goal_reframing() -> None:
    """Demo goal reframing."""
    print("\n=== 4. GOAL REFRAMING ===")
    print("Reinterpret impossible goals\n")

    reframer = GoalReframing()

    goal = {"description": "bring water from Mars"}

    result = reframer.reframe_impossible_goal(goal)
    print(f"Original goal: {goal['description']}")
    print(f"Reframed: {result['reframed']}")
    if result["reframed"]:
        print(f"Underlying need: {result['underlying_need']}")
        print(f"Alternatives found: {len(result['alternatives'])}")
        if result["alternatives"]:
            best = result["alternatives"][0]
            print(f"Best alternative: {best['goal']}")
            print(f"Feasibility: {best['feasibility']:.0%}")


def demo_causal_reasoning() -> None:
    """Demo causal reasoning."""
    print("\n=== 5. CAUSAL REASONING ===")
    print("Predict outcomes and identify risks\n")

    reasoner = CausalReasoningCreative()

    action = {"type": "push", "target": "cup"}
    context = {"object_near_edge": True, "object_fragile": True}

    result = reasoner.predict_outcome(action, context)
    print("Action: Push cup near edge")
    print(f"Causal chain: {len(result['causal_chain'])} events")
    print(f"Risks identified: {len(result['risks'])}")
    if result["risks"]:
        risk = result["risks"][0]
        print(f"  - {risk['risk']}")
        print(f"  - Severity: {risk['severity']}")
        print(f"  - Mitigation: {risk['mitigation']}")


def demo_meta_strategy() -> None:
    """Demo meta-strategy selection."""
    print("\n=== 6. META-STRATEGY SELECTION ===")
    print("Choose right thinking approach\n")

    meta = MetaStrategy()

    problems = [
        {"description": "bring me water", "context": {"seen_before": True}},
        {"description": "impossible task from Mars", "context": {}},
        {"description": "unclear what you mean", "context": {"clarity": "low"}},
    ]

    for prob in problems:
        result = meta.select_strategy(prob)
        print(f"Problem: {prob['description']}")
        print(f"Class: {result['problem_class']}")
        print(f"Strategy: {result['selected_strategy']}")
        print()


def demo_hypothesis_testing() -> None:
    """Demo hypothesis testing."""
    print("\n=== 7. HYPOTHESIS TESTING ===")
    print("Scientific method for unknowns\n")

    tester = HypothesisTesting()

    situation = {"type": "object_not_found", "object": "keys", "usual_location": "table"}

    result = tester.explore_unknown(situation)
    print("Situation: Keys not found")
    print(f"Success: {result['success']}")
    print(f"Experiments run: {result['experiments_run']}")
    if result["success"]:
        print(f"Best hypothesis: {result['best_hypothesis']['hypothesis']}")
        print(f"Confidence: {result['confidence']:.0%}")


def demo_perspective_shifting() -> None:
    """Demo perspective shifting."""
    print("\n=== 8. PERSPECTIVE SHIFTING ===")
    print("View problems from multiple angles\n")

    shifter = PerspectiveShifting()

    problem = {"description": "clean the room efficiently"}

    result = shifter.solve_from_multiple_views(problem)
    print(f"Problem: {problem['description']}")
    print(f"Perspectives considered: {result['perspectives_considered']}")
    print(f"Best approach: {result['best_solution']['primary_perspective']}")
    print(f"Score: {result['best_solution']['overall_score']:.2f}")


def demo_serendipity_engine() -> None:
    """Demo serendipity engine."""
    print("\n=== 9. SERENDIPITY ENGINE ===")
    print("Notice unexpected opportunities\n")

    engine = SerendipityEngine()

    state = {
        "location": "kitchen",
        "current_goal": "get water",
        "objects": [
            {"name": "dirty_dish", "state": "dirty"},
            {"name": "full_trash", "state": "full"},
        ],
    }

    result = engine.detect_opportunities(state)
    print("Current: Getting water in kitchen")
    print(f"Opportunities found: {result['opportunities_found']}")
    for opp in result["opportunities"]:
        print(f"  - {opp['description']}")
        print(f"    Priority: {opp['priority']}, Time: {opp['estimated_time']}s")


def demo_conceptual_blending() -> None:
    """Demo conceptual blending."""
    print("\n=== 10. CONCEPTUAL BLENDING ===")
    print("Combine concepts to create new ideas\n")

    blender = ConceptualBlending()

    result = blender.blend_concepts("vacuum_cleaner", "lawn_mower")
    print("Blending: vacuum_cleaner + lawn_mower")
    print(f"Success: {result['success']}")
    if result["success"]:
        concept = result["new_concept"]
        print(f"New concept: {concept['name']}")
        print(f"Novelty: {concept['novelty_score']:.0%}")
        print(f"Capabilities: {len(concept['capabilities'])}")
        print("Applications:")
        for app in concept["practical_applications"]:
            print(f"  - {app}")


def main() -> None:
    """Run all creative thinking demos."""
    print("=" * 60)
    print("CREATIVE THINKING FEATURES DEMO")
    print("10 Features for Out-of-the-Box Problem Solving")
    print("=" * 60)

    demo_analogical_reasoning()
    demo_constraint_relaxation()
    demo_tool_improvisation()
    demo_goal_reframing()
    demo_causal_reasoning()
    demo_meta_strategy()
    demo_hypothesis_testing()
    demo_perspective_shifting()
    demo_serendipity_engine()
    demo_conceptual_blending()

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print("Total: 10 creative thinking features")
    print("All features demonstrated successfully!")
    print("\nThese features enable robots to:")
    print("  - Adapt past solutions to new problems")
    print("  - Find creative workarounds")
    print("  - Improvise with available tools")
    print("  - Reframe impossible goals")
    print("  - Predict consequences")
    print("  - Choose right thinking strategy")
    print("  - Test hypotheses scientifically")
    print("  - View problems from multiple angles")
    print("  - Notice unexpected opportunities")
    print("  - Blend concepts for innovation")


if __name__ == "__main__":
    main()
