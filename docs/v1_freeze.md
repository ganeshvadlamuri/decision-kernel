# v1.0 Freeze Policy

**Status**: Active from v1.0 onward  
**Authority**: Project Governance  
**Scope**: Core kernel and specifications

## Core Freeze

From v1.0 onward, the following are **frozen**:

### Frozen Components

1. **Kernel Core** (`brain/` directory)
   - Intent parser interface
   - Planner interface
   - Safety validator interface
   - Memory interface
   - Kernel orchestration logic

2. **Data Specifications**
   - Action Specification v1.0
   - WorldState Specification v1.0
   - Adapter Contract v1.0

3. **Adapter Contract**
   - Method signatures (sense, execute, capabilities)
   - Return types
   - Required fields in capabilities()

4. **Compatibility Rules**
   - Conformance test requirements
   - Version compatibility policy
   - Breaking change definition

### What "Frozen" Means

**Frozen** means:
- No new methods added to core interfaces
- No method signatures changed
- No required fields added to dataclasses
- No behavior changes to existing functionality
- No API modifications

**Frozen does NOT mean**:
- No bug fixes (bugs will be fixed)
- No security patches (security is priority)
- No documentation improvements (docs can improve)
- No performance optimizations (if behavior-preserving)

## Allowed Changes Post-v1.0

### Always Allowed

1. **Bug Fixes**
   - Fixes to incorrect behavior
   - Fixes to specification violations
   - Fixes to conformance test failures

2. **Security Patches**
   - Vulnerability fixes
   - Dependency updates for security
   - Security-related behavior corrections

3. **Documentation**
   - Clarifications
   - Examples
   - Tutorials
   - Specifications (clarifying, not changing)

4. **Internal Implementation**
   - Performance improvements (behavior-preserving)
   - Code clarity improvements (behavior-preserving)
   - Test improvements

### Never Allowed

1. **Breaking Changes**
   - Removing methods
   - Changing method signatures
   - Removing required fields
   - Changing behavior of existing functionality

2. **New Core Features**
   - New kernel modules
   - New required methods
   - New required fields
   - New core functionality

3. **Scope Expansion**
   - Learning capabilities
   - Cloud integration
   - LLM integration
   - Execution autonomy

## Extension Points

All new functionality MUST use extension points:

### Adapters
- New adapters for new hardware/simulators
- Enhanced adapter capabilities
- Adapter-specific features

### Skills
- New skill definitions
- Skill libraries
- Skill composition tools

### Tooling
- Conformance testing enhancements
- Development tools
- Debugging utilities
- Visualization tools

### Ecosystem
- Demos
- Educational materials
- Integration examples
- Community contributions

## Change Request Process

### For Bug Fixes

1. Open GitHub issue with "bug" label
2. Demonstrate incorrect behavior
3. Propose minimal fix
4. Submit PR with tests
5. Maintainer review and merge

### For Security Patches

1. Follow SECURITY.md process
2. Private disclosure if needed
3. Minimal fix developed
4. Security advisory published
5. Patch released immediately

### For Documentation

1. Open GitHub issue or PR directly
2. Maintainer review
3. Merge if improves clarity

### For Proposed Changes

1. Open GitHub issue with detailed justification
2. Community discussion (minimum 30 days)
3. Maintainer consensus required
4. If breaking: Extraordinary consensus required
5. If approved: Careful implementation with migration path

## Extraordinary Consensus

Breaking changes require:
- Unanimous maintainer approval
- Community discussion (minimum 90 days)
- Demonstrated critical need
- Comprehensive migration path
- Major version bump (v2.0)

**Threshold**: Intentionally high. Breaking changes should be rare.

## Version Policy

### v1.x Releases

- v1.0: Initial stable release
- v1.1, v1.2, etc.: Bug fixes, security patches, documentation
- No breaking changes in v1.x series

### v2.0 (If Ever Needed)

- Requires extraordinary consensus
- Comprehensive migration guide
- Parallel maintenance of v1.x (minimum 2 years)
- Clear justification for breaking changes

## Rationale

### Why Freeze?

1. **Trust**: Users need stable foundation
2. **Investment**: Organizations invest in stable APIs
3. **Longevity**: Systems built on Decision Kernel last 10+ years
4. **Predictability**: No surprises, no churn
5. **Focus**: Innovation happens in ecosystem, not core

### Why Not Freeze?

Arguments against freezing:
- "We might need new features"
- "Technology evolves"
- "Competitors will innovate faster"

Responses:
- New features belong in ecosystem
- Core abstractions are timeless
- Stability is competitive advantage

### Historical Precedent

Successful frozen standards:
- POSIX (decades of stability)
- HTTP/1.1 (20+ years unchanged)
- SQL-92 (foundation still used)
- TCP/IP (core unchanged since 1981)

Decision Kernel follows this tradition.

## Enforcement

### Maintainer Responsibility

Maintainers MUST:
- Reject PRs that violate freeze policy
- Enforce freeze in code review
- Educate contributors on policy
- Protect core stability

### Community Responsibility

Community SHOULD:
- Respect freeze policy
- Propose extensions, not core changes
- Build on stable foundation
- Report violations

### Violation Consequences

Violations of freeze policy:
- PR rejected
- Issue closed with explanation
- Contributor educated on policy
- Repeated violations: Maintainer review

## Exceptions

No exceptions to freeze policy except:
- Critical security vulnerabilities
- Specification violations (bugs)
- Unanimous maintainer consensus + extraordinary process

## Review

This policy will be reviewed:
- Annually
- After any proposed breaking change
- When governance transitions to Steering Committee

Changes to this policy require:
- Maintainer consensus
- Community discussion (minimum 60 days)
- Clear justification

## Summary

**From v1.0 onward**:
- Core is frozen
- Specifications are frozen
- Adapter contract is frozen
- Extensions are encouraged
- Stability is paramount

**Decision Kernel v1.0+ is infrastructure you can trust for decades.**

---

**This policy is non-negotiable.**
