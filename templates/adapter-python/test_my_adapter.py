"""Example conformance test for adapter"""

from my_adapter import MyAdapter

from brain.execution.report import ExecutionReport
from brain.planner.actions import Action
from brain.world.state import WorldState


def test_adapter_sense():
    """Adapter sense() returns valid WorldState"""
    adapter = MyAdapter()
    state = adapter.sense()
    assert isinstance(state, WorldState)
    assert state.timestamp > 0


def test_adapter_execute():
    """Adapter execute() returns ExecutionReport"""
    adapter = MyAdapter()
    plan = [Action("navigate_to", location="kitchen")]
    report = adapter.execute(plan)
    assert isinstance(report, ExecutionReport)
    assert report.success


def test_adapter_capabilities():
    """Adapter capabilities() returns dict"""
    adapter = MyAdapter()
    caps = adapter.capabilities()
    assert isinstance(caps, dict)
    assert "supported_actions" in caps
    assert "hardware" in caps
