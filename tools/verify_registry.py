"""Verify registry files are valid"""

import sys
from pathlib import Path

import yaml


def verify_adapters(data: dict) -> list[str]:
    """Verify adapters registry format"""
    errors = []

    if "adapters" not in data:
        return ["Missing 'adapters' key"]

    for i, adapter in enumerate(data["adapters"]):
        required = ["name", "description", "repository", "conformance", "hardware", "version"]
        for field in required:
            if field not in adapter:
                errors.append(f"Adapter {i}: missing required field '{field}'")

        # Validate conformance command format
        if "conformance" in adapter:
            cmd = adapter["conformance"]
            if not cmd.startswith("python -m decision_kernel_conformance"):
                errors.append(f"Adapter {i} ({adapter.get('name', 'unknown')}): conformance command must start with 'python -m decision_kernel_conformance'")

    return errors


def verify_skills(data: dict) -> list[str]:
    """Verify skills registry format"""
    errors = []

    if "skills" not in data:
        return ["Missing 'skills' key"]

    for i, skill in enumerate(data["skills"]):
        required = ["name", "description", "repository", "intent_pattern", "version"]
        for field in required:
            if field not in skill:
                errors.append(f"Skill {i}: missing required field '{field}'")

    return errors


def main():
    """Verify all registry files"""
    registry_dir = Path(__file__).parent.parent / "registry"

    all_errors = []

    # Verify adapters
    adapters_file = registry_dir / "compatible_adapters.yaml"
    if not adapters_file.exists():
        all_errors.append(f"Missing file: {adapters_file}")
    else:
        with open(adapters_file) as f:
            data = yaml.safe_load(f)
        errors = verify_adapters(data)
        if errors:
            all_errors.extend([f"compatible_adapters.yaml: {e}" for e in errors])

    # Verify skills
    skills_file = registry_dir / "compatible_skills.yaml"
    if not skills_file.exists():
        all_errors.append(f"Missing file: {skills_file}")
    else:
        with open(skills_file) as f:
            data = yaml.safe_load(f)
        errors = verify_skills(data)
        if errors:
            all_errors.extend([f"compatible_skills.yaml: {e}" for e in errors])

    if all_errors:
        print("Registry validation FAILED:")
        for error in all_errors:
            print(f"  - {error}")
        sys.exit(1)

    print("Registry validation PASSED")
    print(f"  Adapters: {len(data.get('adapters', []))} entries")
    print(f"  Skills: {len(data.get('skills', []))} entries")


if __name__ == "__main__":
    main()
