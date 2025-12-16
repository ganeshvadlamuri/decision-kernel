# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-12-16

### Released - Stability Milestone

Decision Kernel v1.0.0 formalizes the stability guaranteed since v0.9.

**This release introduces no behavioral changes.**

### What v1.0.0 Means

- Core kernel is frozen
- Specifications are frozen (Action v1.0, WorldState v1.0, Adapter Contract v1.0)
- Compatibility guarantees are active
- 10+ year interface stability commitment
- Safe to build long-lived systems on

### Multi-Environment Proof

- ROS2 (middleware)
- Webots (simulation)
- PyBullet (physics)
- Mock (testing)

### Automated Evidence

- Conformance certificates generated automatically
- Compatibility matrix published
- CI enforces conformance

### Post-v1.0 Policy

- Core changes require extraordinary consensus
- Default response to feature requests: "Out of scope. Core is frozen."
- Extensions via adapters, skills, tooling only
- Bug fixes, security patches, documentation allowed

### Technical Status

- All tests passing (57/57)
- Zero kernel modifications since v0.9
- Zero breaking changes
- Stable, boring, dependable

**This is a ceremonial release marking transition from development to long-term standard stewardship.**

## [0.9.x → v1.0 Candidate] - 2024-02-28

### Status: v1.0 Candidate

Decision Kernel has entered v1.0 Candidate status.

**What this means**:
- Core is frozen (no changes except critical bugs)
- Specifications are frozen (Action v1.0, WorldState v1.0, Adapter Contract v1.0)
- Stability guarantees are active now (not waiting for v1.0 release)
- v1.0 will be released upon adoption milestones (see docs/roadmap.md)

**What remains**:
- External validation (education, research, industry adoption)
- Not technical work (core is complete)

**Change policy**:
- Default response: No
- Exceptions: Critical bugs, security vulnerabilities, documentation

**See**: docs/v1_candidate.md

### Added
- v1.0 Candidate declaration (docs/v1_candidate.md)
- Candidate status in README
- Maintainer guidance for candidate phase

### Maintained
- Zero code changes
- Zero behavior changes
- All tests passing (57/57)
- Version remains 0.9.x (v1.0 not released yet)

## [0.9.0] - 2024-02-25

### Added - Preparing for v1.0: Core Freeze
- **v1.0 Freeze Policy** (docs/v1_freeze.md) - Defines what is frozen at v1.0
- **v1.0 Definition** (docs/v1_definition.md) - Guarantees and commitments
- **Stability Commitment** - Prominent README section on long-term stability

### v1.0 Preparation
- Core freeze policy established
- 10+ year compatibility commitment
- Breaking change policy defined (extraordinary consensus required)
- Extension points clarified (adapters, skills, tooling)
- Change request process documented

### Governance Updates
- Roadmap updated with v1.0 stability milestone statement
- Governance updated with breaking change policy
- Post-v1.0 change policy defined (default: no)

### Trust Signals
- Explicit 10+ year interface stability guarantee
- Clear statement: v1.0 is stability milestone, not feature milestone
- Commitment to backward compatibility in v1.x series
- Ecosystem innovation encouraged, core changes rare

### What v1.0 Will Mean
- Adapter contract frozen
- Data specifications frozen
- Conformance requirements frozen
- Kernel behavior frozen
- Only bug fixes, security patches, documentation allowed

### What Hasn't Changed
- Zero kernel behavior changes
- Zero API modifications
- All existing tests passing (57/57)
- No breaking changes
- Version remains 0.9.0 (v1.0 not released yet)

### Note

This release establishes freeze policy and stability commitments.
**v1.0 will be released when adoption criteria are met** (see docs/roadmap.md).

This is a **pre-announcement** of v1.0 stability commitment.

## [0.8.0] - 2024-02-20

### Added - External Legitimacy
- **Academic Whitepaper** (docs/papers/decision_kernel_whitepaper.md) - Citation-ready technical paper
- **Educational Materials** (docs/teaching/) - 60-minute tutorial and lab exercises
- **Adopters Guide** (docs/adopters.md) - Who should/shouldn't use Decision Kernel
- **Citation Metadata** (CITATION.cff) - Formal citation format for research
- **Roadmap** (docs/roadmap.md) - v1.0 criteria and direction
- **Governance Evolution** - Path from BDFL to Steering Committee

### Academic Positioning
- Formal problem definition and system model
- Comparison with ROS, Behavior Trees, planners
- Reproducible demonstrations (ROS2 + Webots)
- Prior art citations
- Academic tone (neutral, precise, no marketing)

### Educational Entry Point
- 60-minute lecture-style tutorial
- Hands-on lab exercises (5 labs + challenges)
- Student-focused learning materials
- Workshop-ready content
- University course integration guide

