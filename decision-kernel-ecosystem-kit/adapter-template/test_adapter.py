"""Test adapter conformance"""

import subprocess
import sys


def test_conformance():
    """Run conformance tests"""
    result = subprocess.run(
        [sys.executable, "-m", "decision_kernel_conformance", "adapter.MyAdapter"],
        capture_output=True,
        text=True,
    )

    print(result.stdout)
    if result.stderr:
        print(result.stderr)

    assert result.returncode == 0, "Conformance tests failed"
    assert "4/4 tests passed" in result.stdout


if __name__ == "__main__":
    test_conformance()
    print("\n[OK] Adapter is Decision Kernel Compatible!")
