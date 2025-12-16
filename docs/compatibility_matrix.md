# Compatibility Matrix
**Generated**: 2025-12-16 22:31:51 UTC
**Kernel Version**: 0.9.0

## Reference Adapters

| Adapter | Hardware | Version | Conformance | Last Verified |
|---------|----------|---------|-------------|---------------|
| 🔵 decision-kernel-ros2 | ros2 | 1.0 | Not verified | N/A |
| 🔵 decision-kernel-webots | webots | 1.0 | Not verified | N/A |
| 🔵 decision-kernel-pybullet | pybullet | 1.0 | Not verified | N/A |
| 🔵 mock-robot | simulation | 1.0 | Not verified | N/A |

**Legend**:
- 🔵 Reference implementation (maintained by Decision Kernel team)
- 🟢 Community adapter

## Specifications

All adapters tested against:
- Action Specification v1.0
- WorldState Specification v1.0
- Adapter Contract v1.0

## Conformance Tests

Each adapter must pass 4/4 tests:
1. Method presence (sense, execute, capabilities)
2. sense() returns valid WorldState
3. execute() returns valid ExecutionReport
4. capabilities() returns required fields

## Verification

Conformance certificates are generated automatically and stored in `certificates/`.

To verify an adapter:
```bash
python -m decision_kernel_conformance <module.ClassName> --cert
```

## Multi-Environment Proof

Decision Kernel runs on:
- **ROS2** (middleware)
- **Webots** (simulation)
- **PyBullet** (physics)
- **Mock** (testing)

This demonstrates environment-agnostic design.
