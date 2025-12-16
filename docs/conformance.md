# Conformance Testing

## Overview

The conformance runner verifies that adapters correctly implement the Adapter contract.

## Usage

### Command Line

```bash
python -m decision_kernel_conformance <module.ClassName>
```

### Examples

Test the built-in MockRobot:
```bash
python -m decision_kernel_conformance adapters.mock.mock_robot.MockRobot
```

Test your custom adapter:
```bash
python -m decision_kernel_conformance my_adapter.MyAdapter
```

## What It Tests

The conformance runner verifies:

1. **Method Presence**
   - sense() exists and is callable
   - execute() exists and is callable
   - capabilities() exists and is callable

2. **sense() Contract**
   - Returns WorldState instance
   - WorldState has valid timestamp
   - Timestamp is positive

3. **execute() Contract**
   - Returns ExecutionReport instance
   - ExecutionReport has success field
   - Handles action plans

4. **capabilities() Contract**
   - Returns dictionary
   - Contains 'supported_actions' key
   - Contains 'hardware' key

## Output

### Passing Adapter
```
Loading adapter: adapters.mock.mock_robot.MockRobot
Adapter loaded: MockRobot

✓ PASS: Method presence
✓ PASS: sense() contract
✓ PASS: execute() contract
✓ PASS: capabilities() contract

==================================================
Results: 4/4 tests passed
✓ Adapter is CONFORMANT
```

### Failing Adapter
```
Loading adapter: my_adapter.BrokenAdapter
Adapter loaded: BrokenAdapter

✓ PASS: Method presence
✗ FAIL: sense() contract
  WorldState timestamp must be positive
✓ PASS: execute() contract
✓ PASS: capabilities() contract

==================================================
Results: 3/4 tests passed
✗ Adapter is NOT CONFORMANT
```

## Programmatic Usage

```python
from decision_kernel_conformance import run_conformance

# Test adapter
success = run_conformance("my_adapter.MyAdapter")
if success:
    print("Adapter is conformant!")
```

## Integration with CI

Add to your CI pipeline:

```yaml
- name: Test Adapter Conformance
  run: |
    python -m decision_kernel_conformance my_adapter.MyAdapter
```

## Creating Conformant Adapters

1. Use the adapter template:
```bash
cp -r templates/adapter-python my_adapter
```

2. Implement required methods:
   - sense() -> WorldState
   - execute(plan) -> ExecutionReport
   - capabilities() -> dict

3. Test conformance:
```bash
python -m decision_kernel_conformance my_adapter.MyAdapter
```

4. Fix any failures and retest

## See Also

- [Adapter Contract](adapter_contract.md) - Full specification
- [Adapter Template](../templates/adapter-python/) - Quick start template