### Adoption Signals
- Clear guidance on who should/shouldn't adopt
- Early adopters section (research, education, industry)
- Adoption process documentation
- Listing criteria and process
- Contact information

### Governance Maturity
- v1.0 criteria defined (10 conditions, no dates)
- Steering Committee transition path
- Contributor diversity criteria
- Adoption threshold metrics
- Governance evolution process

### Institutional Readiness
- Citation-ready whitepaper
- Educational materials for courses
- Clear adopter guidance
- Formal governance path
- Community engagement structure

### Maintained
- Zero kernel regressions
- All existing tests passing (57/57)
- No breaking changes
- No kernel semantic changes
- Stable adapter contract
- Boring and dependable

## [0.7.0] - 2024-02-15

### Added - Cross-Environment Inevitability
- **Webots Adapter** (decision-kernel-webots/) - Second reference implementation
- **Compatibility Guide** (docs/compatibility.md) - Formal compatibility definition
- **Reference Implementations** (docs/reference_implementations.md) - Reference adapter/skill documentation
- **Version Compatibility** - Adapters declare supported kernel versions

### Webots Adapter
- Implements full Adapter contract
- Passes conformance tests (4/4)
- Translation layer for Webots simulator
- Separate repository structure (decision-kernel-webots/)
- Minimal runnable demo (<5 minutes)
- Clear scope and non-goals documented

### Compatibility Formalization
- docs/compatibility.md defines "Decision Kernel Compatible"
- Three compatibility levels: Interface, Semantic, Production
- Version compatibility rules (patch/minor/major)
- Breaking vs non-breaking change definitions
- Compatibility badge and verification process

### Reference Implementations
- ROS2 Adapter (middleware reference)
- Webots Adapter (simulation reference)
- Mock Adapter (testing reference)
- Bring Water Skill (behavior reference)
- Documentation explains reference implementation purpose

### Registry Updates
- Webots adapter added to compatible_adapters.yaml
- Reference status field added to registry entries
- Registry validation continues to pass

### Multi-Environment Proof
- Statement: "Decision Kernel runs on ROS2 and Webots"
- Demonstrates environment-agnostic design
- Proves middleware neutrality
- Validates cross-platform viability

### Maintained
- Zero kernel regressions
- All existing tests passing (57/57)
- No breaking changes
- No kernel semantic changes
- No ROS dependencies in brain/
- No cloud services or LLM integrations
- Stable adapter contract

## [0.6.0] - 2024-02-10

### Added - Adoption Acceleration
- **End-to-end ROS2 Demo** (demos/ros2_hello_world/) - Runnable in under 5 minutes
- **Ecosystem Kit** (decision-kernel-ecosystem-kit/) - Templates and publishing guide
- **Compatibility Registry** (registry/) - Community adapters and skills catalog
- **Adoption Guide** (docs/adoption.md) - Integration patterns and best practices
- **Issue Templates** - Structured adapter and skill proposals
- **Registry Verification** - Automated validation in CI
- **Makefile** - Common commands (demo-ros2, test, lint, typecheck)

### ROS2 Demo
- Simulated ROS2 topics (no ROS2 installation required)
- Full kernel pipeline demonstration
- Single command execution: `make demo-ros2`
- Clear output showing Intent → WorldState → Planning → Execution
- Windows-compatible (ASCII output)

### Ecosystem Kit
- Adapter template with TODO markers
- Skill template with test scaffolding
- Publishing checklist for adapters and skills
- Conformance testing guide
- Ready to split into separate repository

### Registry System
- registry/compatible_adapters.yaml - Community adapter catalog
- registry/compatible_skills.yaml - Community skill catalog
- tools/verify_registry.py - Format validation
- CI integration for registry verification
- Initial entries: ROS2 adapter, MockRobot, bring-water skill

### Community Onboarding
- .github/ISSUE_TEMPLATE/adapter_proposal.md
- .github/ISSUE_TEMPLATE/skill_proposal.md
- docs/adoption.md with integration patterns
- Clear path from stranger to contributor

### Enhanced
- Intent parser now handles generic "bring" commands (not just "bring water")
- README updated with v0.6 features and ecosystem links
- CI workflow includes registry verification step

### Maintained
- Zero kernel regressions
- All existing tests passing (57/57)
- No breaking changes
- No cloud services or LLM dependencies
- Minimal core repository (no bloat in brain/)

## [0.5.0] - 2024-02-05

