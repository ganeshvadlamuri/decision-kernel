# Decision Kernel Lab Exercises

Hands-on exercises for students and workshop participants.

## Lab 1: Understanding WorldState (15 minutes)

### Objective
Understand how environment state is represented in Decision Kernel.

### Exercise 1.1: Create WorldState

```python
from brain.world.state import WorldState
from brain.world.objects import WorldObject
import time

# TODO: Create a WorldState with:
# - 2 objects: "book" on "desk", "pen" on "desk"
# - Robot at "entrance"
# - Human at "desk"
# - 3 locations: "entrance", "desk", "exit"

world = WorldState(
    objects=[
        # Your code here
    ],
    robot_location="",  # Your code here
    human_location="",  # Your code here
    locations=[],  # Your code here
    timestamp=time.time(),
    frame_id="world",
    relations={}  # Optional: add relations
)

print(f"Objects: {[obj.name for obj in world.objects]}")
print(f"Robot: {world.robot_location}")
```

### Exercise 1.2: Query WorldState

```python
# Given a WorldState, find an object
def find_object(world: WorldState, name: str):
    # TODO: Implement
    pass

# Test
obj = find_object(world, "book")
print(f"Found: {obj.name} at {obj.location}")
```

### Exercise 1.3: Validate WorldState

```python
from brain.world.validate import validate_world_state

# TODO: Create an invalid WorldState (empty robot_location)
# Run validation and observe error

invalid_world = WorldState(
    objects=[],
    robot_location="",  # Invalid!
    human_location="home",
    locations=["home"]
)

is_valid, errors = validate_world_state(invalid_world)
print(f"Valid: {is_valid}")
print(f"Errors: {errors}")
```

## Lab 2: Working with Actions (15 minutes)

### Objective
Understand action representation and validation.

### Exercise 2.1: Create Actions

```python
from brain.planner.actions import Action

# TODO: Create actions for:
# 1. Navigate to kitchen
# 2. Grasp cup
# 3. Navigate to living room
# 4. Release cup

actions = [
    # Your code here
]

for i, action in enumerate(actions, 1):
    print(f"{i}. {action}")
```

### Exercise 2.2: Validate Actions

```python
from brain.planner.validate_actions import validate_action

# TODO: Create an invalid action (empty action_type)
invalid_action = Action("", target="cup")

is_valid, error = validate_action(invalid_action)
print(f"Valid: {is_valid}")
print(f"Error: {error}")
```

### Exercise 2.3: Action with Parameters

```python
# TODO: Create action with custom parameters
action = Action(
    action_type="navigate_to",
    location="kitchen",
    parameters={
        "speed": 0.5,
        "avoid_obstacles": True
    }
)

print(f"Action: {action}")
print(f"Parameters: {action.parameters}")
```

## Lab 3: Building an Adapter (30 minutes)

### Objective
Implement a minimal conformant adapter.

### Exercise 3.1: Skeleton Adapter

```python
from brain.world.state import WorldState
from brain.world.objects import WorldObject
from brain.execution.report import ExecutionReport, ActionResult, ExecutionStatus
from brain.planner.actions import Action
import time

class MyFirstAdapter:
    def sense(self) -> WorldState:
        # TODO: Return a WorldState with at least:
        # - 1 object
        # - robot_location
        # - human_location
        # - 1 location
        pass
    
    def execute(self, plan: list[Action]) -> ExecutionReport:
        # TODO: Create ExecutionReport
        # - Iterate through plan
        # - Print each action
        # - Add ActionResult for each
        pass
    
    def capabilities(self) -> dict:
        # TODO: Return dict with:
        # - supported_actions (list)
        # - hardware (string)
        # - version (string)
        pass
```

### Exercise 3.2: Test Adapter

```python
# Test your adapter
adapter = MyFirstAdapter()

# Test sense()
world = adapter.sense()
print(f"WorldState: {len(world.objects)} objects")

# Test execute()
plan = [Action("navigate_to", location="test")]
report = adapter.execute(plan)
print(f"Execution: {report.success}")

# Test capabilities()
caps = adapter.capabilities()
print(f"Capabilities: {caps}")
```

### Exercise 3.3: Run Conformance

```bash
# Save your adapter to my_adapter.py
# Run conformance tests
python -m decision_kernel_conformance my_adapter.MyFirstAdapter
```

**Expected**: 4/4 tests passed

## Lab 4: Using the Kernel (20 minutes)

### Objective
Use Decision Kernel to process intent and generate plans.

