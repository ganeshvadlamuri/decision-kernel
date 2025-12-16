# Decision Kernel v1.0.0 Release

**Date**: December 16, 2024  
**Type**: Stability Milestone  
**Status**: Released

## Summary

Decision Kernel v1.0.0 formalizes the stability guaranteed since v0.9.

The core kernel, specifications, and contracts are frozen.
This release introduces no behavioral changes.

Decision Kernel v1.0.0 is intended as long-term, stable infrastructure
for robot decision-making across environments.

## Verified Environments

- **ROS2** (middleware)
- **Webots** (simulation)
- **PyBullet** (physics)
- **Mock** (testing)

## Compatibility

Compatibility is enforced via automated conformance testing
and published compatibility certificates.

See: `docs/compatibility_matrix.md`

## What v1.0.0 Means

### For Users

- **Stable for 10+ years**: No breaking changes in v1.x series
- **Safe to build on**: Long-lived systems protected
- **Safe to teach with**: Course materials remain valid
- **Safe to cite**: Research reproducibility guaranteed

### For Developers

- **Frozen core**: No API changes
- **Frozen specs**: Action v1.0, WorldState v1.0, Adapter Contract v1.0
- **Predictable**: No surprises, no churn
- **Boring**: In the best possible way

### For Ecosystem

- **Extensions encouraged**: Adapters, skills, tooling
- **Core changes rare**: Extraordinary consensus required
- **Innovation at edges**: Not in core

## Post-v1.0 Policy

### Allowed

- Critical bug fixes
- Security patches
- Documentation clarifications
- Registry updates (adapters, skills)

### Not Allowed

- New features in core
- API modifications
- Behavior changes
- Scope expansion

### Default Response

Feature requests: **"Out of scope. Core is frozen."**

Extensions: **"Build an adapter/skill/tool."**

## Technical Status

- **Tests**: 57/57 passing
- **Kernel modifications**: Zero since v0.9
- **Breaking changes**: Zero
- **Behavioral changes**: Zero

## Transition

This release marks the transition from:
- Development → Long-term standard stewardship
- Evolving project → Stable infrastructure
- Candidate → Released standard

## Verification

All v1.0.0 guarantees were active during candidate phase.
This release is ceremonial, not technical.

## Resources

- [v1.0 Definition](docs/v1_definition.md) - What v1.0 guarantees
- [Freeze Policy](docs/v1_freeze.md) - What is frozen
- [Compatibility Guide](docs/compatibility.md) - Formal compatibility
- [Compatibility Matrix](docs/compatibility_matrix.md) - Verified adapters
- [Roadmap](docs/roadmap.md) - Future direction

## Acknowledgments

Decision Kernel is community-driven, vendor-neutral infrastructure.

See GOVERNANCE.md and MAINTAINERS.md.

---

**Decision Kernel v1.0.0: Stable, boring, dependable infrastructure.**
