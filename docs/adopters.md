# Decision Kernel Adopters

## Who Should Use Decision Kernel

### Research Labs

**Use Decision Kernel if you**:
- Develop planning or decision algorithms
- Need to test across simulators and hardware
- Want reproducible experiments
- Publish algorithms that others can use

**Benefits**:
- Hardware-agnostic algorithm development
- Easy transition from simulation to real robots
- Reproducible research (same kernel, different environments)
- Citation-ready infrastructure

**Example Use Cases**:
- Task planning research
- Human-robot interaction studies
- Multi-robot coordination
- Behavior synthesis

### Educational Institutions

**Use Decision Kernel if you**:
- Teach robotics courses
- Run robot programming workshops
- Need consistent interface across different robots
- Want students to focus on decision logic

**Benefits**:
- Students learn portable concepts
- Works with simulators (Webots, Gazebo via ROS2)
- Minimal setup complexity
- Clear separation of concerns

**Example Use Cases**:
- Undergraduate robotics courses
- Graduate seminars on planning
- Robot programming bootcamps
- Research training

### Robotics Companies

**Use Decision Kernel if you**:
- Build robot applications, not robots
- Need vendor-neutral decision layer
- Want to avoid hardware lock-in
- Develop for multiple robot platforms

**Benefits**:
- Portable decision logic across platforms
- Reduced vendor dependency
- Faster multi-platform development
- Clear architecture boundaries

**Example Use Cases**:
- Service robot applications
- Warehouse automation software
- Agricultural robot behaviors
- Inspection robot tasks

### Open Source Projects

**Use Decision Kernel if you**:
- Build robot behaviors or skills
- Want maximum compatibility
- Need stable, boring infrastructure
- Value vendor neutrality

**Benefits**:
- Stable interface (8 releases, zero breaking changes)
- Formal compatibility contracts
- Active conformance testing
- Community-driven governance

**Example Use Cases**:
- Reusable skill libraries
- Behavior composition frameworks
- Planning algorithm implementations
- Robot application frameworks

## Who Should Not Use Decision Kernel

### Hardware Manufacturers

**Do not use Decision Kernel if you**:
- Build vertically integrated systems
- Optimize for specific hardware
- Require proprietary decision logic
- Need hardware-specific optimizations

**Why not**:
- Decision Kernel is hardware-agnostic by design
- Optimizations belong in adapters, not kernel
- Vendor neutrality may conflict with differentiation

**Alternative**: Build proprietary decision layer, or contribute adapter.

### Real-Time Control Systems

**Do not use Decision Kernel if you**:
- Need microsecond-level control
- Implement low-level motor control
- Require hard real-time guarantees
- Optimize for control loop performance

**Why not**:
- Decision Kernel targets high-level decisions
- Not optimized for real-time performance
- Control belongs in hardware layer

**Alternative**: Use Decision Kernel for high-level decisions, dedicated controller for low-level control.

### Closed Commercial Systems

**Do not use Decision Kernel if you**:
- Require proprietary decision logic
- Cannot open-source adapter code
- Need vendor-specific features
- Optimize for single platform

**Why not**:
- Decision Kernel is open source (Apache 2.0)
- Adapters should be shareable
- Vendor neutrality is core principle

**Alternative**: Build proprietary system, or use Decision Kernel with private adapters.

### AI/ML-First Applications

**Do not use Decision Kernel if you**:
- Decisions are purely learned (end-to-end RL)
- No symbolic planning needed
- Optimize for neural network inference
- Require tight ML framework integration

**Why not**:
- Decision Kernel uses symbolic planning
- Not optimized for ML inference
- No built-in learning

**Alternative**: Use ML framework directly, or integrate ML planner with Decision Kernel.

## Early Adopters

Organizations and projects using Decision Kernel in research, education, or development.

### Research

*This section will be populated as research groups adopt Decision Kernel.*

**Criteria for listing**:
- Published paper citing Decision Kernel
- Open-source research code using Decision Kernel
- Public presentation or demo

### Education

*This section will be populated as educational institutions adopt Decision Kernel.*

**Criteria for listing**:
- Course using Decision Kernel
- Workshop or tutorial delivered
- Educational materials published

### Industry

*This section will be populated as companies adopt Decision Kernel.*

**Criteria for listing**:
- Public announcement of adoption
- Open-source adapter or skill
- Case study or blog post

### Open Source

*This section will be populated as open-source projects adopt Decision Kernel.*

**Criteria for listing**:
- Project using Decision Kernel
- Publicly available code
- Active maintenance

## Adoption Process

### 1. Evaluate Fit

- Read [Adoption Guide](adoption.md)
- Review [Whitepaper](papers/decision_kernel_whitepaper.md)
- Run demos (ROS2, Webots)

### 2. Prototype

- Implement minimal adapter
- Test conformance
- Validate with your use case

### 3. Integrate

- Replace or augment existing decision layer
- Maintain adapter
- Contribute improvements

### 4. Share (Optional)

- Publish adapter to registry
- Write case study
- Present at conference
- Add to adopters list

## How to Be Listed

### Requirements

1. **Public evidence** of adoption (paper, code, announcement)
2. **Active use** (not just evaluation)
3. **Conformant adapter** (passes 4/4 tests) OR educational use

### Process

1. Open GitHub issue with "Adopter Listing" template
2. Provide evidence (link to paper, repo, announcement)
3. Maintainers verify and add to list
4. Update annually to confirm continued use

### Benefits

- Visibility in Decision Kernel community
- Listed in documentation
- Mentioned in presentations
- Included in adoption metrics

## Adoption Metrics

*Metrics will be published as adoption grows.*

Planned metrics:
- Number of research papers citing Decision Kernel
- Number of courses using Decision Kernel
- Number of conformant adapters
- Number of GitHub stars/forks
- Number of active contributors

## Questions

**Q: Can I use Decision Kernel in commercial products?**  
A: Yes. Apache 2.0 license permits commercial use.

**Q: Do I need to open-source my adapter?**  
A: No. Adapters can be private. Registry listing requires public adapter.

**Q: Can I modify Decision Kernel?**  
A: Yes. Apache 2.0 permits modification. Consider contributing improvements.

**Q: How do I get support?**  
A: GitHub Discussions for community support. No commercial support currently.

**Q: Can I be listed without open-sourcing code?**  
A: Yes, if you have public evidence (paper, announcement, case study).

## Contact

- **GitHub Discussions**: For adoption questions
- **GitHub Issues**: For technical issues
- **Email**: See MAINTAINERS.md for maintainer contacts

---

**Note**: This list is maintained by the Decision Kernel community. Inclusion does not imply endorsement. Organizations are responsible for their own adoption decisions.
