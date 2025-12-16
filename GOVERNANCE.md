# Governance

## Philosophy

Decision Kernel is infrastructure, not a product. It is community-driven, vendor-neutral, and hardware-agnostic.

## Model

Decision Kernel follows a **Benevolent Dictator For Life (BDFL)** model with a path to Steering Committee governance.

### Current: BDFL Model

Single decision-maker with community maintainer input.

**Advantages**:
- Fast decisions
- Clear direction
- Consistent vision

**Limitations**:
- Single point of failure
- Limited perspective
- Scalability concerns

### Future: Steering Committee

Decision Kernel will transition to Steering Committee governance when:

1. **Adoption threshold met**:
   - 5+ organizations actively using
   - 3+ universities teaching with Decision Kernel
   - 10+ community adapters in registry

2. **Contributor diversity achieved**:
   - 10+ active contributors
   - 3+ organizations contributing
   - Geographic diversity

3. **Governance readiness**:
   - Documented decision processes
   - Conflict resolution procedures
   - Maintainer succession plan

**Steering Committee composition** (when formed):
- 5-7 members
- Representing: Academia, Industry, Open Source, Maintainers
- Term: 2 years, staggered
- Selection: Community nomination + vote

**Steering Committee responsibilities**:
- Strategic direction
- Major technical decisions
- Maintainer appointments
- Governance evolution
- Conflict resolution

## Maintainership

### Current Maintainers

See [MAINTAINERS.md](MAINTAINERS.md) for the current list.

### Adding Maintainers

Maintainers are added based on:
- Sustained, high-quality contributions
- Deep understanding of kernel architecture
- Commitment to stability and neutrality
- Alignment with project philosophy

Maintainers have:
- Commit access to the repository
- Authority to review and merge pull requests
- Responsibility to uphold project standards

### Removing Maintainers

Maintainers may step down voluntarily or be removed for:
- Sustained inactivity (6+ months)
- Violation of Code of Conduct
- Actions contrary to project neutrality

## Decision Making

### Technical Decisions

- **Minor changes** (bug fixes, docs, tests): Any maintainer may merge
- **Major changes** (API changes, new modules): Require discussion and consensus
- **Breaking changes**: Require strong justification and migration path

### Principles

1. **Stability over features** - The kernel API must remain stable
2. **Neutrality over convenience** - No vendor lock-in
3. **Simplicity over cleverness** - Boring code wins
4. **Specs over implementations** - Contracts matter more than code
5. **Permanence over progress** - Core changes are rare (post-v1.0)

## Contribution Process

1. Open an issue for discussion (for non-trivial changes)
2. Submit a pull request
3. Pass all tests and quality checks
4. Receive maintainer review
5. Address feedback
6. Merge when approved

## Conflict Resolution

In case of disagreement:
1. Discussion in GitHub issues
2. Maintainer consensus
3. BDFL decision if consensus cannot be reached

## v1.0 Candidate Phase

**Status**: Active (see docs/v1_candidate.md)

**Decision policy during candidate phase**:

**Default response to change requests**: No

**Critical bugs**:
- Incorrect behavior vs specification
- Conformance test failures
- Data corruption or loss
- Process: Issue → Minimal fix → PR → Merge

**Security vulnerabilities**:
- Follow SECURITY.md
- Immediate patch
- No discussion delay

**Documentation**:
- Clarifications allowed
- Examples allowed
- Corrections allowed
- No specification changes

**Not allowed**:
- Feature requests (rejected immediately)
- API improvements (rejected)
- Convenience additions (rejected)
- Refactoring (rejected unless critical bug)
- Performance optimizations (rejected unless critical)

**Maintainer responsibility**: Protect stability. Default to "no".

## Breaking Changes (Post-v1.0)

Breaking changes to core require **extraordinary consensus**:

**Process**:
1. GitHub issue with detailed justification
2. Community discussion (minimum 90 days)
3. Unanimous maintainer approval
4. Demonstrated critical need
5. Comprehensive migration path
6. Major version bump (v2.0)

**Threshold**: Intentionally high. Breaking changes should be extremely rare.

**Default answer**: No

**Rationale**: Stability is more valuable than features. Users depend on unchanging interfaces for 10+ years.

**See**: docs/v1_freeze.md for complete policy

## Neutrality Commitment

Decision Kernel will never:
- Favor specific hardware vendors
- Require cloud services
- Include proprietary dependencies
- Implement vendor-specific features in core

Vendor-specific integrations belong in separate adapter repositories.

## Transition Process

### From BDFL to Steering Committee

When transition criteria are met:

1. **Announcement** (3 months notice)
2. **Nomination period** (1 month)
3. **Community review** (1 month)
4. **Election** (if needed)
5. **Transition** (1 month handover)

### Criteria Tracking

Progress toward Steering Committee tracked in:
- docs/roadmap.md (adoption metrics)
- MAINTAINERS.md (contributor diversity)
- GitHub Discussions (community engagement)

## Evolution

This governance model will evolve as the project grows. Changes to governance require:
- Public discussion (minimum 1 month)
- Maintainer consensus (or BDFL decision)
- Clear documentation
- Community notification

## Contact

For governance questions: Open a GitHub issue with the `governance` label.
