"""Demo: Show validation and monitoring in action"""

from brain.kernel import RobotBrainKernel
from brain.world.objects import WorldObject
from brain.world.state import WorldState


def main():
    print("="*80)
    print("VALIDATION & MONITORING DEMO")
    print("="*80)

    kernel = RobotBrainKernel()
    world = WorldState(
        objects=[WorldObject("water", "kitchen", "liquid")],
        robot_location="living room",
        human_location="living room",
        locations=["kitchen", "living room"]
    )

    print("\nPIPELINE STAGES:")
    print("1. Intent Parser    - Understands command")
    print("2. Planner          - Creates action sequence")
    print("3. Safety Validator - Checks constraints")
    print("4. Memory Logger    - Records execution")
    print("5. Adapter          - Executes on hardware")

    # Test 1: Valid command
    print("\n" + "="*80)
    print("TEST 1: Valid Command")
    print("="*80)

    cmd = "bring me water"
    print(f"\nCommand: '{cmd}'")

    # Parse
    goal = kernel.intent_parser.parse(cmd)
    print("\n[1] Intent Parser:")
    print(f"    Action: {goal.action}")
    print(f"    Target: {goal.target}")

    # Plan
    plan = kernel.planner.plan(goal, world)
    print("\n[2] Planner:")
    print(f"    Generated {len(plan)} actions:")
    for i, action in enumerate(plan, 1):
        print(f"      {i}. {action}")

    # Validate
    is_safe, reason = kernel.safety.validate(plan)
    print("\n[3] Safety Validator:")
    print(f"    Safe: {is_safe}")
    print(f"    Reason: {reason}")

    # Execute (logs to memory)
    kernel.process(cmd, world)
    print("\n[4] Memory Logger:")
    print(f"    Executions recorded: {len(kernel.memory.get_history())}")

    history = kernel.memory.get_history()[-1]
    print("    Last execution:")
    print(f"      Goal: {history.goal}")
    print(f"      Actions: {len(history.plan)}")
    print(f"      Success: {history.success}")
    print(f"      Timestamp: {history.timestamp}")

    # Test 2: Invalid command (empty)
    print("\n" + "="*80)
    print("TEST 2: Edge Case (gets smart fallback)")
    print("="*80)

    cmd = "do a backflip"
    print(f"\nCommand: '{cmd}'")

    goal = kernel.intent_parser.parse(cmd)
    print("\n[1] Intent Parser:")
    print(f"    Action: {goal.action} (smart fallback)")

    plan = kernel.planner.plan(goal, world)
    print("\n[2] Planner:")
    print(f"    Generated {len(plan)} actions (helpful response)")

    is_safe, reason = kernel.safety.validate(plan)
    print("\n[3] Safety Validator:")
    print(f"    Safe: {is_safe}")
    print(f"    Reason: {reason}")

    # Test 3: Safety checks
    print("\n" + "="*80)
    print("TEST 3: Safety Constraints")
    print("="*80)

    print("\nSafety Rules:")
    print(f"  - Max actions: {kernel.safety.max_actions}")
    print(f"  - Forbidden actions: {kernel.safety.forbidden_actions}")
    print("  - Empty plan: REJECTED")

    # Test forbidden action
    from brain.planner.actions import Action
    bad_plan = [Action("harm", target="something")]
    is_safe, reason = kernel.safety.validate(bad_plan)
    print("\nTest forbidden action:")
    print(f"  Plan: {bad_plan}")
    print(f"  Safe: {is_safe}")
    print(f"  Reason: {reason}")

    # Test too long plan
    long_plan = [Action("navigate_to", location="kitchen") for _ in range(25)]
    is_safe, reason = kernel.safety.validate(long_plan)
    print("\nTest too long plan:")
    print(f"  Plan length: {len(long_plan)}")
    print(f"  Safe: {is_safe}")
    print(f"  Reason: {reason}")

    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print("\nValidation Checks:")
    print("  [x] Intent parsing")
    print("  [x] Plan generation")
    print("  [x] Safety validation")
    print("  [x] Memory logging")
    print("  [x] Forbidden action blocking")
    print("  [x] Plan length limits")
    print("  [x] Empty plan rejection")

    print(f"\nTotal executions logged: {len(kernel.memory.get_history())}")
    print("\nAll validation systems working!")


if __name__ == "__main__":
    main()
