# Pull Request: v0.2 Skills System

## Summary

Implements optional skill system as a clean extension mechanism for reusable behavior templates. Skills are opt-in and maintain full backward compatibility.

## Changes

### New Files

**Core Implementation:**
- `brain/skills/skill.py` - Skill dataclass definition
- `brain/skills/registry.py` - SkillRegistry for skill management
- `brain/skills/builtin.py` - Reference "bring" skill
- `brain/skills/__init__.py` - Module exports

**Documentation:**
- `docs/skill_spec.md` - Complete skill specification
- `examples/pick_and_place.yaml` - Pick-and-place skill example
- `examples/skills_demo.py` - Working demonstration

**Tests:**
- `tests/test_skills.py` - 8 new tests covering:
  - Skill creation and registry operations
  - Planner skill integration
  - Fallback behavior
  - Built-in skill validation

### Modified Files

**Core Integration:**
- `brain/planner/planner.py` - Added optional skill_registry parameter, skill-based planning with fallback
- `brain/kernel.py` - Added optional skill_registry parameter

**Documentation:**
- `README.md` - Added Skills usage section and documentation link
- `CHANGELOG.md` - Added v0.2.0 entry
- `pyproject.toml` - Version bump to 0.2.0

## Design Principles

✅ **Optional**: Skills are opt-in, existing behavior unchanged  
✅ **Explicit**: No magic globals, explicit registration required  
✅ **Minimal**: Simple data structures, no complex logic  
✅ **Backward Compatible**: All existing tests pass  
✅ **Clean Boundaries**: No ROS, hardware, or cloud dependencies  

## API Stability

### Unchanged Behavior
```python
# v0.1 code still works exactly the same
kernel = RobotBrainKernel()
plan = kernel.process("bring me water", world)
```

### New Optional Behavior
```python
# v0.2 opt-in skills
registry = SkillRegistry()
registry.register(create_bring_water_skill())
kernel = RobotBrainKernel(skill_registry=registry)
```

## Test Results

```
Tests:        23 passing (15 existing + 8 new)
Lint:         All checks passed
Type Check:   Success (29 files)
CLI:          Backward compatible
Contracts:    All passing
```

## Verification Commands

```bash
# Backward compatibility
python -m cli.run "bring me water"

# All tests
pytest tests/ -v

# Quality gates
ruff check .
mypy brain/ cli/ adapters/ --ignore-missing-imports

# Skills demo
python -m examples.skills_demo
```

## Architecture Impact

- No changes to core kernel pipeline
- Planner checks skill registry before fallback
- Skills are pure data (no executable code)
- Parameter substitution at planning time
- Clean separation: skills in brain/, not adapters/

## Breaking Changes

None. This is a backward-compatible feature addition.

## Migration Guide

No migration needed. Existing code continues to work without modification.

To adopt skills:
1. Create SkillRegistry
2. Register skills
3. Pass registry to RobotBrainKernel

See `docs/skill_spec.md` for details.

## Future Work

Skills v0.2 is intentionally minimal. Future enhancements could include:
- Conditional action sequences
- Skill composition
- Runtime precondition checking
- Skill validation tools

These are explicitly out of scope for v0.2 to maintain simplicity.

## Checklist

- [x] Implementation complete
- [x] Tests passing (23/23)
- [x] Lint passing
- [x] Type check passing
- [x] Documentation updated
- [x] CHANGELOG updated
- [x] Backward compatibility verified
- [x] Examples provided
- [x] No ROS/hardware/cloud dependencies
- [x] Clean architecture maintained

## Ready to Merge

This PR is ready for review and merge.
