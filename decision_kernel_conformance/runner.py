"""Conformance test runner"""

import hashlib
import importlib
import json
import sys
from datetime import datetime
from pathlib import Path

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


def generate_certificate(adapter_path: str, results: list, adapter_class_name: str, output_dir: str = "certificates"):
    """Generate conformance certificate"""
    timestamp = datetime.utcnow().isoformat() + "Z"
    passed_count = sum(1 for _, passed, _ in results if passed)
    total_count = len(results)

    # Calculate source hash if possible
    source_hash = "N/A"
    try:
        module_name = adapter_path.rsplit(".", 1)[0]
        module = importlib.import_module(module_name)
        if hasattr(module, "__file__") and module.__file__:
            with open(module.__file__, "rb") as f:
                source_hash = hashlib.sha256(f.read()).hexdigest()
    except Exception:
        pass

    certificate = {
        "adapter": adapter_path,
        "adapter_name": adapter_class_name,
        "kernel_version": "0.9.0",
        "action_spec_version": "1.0",
        "worldstate_spec_version": "1.0",
        "adapter_contract_version": "1.0",
        "timestamp": timestamp,
        "conformance_command": f"python -m decision_kernel_conformance {adapter_path}",
        "source_hash": source_hash,
        "results": {
            "passed": passed_count,
            "total": total_count,
            "status": "PASS" if passed_count == total_count else "FAIL",
            "tests": [{"name": name, "passed": passed, "message": msg} for name, passed, msg in results]
        }
    }

    # Create output directory
    cert_dir = Path(output_dir) / adapter_class_name
    cert_dir.mkdir(parents=True, exist_ok=True)

    # Save JSON
    json_file = cert_dir / f"{timestamp.replace(':', '-')}.json"
    with open(json_file, "w") as f:
        json.dump(certificate, f, indent=2)

    # Save Markdown
    md_file = cert_dir / f"{timestamp.replace(':', '-')}.md"
    with open(md_file, "w", encoding="utf-8") as f:
        f.write("# Conformance Certificate\n\n")
        f.write(f"**Adapter**: `{adapter_path}`\n")
        f.write(f"**Status**: {certificate['results']['status']}\n")
        f.write(f"**Timestamp**: {timestamp}\n")
        f.write(f"**Kernel Version**: {certificate['kernel_version']}\n\n")
        f.write("## Specifications\n\n")
        f.write(f"- Action Spec: v{certificate['action_spec_version']}\n")
        f.write(f"- WorldState Spec: v{certificate['worldstate_spec_version']}\n")
        f.write(f"- Adapter Contract: v{certificate['adapter_contract_version']}\n\n")
        f.write("## Results\n\n")
        f.write(f"**Passed**: {passed_count}/{total_count} tests\n\n")
        for test in certificate['results']['tests']:
            status = "PASS" if test['passed'] else "FAIL"
            f.write(f"- [{status}] {test['name']}\n")
        f.write("\n## Verification\n\n")
        f.write(f"```bash\n{certificate['conformance_command']}\n```\n\n")
        f.write(f"**Source Hash**: `{source_hash}`\n")

    return json_file, md_file


def run_conformance(adapter_path: str, generate_cert: bool = False) -> bool:
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
        success = True
    else:
        print("[FAIL] Adapter is NOT CONFORMANT")
        success = False

    # Generate certificate if requested
    if generate_cert:
        try:
            json_file, md_file = generate_certificate(adapter_path, results, adapter.__class__.__name__)
            print("\nCertificate generated:")
            print(f"  JSON: {json_file}")
            print(f"  MD: {md_file}")
        except Exception as e:
            print(f"\nWarning: Could not generate certificate: {e}")

    return success


def main():
    """CLI entry point"""
    if len(sys.argv) < 2:
        print("Usage: python -m decision_kernel_conformance <module.ClassName> [--cert]")
        print("Example: python -m decision_kernel_conformance adapters.mock.mock_robot.MockRobot")
        print("Options:")
        print("  --cert    Generate conformance certificate")
        return 1

    adapter_path = sys.argv[1]
    generate_cert = "--cert" in sys.argv
    success = run_conformance(adapter_path, generate_cert=generate_cert)
    return 0 if success else 1
