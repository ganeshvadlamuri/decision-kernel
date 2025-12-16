# Decision Kernel in 60 Minutes

A lecture-style walkthrough for university courses and workshops.

**Target Audience**: Students with basic Python and robotics knowledge  
**Prerequisites**: Python 3.10+, basic understanding of robot systems  
**Duration**: 60 minutes (40 min lecture + 20 min lab)

## Part 1: Motivation (10 minutes)

### The Problem

Modern robots conflate three concerns:
1. **What to do** (decision-making)
2. **How to move** (motion planning)
3. **How to command hardware** (control)

**Question**: Why is this problematic?

**Answer**: Hardware lock-in, middleware dependency, no behavior reuse.

### The Solution

**Separate decision logic from execution infrastructure.**

```
Human Intent → Decision Kernel → Hardware Adapter → Robot
```

Decision Kernel: What to do  
Adapter: How to do it  
Hardware: Does it

### Key Insight

Decision logic should be **hardware-agnostic**.

Same decision code should run on:
- Different robots
- Different simulators
- Different middleware (ROS, custom, etc.)

## Part 2: Core Concepts (15 minutes)

### Concept 1: WorldState

**Definition**: Representation of environment at a point in time.

```python
WorldState(
    objects=[WorldObject("cup", "table", "graspable")],
    robot_location="kitchen",
    human_location="living_room",
    locations=["kitchen", "table", "living_room"],
    timestamp=time.time(),
    frame_id="world",
    relations={"cup": {"on": "table"}}
)
```

**Key Point**: WorldState is hardware-agnostic. Same structure for all robots.

### Concept 2: Action

**Definition**: Single executable operation.

```python
Action(
    action_type="navigate_to",
    location="kitchen",
    version="1.0"
)
```

**Key Point**: Actions are abstract. Adapters translate to hardware commands.

### Concept 3: Plan

**Definition**: Sequence of actions to achieve goal.

```python
plan = [
    Action("navigate_to", location="kitchen"),
    Action("grasp", target="cup"),
    Action("navigate_to", location="living_room"),
    Action("release", target="cup")
]
```

**Key Point**: Plans are hardware-independent. Same plan works on different robots.

### Concept 4: Adapter

**Definition**: Translation layer between kernel and hardware.

```python
class MyAdapter:
    def sense(self) -> WorldState:
        # Read sensors, return WorldState
        pass
    
    def execute(self, plan: list[Action]) -> ExecutionReport:
        # Translate actions to hardware commands
        pass
    
    def capabilities(self) -> dict:
        # Declare supported actions
        return {"supported_actions": ["navigate_to", "grasp"]}
```

**Key Point**: Adapters are thin. They translate, not implement autonomy.

## Part 3: Pipeline (10 minutes)

### The Decision Pipeline

```
Intent → Parse → Plan → Validate → Execute
```

**Step 1: Intent Parsing**
```python
intent = "bring me water"
goal = intent_parser.parse(intent)
# Goal(action="bring", target="water")
```

**Step 2: Planning**
```python
plan = planner.plan(goal, world_state)
# [navigate_to(kitchen), grasp(water), navigate_to(human), release(water)]
```

**Step 3: Safety Validation**
```python
is_safe, reason = safety.validate(plan)
# (True, "All constraints satisfied")
```

**Step 4: Execution**
```python
report = adapter.execute(plan)
# ExecutionReport(success=True, results=[...])
```

### Complete Example

```python
from brain.kernel import RobotBrainKernel

# Create kernel with adapter
kernel = RobotBrainKernel(adapter=my_adapter)

# Sense world
world_state = my_adapter.sense()

# Process intent
plan = kernel.process("bring me water", world_state)

# Execute
report = my_adapter.execute(plan)
```

**Key Point**: Same code works with any conformant adapter.

## Part 4: Conformance (5 minutes)

### What is Conformance?

**Definition**: Adapter correctly implements the contract.

**Contract Requirements**:
1. Has sense(), execute(), capabilities() methods
2. sense() returns valid WorldState
3. execute() returns valid ExecutionReport
4. capabilities() declares supported actions

### Verification

```bash
python -m decision_kernel_conformance my_adapter.MyAdapter
```

**Output**:
```
[PASS]: Method presence
[PASS]: sense() contract
[PASS]: execute() contract
[PASS]: capabilities() contract

Results: 4/4 tests passed
[PASS] Adapter is CONFORMANT
```

**Key Point**: Conformance is automated and objective.

