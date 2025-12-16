"""Conformance test runner"""

import importlib
import sys

from brain.execution.report import ExecutionReport
from brain.planner.actions import Action
from brain.world.state import WorldState


def load_adapter(import_path: str):
    """Load adapter class from import path (module.ClassName)"""
    if "." not in import_path:
        print(f"Error: Import path must be 'module.ClassName', got: {import_path}")
        return None

    module_name, class_name = import_path.rsplit(".", 1)

    try:
        module = importlib.import_module(module_name)
        adapter_class = getattr(module, class_name)
        return adapter_class()
    except Exception as e:
        print(f"Error loading adapter: {e}")
        return None


def test_adapter_has_methods(adapter) -> tuple[bool, str]:
    """Test adapter has required methods"""
    required = ["sense", "execute", "capabilities"]
    for method in required:
        if not hasattr(adapter, method):
            return False, f"Missing method: {method}"
        if not callable(getattr(adapter, method)):
            return False, f"Method not callable: {method}"
    return True, "All methods present"


def test_adapter_sense(adapter) -> tuple[bool, str]:
    """Test sense() returns valid WorldState"""
    try:
        state = adapter.sense()
        if not isinstance(state, WorldState):
            return False, f"sense() must return WorldState, got {type(state)}"
        if not hasattr(state, "timestamp"):
            return False, "WorldState missing timestamp"
        if state.timestamp <= 0:
            return False, "WorldState timestamp must be positive"
        return True, "sense() returns valid WorldState"
    except Exception as e:
        return False, f"sense() raised exception: {e}"


def test_adapter_execute(adapter) -> tuple[bool, str]:
    """Test execute() returns ExecutionReport"""
    try:
        plan = [Action("test_action")]
        report = adapter.execute(plan)
        if not isinstance(report, ExecutionReport):
            return False, f"execute() must return ExecutionReport, got {type(report)}"
        if not hasattr(report, "success"):
            return False, "ExecutionReport missing success field"
        return True, "execute() returns valid ExecutionReport"
    except Exception as e:
        return False, f"execute() raised exception: {e}"


def test_adapter_capabilities(adapter) -> tuple[bool, str]:
    """Test capabilities() returns dict"""
    try:
        caps = adapter.capabilities()
        if not isinstance(caps, dict):
            return False, f"capabilities() must return dict, got {type(caps)}"
        if "supported_actions" not in caps:
            return False, "capabilities() missing 'supported_actions'"
        if "hardware" not in caps:
            return False, "capabilities() missing 'hardware'"
        return True, "capabilities() returns valid dict"
    except Exception as e:
        return False, f"capabilities() raised exception: {e}"


def run_conformance(adapter_path: str) -> bool:
    """Run conformance tests on adapter"""
    print(f"Loading adapter: {adapter_path}")
    adapter = load_adapter(adapter_path)

    if adapter is None:
        return False

    print(f"Adapter loaded: {adapter.__class__.__name__}\n")

    tests = [
        ("Method presence", test_adapter_has_methods),
        ("sense() contract", test_adapter_sense),
        ("execute() contract", test_adapter_execute),
        ("capabilities() contract", test_adapter_capabilities),
    ]

    results = []
    for name, test_func in tests:
        passed, msg = test_func(adapter)
        results.append((name, passed, msg))
        status = "[PASS]" if passed else "[FAIL]"
        print(f"{status}: {name}")
        if not passed:
            print(f"  {msg}")

    print("\n" + "=" * 50)
    passed_count = sum(1 for _, passed, _ in results if passed)
    total_count = len(results)
    print(f"Results: {passed_count}/{total_count} tests passed")

    if passed_count == total_count:
        print("[PASS] Adapter is CONFORMANT")
        return True
    else:
        print("[FAIL] Adapter is NOT CONFORMANT")
        return False


def main():
    """CLI entry point"""
    if len(sys.argv) < 2:
        print("Usage: python -m decision_kernel_conformance <module.ClassName>")
        print("Example: python -m decision_kernel_conformance adapters.mock.mock_robot.MockRobot")
        return 1

    adapter_path = sys.argv[1]
    success = run_conformance(adapter_path)
    return 0 if success else 1
