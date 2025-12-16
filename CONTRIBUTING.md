# Contributing to Decision Kernel

## Development Setup

```bash
git clone https://github.com/your-org/decision-kernel.git
cd decision-kernel
pip install -e ".[dev]"
```

## Running Tests

```bash
pytest tests/
```

## Code Quality

Before submitting a PR:

```bash
# Format and lint
ruff check . --fix

# Type check
mypy brain/ cli/ adapters/ --ignore-missing-imports

# Run tests
pytest tests/
```

## Pull Request Guidelines

- Keep PRs focused on a single change
- Add tests for new functionality
- Ensure all tests pass
- Follow existing code style
- Update documentation as needed

## Architecture Rules

- **brain/** must remain hardware-agnostic (no ROS, no hardware drivers)
- **adapters/** contain all hardware/framework integrations
- No cloud service dependencies in core
- No hardcoded AI models

## Commit Messages

Use clear, descriptive commit messages:
- `fix: correct safety validation logic`
- `feat: add new action primitive`
- `docs: update architecture diagram`
- `test: add planner edge cases`
