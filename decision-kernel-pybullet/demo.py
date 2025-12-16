"""PyBullet adapter demo - Minimal runnable example"""

from decision_kernel_pybullet.adapter import PyBulletAdapter

from brain.kernel import RobotBrainKernel


def main():
    print("=" * 60)
    print("Decision Kernel - PyBullet Demo")
    print("=" * 60)

    # Create adapter
    print("\n[1/4] Creating PyBullet adapter...")
    adapter = PyBulletAdapter()
    print("[OK] Adapter created")

    # Sense world
    print("\n[2/4] Sensing PyBullet simulation...")
    world_state = adapter.sense()
    print(f"[OK] WorldState: {len(world_state.objects)} objects")
    print(f"  Robot at: {world_state.robot_location}")
    print(f"  Objects: {[obj.name for obj in world_state.objects]}")

    # Process intent
    print("\n[3/4] Processing intent...")
    kernel = RobotBrainKernel(adapter=adapter)
    intent = "bring me the cube"
    print(f"  Intent: '{intent}'")

    plan = kernel.process(intent, world_state)
    print(f"[OK] Plan: {len(plan)} actions")

    # Execute
    print("\n[4/4] Executing in PyBullet...")
    for i, action in enumerate(plan, 1):
        print(f"  {i}. {action}")

    execution_report = adapter.execute(plan)
    print(f"\n[OK] {execution_report.message}")
    print(f"  Success: {execution_report.success}")

    print("\n" + "=" * 60)
    print("Demo complete! Decision Kernel ran on PyBullet.")
    print("=" * 60)


if __name__ == "__main__":
    main()
