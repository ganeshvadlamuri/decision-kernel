---
name: New Adapter Proposal
about: Propose a new Decision Kernel compatible adapter
title: '[ADAPTER] '
labels: adapter, community
assignees: ''
---

## Adapter Information

**Name**: 
**Hardware/Platform**: 
**Repository**: 

## Description

Brief description of what this adapter does and what hardware it supports.

## Conformance

- [ ] Passes Action Specification v1.0
- [ ] Passes WorldState Specification v1.0
- [ ] Passes Adapter Contract (4/4 tests)
- [ ] Includes README with usage examples
- [ ] Includes conformance command

**Conformance command**:
```bash
python -m decision_kernel_conformance your_module.YourAdapter
```

## Supported Actions

List the actions your adapter supports:
- `navigate_to`
- `grasp`
- ...

## Registry Entry

```yaml
- name: your-adapter
  description: Brief description
  repository: https://github.com/user/repo
  conformance: "python -m decision_kernel_conformance your_module.YourAdapter"
  hardware: your_hardware
  version: "1.0"
  maintainer: Your Name
```

## Additional Context

Any additional information about the adapter.