### Added - Reference Standard
- **ROS2 Adapter** (decision-kernel-ros2/) - Real external adapter, translation layer only
- **Governance** (GOVERNANCE.md) - Community-driven, vendor-neutral governance model
- **Maintainers** (MAINTAINERS.md) - Clear maintainer structure
- **Technical Vision** (docs/vision.md) - "Why Robot Brains Need a Kernel"
- **Compatibility Badge** - Clear definition of Decision Kernel Compatible
- Neutrality statement in README

### ROS2 Adapter
- Implements full Adapter contract
- Passes conformance tests
- Translation layer only (no hardware control)
- Separate repository structure (decision-kernel-ros2/)
- Clear scope and non-goals documented

### Governance & Neutrality
- BDFL model with community maintainer path
- Vendor-neutral commitment
- Clear decision-making process
- Contribution guidelines

### Vision
- Technical essay for senior engineers
- Explains separation of concerns
- Positions Decision Kernel as infrastructure standard
- Clear non-goals and principles

### Credibility Signals
- "Decision Kernel runs on ROS2" (via adapter)
- Compatible adapter list in README
- Conformance verification process
- Professional governance structure

### Maintained
- Zero kernel regressions
- All existing tests passing (57/57)
- No breaking changes
- Stable API preserved
- No ROS dependencies in brain/

## [0.4.0] - 2024-01-30

### Added
- Adapter template (templates/adapter-python/) for quick adapter development
- Skill template (templates/skill/) for quick skill creation
- Conformance runner: `python -m decision_kernel_conformance <adapter>`
- Conformance documentation (docs/conformance.md)
- Capability negotiation: kernel checks adapter capabilities before execution
- Standard capability keys in adapter contract
- 4 new capability gating tests
- README badges (CI, ruff, mypy, Python, license)
- Quick start section in README

### Changed
- RobotBrainKernel: added optional `adapter` parameter
- Kernel validates plan actions against adapter capabilities
- Adapter contract: standardized capability keys (supported_actions, hardware, version)

### Developer Experience
- Templates make it trivial to create compatible adapters and skills
- Conformance runner provides instant feedback on adapter compatibility
- Capability gating prevents runtime errors from unsupported actions

### Maintained
- Full backward compatibility with v0.1-v0.3
- All existing tests passing (53 + 4 new = 57 total)
- No ROS or hardware dependencies
- Stable kernel API

## [0.3.0] - 2024-01-25

### Added
- Action specification v1.0 (docs/action_spec.md)
- WorldState specification v1.0 (docs/world_state_spec.md)
- Adapter contract v1.0 (docs/adapter_contract.md)
- Action validation utilities (brain/planner/validate_actions.py)
- WorldState validation utilities (brain/world/validate.py)
- Adapter base contract (adapters/base.py)
- ExecutionReport and ActionResult structures (brain/execution/report.py)
- 30 new conformance tests for specs and contracts

### Changed
- Action dataclass: added `parameters` dict and `version` field
- WorldState dataclass: added `timestamp`, `frame_id`, and `relations` fields
- MockRobot: now implements full Adapter contract with sense(), execute(), capabilities()

### Maintained
- Full backward compatibility with v0.1-v0.2
- All existing tests passing (23 + 30 new = 53 total)
- No ROS or hardware dependencies
- Clean architecture boundaries
- Stable kernel API

## [0.2.0] - 2024-01-20

### Added
- Skill system for reusable behavior templates
- `brain/skills/` module with Skill dataclass and SkillRegistry
- Optional skill_registry parameter in RobotBrainKernel and Planner
- Built-in "bring" reference skill
- Skill specification documentation (docs/skill_spec.md)
- Pick-and-place example (examples/pick_and_place.yaml)
- Comprehensive skill tests (8 new tests)

### Changed
- Planner now checks skill registry before fallback to naive planning
- Kernel accepts optional skill_registry parameter

### Maintained
- Backward compatibility: existing behavior unchanged without skills
- No ROS or hardware dependencies
- All existing tests passing
- Clean architecture boundaries

## [0.1.0] - 2024-01-15

### Added
- Initial public release of Decision Kernel
- Core orchestration pipeline: Intent → Planning → Safety → Memory
- Intent parser with rule-based goal extraction
- Naive symbolic planner for action sequence generation
- Safety validator with constraint checking
- In-memory execution history storage
- Mock robot adapter for testing
- CLI interface for command execution
- Comprehensive test suite
- CI/CD with GitHub Actions
- Code quality tooling (ruff, mypy)
- Documentation and contributor guidelines

### Architecture
- Hardware-agnostic kernel design
- Clean separation between brain/ and adapters/
- No ROS dependencies in core
- No cloud service requirements
- No hardcoded AI models

[0.1.0]: https://github.com/your-org/decision-kernel/releases/tag/v0.1.0
