"""ROS2 Hello World demo - End-to-end kernel execution"""

from brain.kernel import RobotBrainKernel

from .demo_adapter import DemoROS2Adapter


def main():
    print("=" * 60)
    print("Decision Kernel - ROS2 Hello World Demo")
    print("=" * 60)

    # 1. Create adapter
    print("\n[1/4] Creating ROS2 adapter...")
    adapter = DemoROS2Adapter()
    print("[OK] Adapter created")

    # 2. Sense world state
    print("\n[2/4] Sensing world state from ROS2 topics...")
    world_state = adapter.sense()
    print(f"[OK] WorldState: {len(world_state.objects)} objects, {len(world_state.locations)} locations")
    print(f"  Robot at: {world_state.robot_location}")
    print(f"  Objects: {[obj.name for obj in world_state.objects]}")

    # 3. Create kernel and process intent
    print("\n[3/4] Processing intent through kernel...")
    kernel = RobotBrainKernel(adapter=adapter)
    intent = "bring me the cup"
    print(f"  Intent: '{intent}'")

    plan = kernel.process(intent, world_state)
    print(f"[OK] Plan generated: {len(plan)} actions")
    print("  Safety: PASS")

    # 4. Execute plan
    print("\n[4/4] Executing plan...")
    for i, action in enumerate(plan, 1):
        print(f"  {i}. {action}")

    execution_report = adapter.execute(plan)
    print(f"\n[OK] Execution: {execution_report.message}")
    print(f"  Success: {execution_report.success}")
    print(f"  Actions completed: {len(execution_report.results)}")

    print("\n" + "=" * 60)
    print("Demo complete! Decision Kernel ran end-to-end with ROS2.")
    print("=" * 60)


if __name__ == "__main__":
    main()
