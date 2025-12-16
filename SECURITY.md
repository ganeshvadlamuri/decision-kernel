# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in Decision Kernel, please report it by emailing:

**security@your-domain.com**

Please include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

## Response Timeline

- Initial response: within 48 hours
- Status update: within 7 days
- Fix timeline: depends on severity

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Security Considerations

Decision Kernel is infrastructure software. When deploying:

- Validate all human input before processing
- Review safety rules for your specific use case
- Audit adapter implementations for hardware safety
- Run with minimal privileges
- Monitor execution logs for anomalies

## Scope

Security issues in:
- Core kernel logic (brain/)
- Safety validation
- Memory/logging systems

Out of scope:
- Third-party adapters
- Hardware-specific implementations
- Deployment configurations
