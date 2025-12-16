"""Generate compatibility matrix from registry and certificates"""

import json
from datetime import datetime
from pathlib import Path

import yaml


def load_registry():
    """Load compatible adapters registry"""
    registry_file = Path("registry/compatible_adapters.yaml")
    if not registry_file.exists():
        return []

    with open(registry_file) as f:
        data = yaml.safe_load(f)

    return data.get("adapters", [])


def load_latest_certificate(adapter_name: str):
    """Load latest certificate for adapter"""
    cert_dir = Path("certificates") / adapter_name
    if not cert_dir.exists():
        return None

    # Find latest JSON certificate
    json_files = list(cert_dir.glob("*.json"))
    if not json_files:
        return None

    latest = max(json_files, key=lambda p: p.stat().st_mtime)

    with open(latest) as f:
        return json.load(f)


def generate_matrix():
    """Generate compatibility matrix markdown"""
    adapters = load_registry()

    output = []
    output.append("# Compatibility Matrix\n")
    output.append("**Generated**: " + datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC") + "\n")
    output.append("**Kernel Version**: 0.9.0\n")
    output.append("\n")
    output.append("## Reference Adapters\n")
    output.append("\n")
    output.append("| Adapter | Hardware | Version | Conformance | Last Verified |\n")
    output.append("|---------|----------|---------|-------------|---------------|\n")

    for adapter in adapters:
        name = adapter.get("name", "Unknown")
        hardware = adapter.get("hardware", "Unknown")
        version = adapter.get("version", "Unknown")
        status = adapter.get("status", "community")

        # Try to load certificate
        cert = load_latest_certificate(name)
        if cert:
            conformance = cert["results"]["status"]
            passed = cert["results"]["passed"]
            total = cert["results"]["total"]
            timestamp = cert["timestamp"][:10]  # Just date
            conformance_str = f"{conformance} ({passed}/{total})"
        else:
            conformance_str = "Not verified"
            timestamp = "N/A"

        badge = "🔵" if status == "reference" else "🟢"
        output.append(f"| {badge} {name} | {hardware} | {version} | {conformance_str} | {timestamp} |\n")

    output.append("\n")
    output.append("**Legend**:\n")
    output.append("- 🔵 Reference implementation (maintained by Decision Kernel team)\n")
    output.append("- 🟢 Community adapter\n")
    output.append("\n")

    output.append("## Specifications\n")
    output.append("\n")
    output.append("All adapters tested against:\n")
    output.append("- Action Specification v1.0\n")
    output.append("- WorldState Specification v1.0\n")
    output.append("- Adapter Contract v1.0\n")
    output.append("\n")

    output.append("## Conformance Tests\n")
    output.append("\n")
    output.append("Each adapter must pass 4/4 tests:\n")
    output.append("1. Method presence (sense, execute, capabilities)\n")
    output.append("2. sense() returns valid WorldState\n")
    output.append("3. execute() returns valid ExecutionReport\n")
    output.append("4. capabilities() returns required fields\n")
    output.append("\n")

    output.append("## Verification\n")
    output.append("\n")
    output.append("Conformance certificates are generated automatically and stored in `certificates/`.\n")
    output.append("\n")
    output.append("To verify an adapter:\n")
    output.append("```bash\n")
    output.append("python -m decision_kernel_conformance <module.ClassName> --cert\n")
    output.append("```\n")
    output.append("\n")

    output.append("## Multi-Environment Proof\n")
    output.append("\n")
    output.append("Decision Kernel runs on:\n")
    output.append("- **ROS2** (middleware)\n")
    output.append("- **Webots** (simulation)\n")
    output.append("- **PyBullet** (physics)\n")
    output.append("- **Mock** (testing)\n")
    output.append("\n")
    output.append("This demonstrates environment-agnostic design.\n")

    return "".join(output)


def main():
    """Generate and save compatibility matrix"""
    matrix = generate_matrix()

    output_file = Path("docs/compatibility_matrix.md")
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(matrix)

    print(f"Compatibility matrix generated: {output_file}")


if __name__ == "__main__":
    main()
