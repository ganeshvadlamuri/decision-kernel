# Decision Kernel Ecosystem Kit

Scaffold for creating Decision Kernel compatible adapters and skills.

## What's Included

- **Adapter template**: Hardware integration template
- **Skill template**: Reusable behavior template
- **Conformance guide**: How to verify compatibility
- **Publishing checklist**: Steps to share your adapter/skill

## Quick Start

### Create an Adapter

```bash
# Copy template
cp -r adapter-template/ my-robot-adapter/
cd my-robot-adapter/

# Edit adapter.py with your hardware logic
# Run conformance tests
python -m decision_kernel_conformance my_adapter.MyAdapter
```

### Create a Skill

```bash
# Copy template
cp -r skill-template/ my-skill/
cd my-skill/

# Edit skill.py with your behavior
# Test it
python test_skill.py
```

## Publishing Your Work

### Adapter Checklist

- [ ] Passes Action Specification v1.0
- [ ] Passes WorldState Specification v1.0
- [ ] Passes Adapter Contract conformance (4/4 tests)
- [ ] Includes README with usage examples
- [ ] Includes conformance command in README
- [ ] Submit PR to add to registry/compatible_adapters.yaml

### Skill Checklist

- [ ] Follows Skill Specification v1.0
- [ ] Includes test file
- [ ] Includes README with usage examples
- [ ] Submit PR to add to registry/compatible_skills.yaml

## Conformance Testing

```bash
# Install decision-kernel
pip install decision-kernel

# Test your adapter
python -m decision_kernel_conformance your_module.YourAdapter

# Expected output:
# ✓ Method presence check: PASS
# ✓ sense() contract: PASS
# ✓ execute() contract: PASS
# ✓ capabilities() contract: PASS
# Conformance: 4/4 tests passed
```

## Resources

- [Adapter Contract](../docs/adapter_contract.md)
- [Skill Specification](../docs/skill_spec.md)
- [Action Specification](../docs/action_spec.md)
- [WorldState Specification](../docs/world_state_spec.md)

## Community

- Submit adapters/skills via PR
- Report issues on GitHub
- Join discussions in Issues

---

**Note**: This kit will be split into a separate repository in the future for easier distribution.
