# Adapter Template

Minimal template for creating a decision-kernel compatible adapter.

## Quick Start

1. Copy this template:
```bash
cp -r templates/adapter-python my_adapter
cd my_adapter
```

2. Edit `my_adapter.py`:
   - Replace `sense()` with your sensor/simulation logic
   - Replace `execute()` with your hardware control logic
   - Update `capabilities()` to match your hardware

3. Test conformance:
```bash
python -m decision_kernel_conformance my_adapter.MyAdapter
```

## Adapter Contract

Your adapter must implement three methods:

### sense() -> WorldState
Query environment and return current state.

**Must return:**
- Valid WorldState with all required fields
- Fresh timestamp
- Accurate object/location data

### execute(plan: list[Action]) -> ExecutionReport
Execute action plan and return results.

**Must:**
- Execute each action in sequence
- Record result for each action
- Handle failures gracefully
- Return comprehensive report

### capabilities() -> dict
Report what your adapter supports.

**Must include:**
- `supported_actions`: List of action types
- `hardware`: Hardware identifier
- `version`: Adapter version

## Example Usage

```python
from my_adapter import MyAdapter
from brain.kernel import RobotBrainKernel

# Create adapter
adapter = MyAdapter()

# Use with kernel
kernel = RobotBrainKernel()
world = adapter.sense()
plan = kernel.process("bring me water", world)
report = adapter.execute(plan)
```

## Testing

Run conformance tests:
```bash
# Test your adapter
python -m decision_kernel_conformance my_adapter.MyAdapter

# Run with pytest
pytest test_my_adapter.py
```

## Documentation

See [Adapter Contract](../../docs/adapter_contract.md) for full specification.