## Part 5: Multi-Environment Proof (10 minutes)

### Same Kernel, Different Environments

**Environment 1: ROS2**
```python
from decision_kernel_ros2.adapter import ROS2Adapter

adapter = ROS2Adapter()
kernel = RobotBrainKernel(adapter=adapter)
# Kernel works with ROS2
```

**Environment 2: Webots**
```python
from decision_kernel_webots.adapter import WebotsAdapter

adapter = WebotsAdapter()
kernel = RobotBrainKernel(adapter=adapter)
# Same kernel works with Webots
```

**Environment 3: Mock**
```python
from adapters.mock.mock_robot import MockRobot

adapter = MockRobot()
kernel = RobotBrainKernel(adapter=adapter)
# Same kernel works with mock
```

**Key Insight**: Decision logic is portable. Only adapters change.

### Why This Matters

**For Research**: Test algorithms in simulation, deploy on real robots  
**For Education**: Learn on simulators, transfer to hardware  
**For Industry**: Develop vendor-neutral solutions

## Lab Exercise (20 minutes)

### Exercise 1: Run Webots Demo (5 min)

```bash
cd decision-kernel-webots
python demo.py
```

**Observe**:
1. WorldState construction
2. Intent parsing
3. Plan generation
4. Action execution

**Question**: What would change if this was a real robot?  
**Answer**: Only the adapter implementation.

### Exercise 2: Inspect WorldState (5 min)

```python
from brain.world.state import WorldState
from brain.world.objects import WorldObject
import time

# Create WorldState
world = WorldState(
    objects=[WorldObject("bottle", "table", "graspable")],
    robot_location="start",
    human_location="goal",
    locations=["start", "table", "goal"],
    timestamp=time.time(),
    frame_id="world",
    relations={}
)

# Inspect
print(f"Objects: {[obj.name for obj in world.objects]}")
print(f"Robot at: {world.robot_location}")
```

**Task**: Add another object and location.

### Exercise 3: Create Simple Adapter (10 min)

```python
from brain.world.state import WorldState
from brain.execution.report import ExecutionReport
import time

class SimpleAdapter:
    def sense(self) -> WorldState:
        return WorldState(
            objects=[],
            robot_location="home",
            human_location="home",
            locations=["home"],
            timestamp=time.time(),
            frame_id="world",
            relations={}
        )
    
    def execute(self, plan):
        print(f"Executing {len(plan)} actions")
        for action in plan:
            print(f"  - {action}")
        return ExecutionReport(success=True, message="Done")
    
    def capabilities(self):
        return {
            "supported_actions": ["navigate_to"],
            "hardware": "simple",
            "version": "1.0"
        }
```

**Task**: Test conformance:
```bash
python -m decision_kernel_conformance your_module.SimpleAdapter
```

## Summary (5 minutes)

### Key Takeaways

1. **Separation of Concerns**: Decision logic ≠ Execution logic
2. **Hardware Agnostic**: Same kernel, different adapters
3. **Formal Contracts**: Conformance is verifiable
4. **Multi-Environment**: Proven on ROS2, Webots, Mock
5. **Minimal Interface**: Adapters are thin translation layers

### What Decision Kernel Is

- Orchestration layer for robot decisions
- Hardware-agnostic interface
- Stable, boring infrastructure

### What Decision Kernel Is Not

- Motion planner
- Perception system
- Hardware driver
- AI/ML framework

### Next Steps

**For Students**:
- Implement adapter for your robot
- Test conformance
- Experiment with planning

**For Researchers**:
- Replace planner with your algorithm
- Evaluate across environments
- Cite whitepaper

**For Developers**:
- Integrate into your stack
- Contribute adapters
- Join community

## Resources

- **Whitepaper**: docs/papers/decision_kernel_whitepaper.md
- **Adoption Guide**: docs/adoption.md
- **Specifications**: docs/action_spec.md, docs/world_state_spec.md
- **Examples**: demos/, examples/

## Questions?

Common questions and answers:

**Q: Can I use my own planner?**  
A: Yes. Planner is replaceable.

**Q: Does this work with ROS1?**  
A: Yes. Create ROS1 adapter.

**Q: Is this production-ready?**  
A: Kernel is stable. Adapters vary.

**Q: How do I contribute?**  
A: See CONTRIBUTING.md

---

**End of Tutorial**

**Time**: 60 minutes  
**Outcome**: Students understand Decision Kernel concepts and can run demos  
**Next**: Students implement their own adapters
