# Adapter Contract v1.0

## Overview

Adapters bridge the decision kernel to real hardware, simulators, or mock systems. This contract defines the required interface.

## Protocol

```python
class Adapter(Protocol):
    def sense(self) -> WorldState
    def execute(self, plan: list[Action]) -> ExecutionReport
    def capabilities(self) -> dict
```

## Required Methods

### sense() -> WorldState

Sense the environment and return current world state.

**Returns:**
- WorldState conforming to v1.0 spec
- Must include valid timestamp
- Must include all required fields

**Responsibilities:**
- Query sensors/simulation
- Construct WorldState representation
- Update timestamp to current time
- Populate objects, locations, robot/human positions

**Example:**
```python
def sense(self) -> WorldState:
    return WorldState(
        objects=[WorldObject("cup", "table", "container")],
        robot_location="kitchen",
        human_location="living_room",
        locations=["kitchen", "living_room"],
        timestamp=time.time(),
        frame_id="world"
    )
```

### execute(plan: list[Action]) -> ExecutionReport

Execute a plan and return execution report.

**Args:**
- plan: List of Action objects conforming to v1.0 spec

**Returns:**
- ExecutionReport with:
  - success: Overall success boolean
  - results: List of ActionResult for each action
  - total_duration: Total execution time
  - message: Summary message

**Responsibilities:**
- Execute each action in sequence
- Record result for each action
- Handle failures gracefully
- Return comprehensive report

**Example:**
```python
def execute(self, plan: list[Action]) -> ExecutionReport:
    report = ExecutionReport(success=True)
    for i, action in enumerate(plan):
        result = ActionResult(
            action_index=i,
            status=ExecutionStatus.SUCCESS,
            duration=0.1
        )
        report.add_result(result)
    return report
```

### capabilities() -> dict

Report adapter capabilities and supported features.

**Returns:**
- Dictionary with standard keys:
  - **supported_actions** (required): List of action types adapter can execute
  - **hardware** (required): Hardware identifier string
  - **version** (required): Adapter version string
  - sensing (optional): List of available sensors
  - max_payload (optional): Maximum payload in kg
  - workspace (optional): Workspace dimensions

**Standard Keys:**
```python
{
    "supported_actions": ["navigate_to", "grasp", "release"],  # Required
    "hardware": "mock",                                         # Required
    "version": "1.0",                                           # Required
    "sensing": ["camera", "lidar"],                            # Optional
    "max_payload": 5.0,                                         # Optional
    "workspace": {"x": 2.0, "y": 2.0, "z": 1.5}               # Optional
}
```

**Example:**
```python
def capabilities(self) -> dict:
    return {
        "supported_actions": ["navigate_to", "grasp", "release"],
        "sensing": ["camera", "lidar"],
        "hardware": "mock",
        "version": "1.0"
    }
```

## Implementation Guidelines

### Error Handling
- Adapters should not raise exceptions during execute()
- Report failures via ExecutionReport.success = False
- Include error details in ActionResult.error

### State Consistency
- sense() should return fresh state
- Update timestamp on every sense() call
- Maintain internal state consistency

### Performance
- execute() may be blocking
- Report progress via ActionResult
- Consider timeout handling

### Testing
- Implement conformance tests
- Verify all methods present
- Validate return types

## Conformance

Adapters must:
1. Implement all three methods
2. Return correct types
3. Handle edge cases (empty plans, invalid actions)
4. Provide meaningful error messages
5. Pass conformance test suite

## Examples

### Mock Adapter
```python
class MockAdapter:
    def sense(self) -> WorldState:
        return WorldState(
            objects=[],
            robot_location="home",
            human_location="home",
            locations=["home"],
            timestamp=time.time()
        )
    
    def execute(self, plan: list[Action]) -> ExecutionReport:
        report = ExecutionReport(success=True)
        for i, action in enumerate(plan):
            print(f"Executing: {action}")
            report.add_result(ActionResult(
                action_index=i,
                status=ExecutionStatus.SUCCESS
            ))
        return report
    
    def capabilities(self) -> dict:
        return {"hardware": "mock", "version": "1.0"}
```

## Version History

- v1.0 (v0.3): Initial adapter contract specification
