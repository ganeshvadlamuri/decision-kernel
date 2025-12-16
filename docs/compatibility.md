# Decision Kernel Compatibility

Formal definition of "Decision Kernel Compatible" status.

## What It Means

An adapter or skill is **Decision Kernel Compatible** if it:

1. **Passes Action Specification v1.0**
   - Uses Action dataclass correctly
   - Includes required fields (action_type, version)
   - Validates action structure

2. **Passes WorldState Specification v1.0**
   - Uses WorldState dataclass correctly
   - Includes required fields (objects, locations, timestamp, frame_id)
   - Validates state structure

3. **Passes Adapter Contract conformance**
   - Implements sense() → WorldState
   - Implements execute(plan) → ExecutionReport
   - Implements capabilities() → dict
   - Passes 4/4 conformance tests

## What It Does NOT Mean

Decision Kernel Compatible does NOT guarantee:

- ✗ Hardware compatibility
- ✗ Performance characteristics
- ✗ Safety certification
- ✗ Production readiness
- ✗ Specific action support
- ✗ Real-time guarantees

Compatibility is about **interface adherence**, not implementation quality.

## Verification

### Adapters

```bash
python -m decision_kernel_conformance your_module.YourAdapter
```

Must output:
```
Results: 4/4 tests passed
[PASS] Adapter is CONFORMANT
```

### Skills

Skills must:
- Follow Skill Specification v1.0
- Use correct dataclass structure
- Include test file
- Document intent pattern

## Version Compatibility

### Adapter Version Declaration

Adapters SHOULD declare supported kernel version:

```python
def capabilities(self) -> dict:
    return {
        "supported_actions": [...],
        "hardware": "...",
        "version": "1.0",
        "kernel_version": "0.7.0",  # Supported kernel version
    }
```

### Compatibility Rules

- **Patch versions** (0.7.0 → 0.7.1): Always compatible
- **Minor versions** (0.7.0 → 0.8.0): Compatible unless noted
- **Major versions** (0.x → 1.0): May break compatibility

### Kernel Behavior

When adapter declares `kernel_version`:
- Kernel logs warning if version mismatch detected
- Execution continues (warning only, not error)
- Adapter responsible for handling differences

## Compatibility Levels

### Level 1: Interface Compatible
- Passes conformance tests
- Implements required methods
- Returns correct types

### Level 2: Semantically Compatible
- Actions have expected behavior
- WorldState accurately reflects environment
- ExecutionReport truthfully reports results

### Level 3: Production Compatible
- Tested in target environment
- Performance validated
- Safety verified
- Documentation complete

**Decision Kernel Compatible** = Level 1 (Interface Compatible)

Higher levels are adapter-specific commitments.

## Breaking Changes

Changes that break compatibility:

- Removing required fields from Action/WorldState
- Changing method signatures in Adapter contract
- Removing required keys from capabilities()
- Changing conformance test requirements

Non-breaking changes:

- Adding optional fields
- Adding new methods
- Adding new capability keys
- Improving validation

## Compatibility Badge

Use this badge in your adapter README:

```markdown
![Decision Kernel Compatible](https://img.shields.io/badge/Decision%20Kernel-Compatible-brightgreen)
```

Include verification command:
```bash
python -m decision_kernel_conformance your_module.YourAdapter
```

## Registry Requirements

To be listed in `registry/compatible_adapters.yaml`:

1. Pass conformance tests
2. Include README with usage examples
3. Include conformance command
4. Declare supported kernel version
5. Document scope and non-goals

## Compatibility Commitment

By declaring "Decision Kernel Compatible", you commit to:

- Maintaining interface adherence
- Updating for breaking changes
- Documenting version support
- Responding to compatibility issues

This is a **technical contract**, not a quality guarantee.

## Testing Compatibility

### Continuous Testing

Run conformance in CI:

```yaml
- name: Test conformance
  run: python -m decision_kernel_conformance your_module.YourAdapter
```

### Version Testing

Test against multiple kernel versions:

```yaml
strategy:
  matrix:
    kernel-version: ["0.6.0", "0.7.0"]
```

## Compatibility vs Quality

**Compatibility** = Interface adherence
**Quality** = Implementation excellence

Decision Kernel verifies compatibility.
Users verify quality.

## Questions

**Q: My adapter passes conformance but doesn't work well. Is it compatible?**
A: Yes. Compatibility is about interface, not quality.

**Q: Can I be compatible with multiple kernel versions?**
A: Yes. Test against each version and document support.

**Q: What if conformance tests change?**
A: Breaking changes will be announced. Adapters must update.

**Q: Is compatibility permanent?**
A: No. Adapters must maintain compatibility as kernel evolves.

## Summary

Decision Kernel Compatible means:
- ✓ Passes conformance tests
- ✓ Implements required interfaces
- ✓ Follows specifications

It does NOT mean:
- ✗ Production ready
- ✗ High quality
- ✗ Safe for use

Compatibility is necessary but not sufficient for production use.
