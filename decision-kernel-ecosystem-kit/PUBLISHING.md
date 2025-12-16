# Publishing Guide

How to share your Decision Kernel compatible adapter or skill.

## Adapter Publishing

### 1. Verify Conformance

```bash
python -m decision_kernel_conformance your_module.YourAdapter
```

Must pass 4/4 tests:
- Method presence check
- sense() contract
- execute() contract
- capabilities() contract

### 2. Prepare Repository

Required files:
- `README.md` with usage examples
- Conformance command in README
- License file
- Example code

### 3. Submit to Registry

Create PR to `decision-kernel` repository:

```yaml
# Add to registry/compatible_adapters.yaml
- name: my-adapter
  description: Adapter for XYZ robot
  repository: https://github.com/user/my-adapter
  conformance: "python -m decision_kernel_conformance my_adapter.MyAdapter"
  hardware: xyz_robot
  version: "1.0"
```

### 4. Add Badge

Add to your README:

```markdown
![Decision Kernel Compatible](https://img.shields.io/badge/Decision%20Kernel-Compatible-brightgreen)
```

## Skill Publishing

### 1. Test Skill

```bash
python test_skill.py
```

### 2. Prepare Repository

Required files:
- `README.md` with usage examples
- Test file
- License file

### 3. Submit to Registry

Create PR to `decision-kernel` repository:

```yaml
# Add to registry/compatible_skills.yaml
- name: my-skill
  description: Skill for XYZ behavior
  repository: https://github.com/user/my-skill
  intent_pattern: "do xyz"
  version: "1.0"
```

## Best Practices

- Include clear documentation
- Provide usage examples
- Add tests
- Follow semantic versioning
- Maintain backward compatibility
- Respond to issues promptly

## Questions?

Open an issue in the `decision-kernel` repository.
