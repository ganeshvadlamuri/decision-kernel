"""Contract tests enforcing kernel API guarantees"""

from brain.kernel import RobotBrainKernel
from brain.planner.actions import Action
from brain.world.objects import WorldObject
from brain.world.state import WorldState


def test_kernel_has_process_method():
    """Kernel must expose process() method"""
    kernel = RobotBrainKernel()
    assert hasattr(kernel, "process")
    assert callable(kernel.process)


def test_kernel_process_signature():
    """process() must accept human_input: str and world_state: WorldState"""
    kernel = RobotBrainKernel()
    world = WorldState()

    # Should accept correct signature (use valid command)
    result = kernel.process("go to kitchen", world)
    assert isinstance(result, list)


def test_kernel_returns_action_list():
    """process() must return list of Action objects"""
    kernel = RobotBrainKernel()
    world = WorldState(
        objects=[WorldObject("water", "kitchen", "liquid")],
        human_location="living room",
    )

    plan = kernel.process("bring me water", world)

    assert isinstance(plan, list)
    assert len(plan) > 0
    for action in plan:
        assert isinstance(action, Action)
        assert hasattr(action, "action_type")


def test_safety_validation_before_memory():
    """Safety validation must occur before memory storage"""
    kernel = RobotBrainKernel()
    world = WorldState()

    # Valid plan should be stored
    kernel.process("go to kitchen", world)
    assert len(kernel.memory.get_history()) == 1

    # Invalid plan should not be stored
    initial_count = len(kernel.memory.get_history())
    try:
        # Create a plan that will fail safety (empty plan triggers "unknown" action)
        kernel.process("", world)
    except ValueError:
        pass

    # Memory should not have increased if safety failed
    assert len(kernel.memory.get_history()) == initial_count


def test_planner_output_conforms_to_action():
    """All planner outputs must be valid Action objects"""
    kernel = RobotBrainKernel()
    world = WorldState(
        objects=[WorldObject("cup", "kitchen", "container")],
        robot_location="living room",
        human_location="living room",
    )

    plan = kernel.process("bring me water", world)

    for action in plan:
        # Must be Action instance
        assert isinstance(action, Action)

        # Must have required fields
        assert isinstance(action.action_type, str)
        assert len(action.action_type) > 0

        # Optional fields must be str or None
        assert action.target is None or isinstance(action.target, str)
        assert action.location is None or isinstance(action.location, str)

        # Must be convertible to string
        assert isinstance(str(action), str)


def test_safety_validator_is_invoked():
    """Safety validator must be called during process()"""
    kernel = RobotBrainKernel()
    world = WorldState()

    # Track that safety was checked
    original_validate = kernel.safety.validate

    called = []

    def tracked_validate(plan):
        called.append(True)
        return original_validate(plan)

    kernel.safety.validate = tracked_validate

    kernel.process("go to kitchen", world)

    assert len(called) > 0, "Safety validator was not invoked"


def test_memory_stores_execution():
    """Memory must store goal and plan after successful execution"""
    kernel = RobotBrainKernel()
    world = WorldState()

    initial_count = len(kernel.memory.get_history())

    kernel.process("go to kitchen", world)

    history = kernel.memory.get_history()
    assert len(history) == initial_count + 1

    record = history[-1]
    assert hasattr(record, "goal")
    assert hasattr(record, "plan")
    assert hasattr(record, "timestamp")
    assert isinstance(record.plan, list)
