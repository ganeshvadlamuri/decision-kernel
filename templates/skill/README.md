# Skill Template

Minimal template for creating decision-kernel compatible skills.

## Quick Start

1. Copy this template:
```bash
cp -r templates/skill my_skill
cd my_skill
```

2. Edit `my_skill.py`:
   - Update skill name
   - Define inputs
   - List preconditions and effects
   - Create action sequence

3. Test your skill:
```bash
python test_my_skill.py
```

## Skill Structure

### Required Fields

- **name**: Unique identifier (matches Goal.action)
- **description**: Human-readable description
- **inputs**: Dictionary of input parameters
- **preconditions**: List of required conditions
- **effects**: List of expected outcomes
- **action_sequence**: List of action templates

### Parameter Substitution

Use placeholders in action_sequence:
- `{target}` → goal.target
- `{target_location}` → location of target object
- `{human_location}` → world_state.human_location
- `{destination}` → custom parameter

## Example Usage

```python
from brain.kernel import RobotBrainKernel
from brain.skills.registry import SkillRegistry
from my_skill import create_my_skill

# Register skill
registry = SkillRegistry()
registry.register(create_my_skill())

# Use with kernel
kernel = RobotBrainKernel(skill_registry=registry)
```

## Testing

```python
from brain.skills.registry import SkillRegistry
from my_skill import create_my_skill

def test_my_skill():
    skill = create_my_skill()
    assert skill.name == "my_skill"
    assert len(skill.action_sequence) > 0
```

## Documentation

See [Skill Specification](../../docs/skill_spec.md) for full details.
