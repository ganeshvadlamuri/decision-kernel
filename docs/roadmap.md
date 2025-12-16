# Decision Kernel Roadmap

**Status**: Living document  
**Last Updated**: February 2024

## Principles

1. **Stability over features** - No breaking changes without major version
2. **Boring is good** - Predictable, dependable infrastructure
3. **Community-driven** - Decisions reflect adopter needs
4. **Vendor-neutral** - No single organization controls direction

## Current Status (v0.8)

### Stable
- Core kernel (Intent → Planning → Safety → Memory)
- Adapter contract (sense, execute, capabilities)
- Data specifications (Action v1.0, WorldState v1.0)
- Conformance testing (4/4 tests)
- Reference implementations (ROS2, Webots, Mock)

### Proven
- Multi-environment viability (ROS2, Webots, Mock)
- Zero breaking changes across 8 releases
- 57/57 tests passing
- Formal compatibility contracts

## v0.x Stabilization

### Goals

**Interface Stability**:
- No breaking changes to adapter contract
- No breaking changes to data specifications
- Backward compatibility maintained

**Ecosystem Growth**:
- Community adapters beyond reference implementations
- Community skills beyond built-in examples
- Educational adoption (courses, workshops)
- Research adoption (papers, citations)

**Documentation Maturity**:
- Complete specification coverage
- Educational materials
- Adoption case studies
- Performance characteristics

### Non-Goals

- Feature additions to core kernel
- New planning algorithms in core
- Built-in ML/AI capabilities
- Real-time performance optimization

## v1.0 Criteria

**IMPORTANT**: v1.0 is a **stability milestone**, not a feature milestone.

v1.0 signals:
- Core is frozen (see docs/v1_freeze.md)
- Interfaces are stable for 10+ years
- Safe to build long-lived systems on
- Commitment to backward compatibility

v1.0 does NOT signal:
- Feature completeness
- Perfection
- End of development
- No more improvements

Decision Kernel will reach v1.0 when ALL of the following conditions are met:

### Technical Criteria

1. **Interface Stability**
   - Adapter contract unchanged for 6+ months
   - Data specifications unchanged for 6+ months
   - All conformance tests passing
   - Zero known breaking bugs

2. **Multi-Environment Proof**
   - 3+ reference implementations maintained
   - 5+ community adapters in registry
   - Demonstrated on real hardware (not just simulation)

3. **Specification Completeness**
   - All interfaces formally specified
   - All specifications versioned
   - All specifications tested
   - Migration guides for all versions

### Adoption Criteria

4. **Educational Adoption**
   - 3+ universities using in courses
   - 5+ workshops or tutorials delivered
   - Educational materials published

5. **Research Adoption**
   - 5+ papers citing Decision Kernel
   - 3+ research groups actively using
   - Research code publicly available

6. **Industry Validation**
   - 2+ companies using in development
   - 1+ production deployment
   - Case studies published

### Community Criteria

7. **Contributor Diversity**
   - 10+ contributors beyond founding team
   - 3+ organizations contributing
   - Active community discussions

8. **Governance Maturity**
   - Steering committee established
   - Decision-making process documented
   - Conflict resolution process defined
   - Maintainer succession plan

### Documentation Criteria

9. **Complete Documentation**
   - All specifications published
   - All APIs documented
   - Migration guides complete
   - Performance characteristics documented

10. **Quality Assurance**
    - 90%+ test coverage
    - All reference implementations conformant
    - Security audit completed
    - Performance benchmarks published

## Post-1.0 Direction

### Change Policy

**Post-v1.0, core changes require**:
- Demonstrated critical need
- Community discussion (minimum 30 days)
- Maintainer consensus
- If breaking: Extraordinary consensus (see docs/v1_freeze.md)

**Default answer to change requests**: No (unless bug, security, or documentation)

**Rationale**: Stability is more valuable than features

### Potential Areas (Not Commitments)

**Advanced Planning**:
- Integration with PDDL planners
- Probabilistic planning support
- Learning-based planner integration

**Formal Verification**:
- Temporal logic specifications
- Model checking integration
- Safety property verification

**Multi-Robot**:
- Distributed decision-making
- Conflict resolution
- Resource allocation

**Standardization**:
- IEEE/ISO specification process
- Industry working group
- Academic consortium

**Performance**:
- Real-time optimization
- Distributed execution
- Scalability improvements

### What Will NOT Change

- Hardware-agnostic principle
- Vendor-neutral governance
- Separation of concerns (decision vs execution)
- Minimal core philosophy
- Adapter-based architecture

## Timeline

**No dates are provided intentionally.**

Decision Kernel will reach v1.0 when criteria are met, not when a date arrives.

**Current focus**: v0.x stabilization and adoption growth.

**v1.0 preparation**: Establishing freeze policy and stability commitments.

## How to Influence Roadmap

### For Adopters

1. **Use Decision Kernel** - Adoption drives priorities
2. **Report issues** - Bug reports improve stability
3. **Share use cases** - Real-world needs shape direction
4. **Contribute adapters** - Ecosystem growth validates design

### For Contributors

1. **Fix bugs** - Stability is priority
2. **Improve documentation** - Clarity enables adoption
3. **Add tests** - Quality assurance matters
4. **Review PRs** - Community review improves quality

### For Researchers

1. **Cite Decision Kernel** - Academic validation matters
2. **Publish research code** - Reproducibility helps community
3. **Share results** - Performance data informs decisions
4. **Propose improvements** - Research insights welcome

### For Companies

1. **Deploy Decision Kernel** - Production use validates design
2. **Share case studies** - Real-world validation helps community
3. **Contribute adapters** - Ecosystem growth benefits all
4. **Fund development** - Sponsorship accelerates progress

## Governance

Roadmap decisions follow governance process defined in GOVERNANCE.md.

**Current model**: BDFL (Benevolent Dictator For Life)  
**Future model**: Steering Committee (when criteria met)

See GOVERNANCE.md for details.

## Questions

**Q: When will v1.0 be released?**  
A: When all v1.0 criteria are met. No date set.

**Q: Can I propose new features?**  
A: Yes. Open GitHub issue with proposal. Evaluated against principles.

**Q: Will there be breaking changes before v1.0?**  
A: No. Backward compatibility maintained in v0.x.

**Q: What happens after v1.0?**  
A: Continued stability, ecosystem growth, potential advanced features.

**Q: How do I track progress?**  
A: GitHub milestones, CHANGELOG.md, community discussions.

## Updates

This roadmap is updated quarterly or when significant changes occur.

**Next review**: May 2024

---

**Remember**: Decision Kernel is infrastructure, not a product. Stability and adoption matter more than features.
