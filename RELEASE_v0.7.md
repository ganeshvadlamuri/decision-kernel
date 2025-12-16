# Decision Kernel v0.7 - Release Notes

**Version**: 0.7.0  
**Release Date**: 2024-02-15  
**Theme**: Cross-Environment Inevitability

## Summary

Decision Kernel v0.7 proves multi-environment viability and formalizes compatibility as a technical contract.

**Key Statement**: "Decision Kernel runs on ROS2 and Webots."

## What's New

### Webots Adapter (Reference Implementation)

Second reference adapter demonstrating Decision Kernel in simulation environment.

- Full Adapter contract implementation
- Passes conformance tests (4/4)
- Translation layer for Webots simulator
- Minimal runnable demo (<5 seconds)
- Clear scope and non-goals

**Try it**:
```bash
cd decision-kernel-webots
python demo.py
```

### Compatibility Formalization

New documentation defining "Decision Kernel Compatible" as formal technical contract.

- Three compatibility levels (Interface, Semantic, Production)
- Version compatibility rules
- Breaking vs non-breaking change definitions
- Adapter version declaration in capabilities()

**Read**: [docs/compatibility.md](docs/compatibility.md)

### Reference Implementations Documentation

Comprehensive guide to reference adapters and skills.

- ROS2 Adapter (middleware)
- Webots Adapter (simulation)
- Mock Adapter (testing)
- Bring Water Skill (behavior)

**Read**: [docs/reference_implementations.md](docs/reference_implementations.md)

## Multi-Environment Proof

Decision Kernel now demonstrably runs on:

1. **ROS2** - Industry middleware standard
2. **Webots** - Academic/research simulator
3. **Mock** - Pure software testing

This proves:
- Environment agnosticism
- Middleware neutrality
- Hardware independence

## Compatibility

### Backward Compatibility

✅ **100% backward compatible** with v0.1-v0.6

- All existing code works unchanged
- No breaking API changes
- All 57 tests passing
- Zero kernel regressions

### Version Declaration

Adapters can now declare supported kernel version:

```python
def capabilities(self) -> dict:
    return {
        "kernel_version": "0.7.0",
        # ... other fields
    }
```

Kernel logs warning on version mismatch (non-blocking).

## Verification

All quality checks passing:

```bash
# Original CLI
python -m cli.run "bring me water"
✅ PASS

# Test suite
pytest tests/ -v
✅ 57/57 passing

# Linting
python -m ruff check .
✅ All checks passed

# Type checking
python -m mypy brain/ cli/ adapters/ --ignore-missing-imports
✅ Success: 34 files

# Conformance
python -m decision_kernel_conformance adapters.mock.mock_robot.MockRobot
✅ 4/4 tests passed
```

## Design Principles Maintained

✅ No kernel semantic changes  
✅ No ROS dependencies in brain/  
✅ No cloud services  
✅ No LLM integrations  
✅ No execution autonomy  
✅ Minimal core repository  

## Documentation

New documentation:
- [Compatibility Guide](docs/compatibility.md) - Formal compatibility definition
- [Reference Implementations](docs/reference_implementations.md) - Reference adapter/skill guide

Updated documentation:
- [README.md](README.md) - Added compatibility section
- [CHANGELOG.md](CHANGELOG.md) - Added v0.7.0 entry

## Registry

Updated [registry/compatible_adapters.yaml](registry/compatible_adapters.yaml):
- Added Webots adapter
- Added `status: reference` field
- Three reference adapters listed

## Migration Guide

### From v0.6 to v0.7

**No changes required**. v0.7 is fully backward compatible.

**Optional**: Add kernel version to adapter capabilities:

```python
def capabilities(self) -> dict:
    return {
        "supported_actions": [...],
        "hardware": "...",
        "version": "1.0",
        "kernel_version": "0.7.0",  # Optional: declare supported version
    }
```

## What This Means

### For Users
- Decision Kernel works in more environments
- Formal compatibility guarantees
- Clear reference implementations

### For Developers
- Multi-environment proof reduces risk
- Formal contracts enable confident integration
- Reference implementations provide patterns

### For Ecosystem
- Environment-agnostic standard
- Vendor-neutral infrastructure
- Inevitable adoption path

## Strategic Positioning

Decision Kernel v0.7 shifts perception:

**Before**: "Interesting ROS alternative"  
**After**: "Environment-agnostic infrastructure standard"

**Before**: Single environment proof  
**After**: Multi-environment proof

**Before**: Informal compatibility  
**After**: Formal technical contract

## Next Steps

### Try Webots Adapter
```bash
cd decision-kernel-webots
python demo.py
```

### Read Compatibility Guide
```bash
cat docs/compatibility.md
```

### Verify Your Adapter
```bash
python -m decision_kernel_conformance your_module.YourAdapter
```

## Community

- **Report issues**: GitHub Issues
- **Propose adapters**: Use issue template
- **Contribute**: See CONTRIBUTING.md
- **Discuss**: GitHub Discussions

## Credits

Decision Kernel is community-driven, vendor-neutral infrastructure.

See [GOVERNANCE.md](GOVERNANCE.md) for project governance.  
See [MAINTAINERS.md](MAINTAINERS.md) for maintainer list.

## License

Apache License 2.0

---

**Decision Kernel v0.7**: Boring, dependable, inevitable infrastructure.

**Statement**: Decision Kernel runs on ROS2 and Webots.

**Implication**: Decision Kernel is environment-agnostic standard.
