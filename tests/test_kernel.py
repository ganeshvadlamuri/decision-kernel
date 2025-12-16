from brain.kernel import RobotBrainKernel
from brain.world.objects import WorldObject
from brain.world.state import WorldState


def test_kernel_process():
    kernel = RobotBrainKernel()
    world = WorldState(
        objects=[WorldObject("water", "kitchen", "liquid")],
        robot_location="living room",
        human_location="living room"
    )

    plan = kernel.process("bring me water", world)
    assert len(plan) > 0
    assert plan[0].action_type == "navigate_to"


def test_kernel_memory():
    kernel = RobotBrainKernel()
    world = WorldState()

    kernel.process("go to kitchen", world)
    history = kernel.memory.get_history()
    assert len(history) == 1
    assert history[0].success is True