### Exercise 4.1: Basic Pipeline

```python
from brain.kernel import RobotBrainKernel
from my_adapter import MyFirstAdapter

# TODO: Create kernel with your adapter
adapter = MyFirstAdapter()
kernel = RobotBrainKernel(adapter=adapter)

# TODO: Get world state
world_state = adapter.sense()

# TODO: Process intent
intent = "bring me water"
plan = kernel.process(intent, world_state)

# TODO: Print plan
for i, action in enumerate(plan, 1):
    print(f"{i}. {action}")
```

### Exercise 4.2: Execute Plan

```python
# TODO: Execute the plan
report = adapter.execute(plan)

# TODO: Check results
print(f"Success: {report.success}")
print(f"Message: {report.message}")
print(f"Actions completed: {len(report.results)}")
```

### Exercise 4.3: Different Intents

```python
# TODO: Try different intents
intents = [
    "bring me water",
    "navigate to kitchen",
    "grasp cup"
]

for intent in intents:
    plan = kernel.process(intent, world_state)
    print(f"\nIntent: {intent}")
    print(f"Plan: {len(plan)} actions")
    for action in plan:
        print(f"  - {action}")
```

## Lab 5: Running Demos (15 minutes)

### Objective
Run and understand reference implementations.

### Exercise 5.1: Webots Demo

```bash
# Navigate to Webots adapter
cd decision-kernel-webots

# Run demo
python demo.py
```

**Observe**:
1. How WorldState is constructed
2. How intent is parsed
3. How plan is generated
4. How actions are executed

**Question**: What would you change to add a new action type?

### Exercise 5.2: ROS2 Demo

```bash
# Navigate to main directory
cd ..

# Run ROS2 demo
python -m demos.ros2_hello_world.run
```

**Observe**:
1. Simulated ROS2 topics
2. Adapter translation
3. Kernel processing
4. Execution logging

**Question**: How does this differ from Webots demo?

### Exercise 5.3: Compare Adapters

```python
# TODO: Load both adapters
from decision_kernel_ros2.adapter import ROS2Adapter
from decision_kernel_webots.adapter import WebotsAdapter

ros_adapter = ROS2Adapter()
webots_adapter = WebotsAdapter()

# TODO: Compare capabilities
print("ROS2:", ros_adapter.capabilities())
print("Webots:", webots_adapter.capabilities())

# Question: What's the same? What's different?
```

## Challenge Exercises

### Challenge 1: Custom Planner

Implement a planner that generates different action sequences.

```python
from brain.planner.planner import Planner
from brain.intent.schema import Goal
from brain.world.state import WorldState
from brain.planner.actions import Action

class MyPlanner(Planner):
    def plan(self, goal: Goal, world_state: WorldState) -> list[Action]:
        # TODO: Implement custom planning logic
        pass
```

### Challenge 2: Safety Constraints

Add custom safety validation.

```python
from brain.safety.rules import SafetyValidator

class MyValidator(SafetyValidator):
    def validate(self, plan: list[Action]) -> tuple[bool, str]:
        # TODO: Add custom safety checks
        # Example: No more than 5 actions
        # Example: Must start with navigate_to
        pass
```

### Challenge 3: Multi-Robot Adapter

Create adapter that manages multiple robots.

```python
class MultiRobotAdapter:
    def __init__(self, robots: list):
        self.robots = robots
    
    def sense(self) -> WorldState:
        # TODO: Aggregate state from all robots
        pass
    
    def execute(self, plan: list[Action]) -> ExecutionReport:
        # TODO: Distribute actions across robots
        pass
```

## Solutions

Solutions available in `docs/teaching/solutions/` directory.

## Assessment

### Criteria

Students should be able to:
1. Create valid WorldState and Actions
2. Implement conformant adapter
3. Use kernel to process intents
4. Run and understand demos
5. Explain separation of concerns

### Grading Rubric

- **Lab 1-2** (20%): Data structures
- **Lab 3** (30%): Adapter implementation
- **Lab 4** (30%): Kernel usage
- **Lab 5** (20%): Demo understanding

## Resources

- **Tutorial**: docs/teaching/60_minute_tutorial.md
- **Specifications**: docs/action_spec.md, docs/world_state_spec.md
- **Examples**: examples/, demos/
- **Help**: GitHub Discussions

## Tips

1. Start simple - minimal adapter first
2. Test conformance early and often
3. Read error messages carefully
4. Study reference implementations
5. Ask questions in discussions

---

**Good luck!**
