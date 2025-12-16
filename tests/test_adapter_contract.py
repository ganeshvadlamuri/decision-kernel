"""Tests for Adapter contract conformance"""

from adapters.mock.mock_robot import MockRobot
from brain.execution.report import ExecutionReport
from brain.planner.actions import Action
from brain.world.state import WorldState


def test_adapter_has_sense():
    """Adapter must implement sense()"""
    adapter = MockRobot()
    assert hasattr(adapter, "sense")
    assert callable(adapter.sense)


def test_adapter_has_execute():
    """Adapter must implement execute()"""
    adapter = MockRobot()
    assert hasattr(adapter, "execute")
    assert callable(adapter.execute)


def test_adapter_has_capabilities():
    """Adapter must implement capabilities()"""
    adapter = MockRobot()
    assert hasattr(adapter, "capabilities")
    assert callable(adapter.capabilities)


def test_adapter_sense_returns_world_state():
    """sense() must return WorldState"""
    adapter = MockRobot()
    state = adapter.sense()
    assert isinstance(state, WorldState)
    assert hasattr(state, "timestamp")
    assert hasattr(state, "frame_id")


def test_adapter_execute_returns_report():
    """execute() must return ExecutionReport"""
    adapter = MockRobot()
    plan = [Action("navigate_to", location="kitchen")]
    report = adapter.execute(plan)
    assert isinstance(report, ExecutionReport)
    assert hasattr(report, "success")
    assert hasattr(report, "results")


def test_adapter_execute_empty_plan():
    """Adapter handles empty plan"""
    adapter = MockRobot()
    report = adapter.execute([])
    assert isinstance(report, ExecutionReport)
    assert report.success


def test_adapter_execute_records_results():
    """execute() records result for each action"""
    adapter = MockRobot()
    plan = [
        Action("navigate_to", location="kitchen"),
        Action("grasp", target="cup"),
    ]
    report = adapter.execute(plan)
    assert len(report.results) == 2
    assert report.results[0].action_index == 0
    assert report.results[1].action_index == 1


def test_adapter_capabilities_returns_dict():
    """capabilities() must return dict"""
    adapter = MockRobot()
    caps = adapter.capabilities()
    assert isinstance(caps, dict)


def test_adapter_capabilities_has_required_keys():
    """capabilities() should include standard keys"""
    adapter = MockRobot()
    caps = adapter.capabilities()
    assert "hardware" in caps
    assert "version" in caps


def test_mock_adapter_conformance():
    """MockRobot fully conforms to Adapter contract"""
    adapter = MockRobot()

    # Test sense
    state = adapter.sense()
    assert isinstance(state, WorldState)
    assert state.timestamp > 0

    # Test execute
    plan = [Action("test")]
    report = adapter.execute(plan)
    assert isinstance(report, ExecutionReport)
    assert len(report.results) == 1

    # Test capabilities
    caps = adapter.capabilities()
    assert isinstance(caps, dict)
    assert "supported_actions" in caps
