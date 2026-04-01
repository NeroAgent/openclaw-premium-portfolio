#!/usr/bin/env python3
"""
Resource Check — Main orchestrator for system resource diagnostics.

Runs configured checks and outputs recommendations.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

# Import check modules (they'll be in the same directory)
SCRIPT_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(SCRIPT_DIR))

def run_check(module_name, *args):
    """Run a check module and return its result dict."""
    try:
        module = __import__(module_name)
        return module.check(*args)
    except Exception as e:
        return {
            "error": str(e),
            "status": "error"
        }

def format_output(results, format="text"):
    """Format results for human or machine consumption."""
    if format == "json":
        return json.dumps(results, indent=2)

    # Text format
    lines = ["=== Resource Check Report ==="]
    for key, data in results.items():
        if key in ("recommendation", "recommendation_reason"):
            if key == "recommendation":
                lines.append(f"\n📋 Overall: {data}")
            if key == "recommendation_reason":
                lines.append(f"   Reason: {data}")
            continue
        lines.append(f"\n{key.upper()}:")
        if not isinstance(data, dict):
            lines.append(f"  ❌ Invalid data: {data}")
            continue
        if "error" in data:
            lines.append(f"  ❌ Error: {data['error']}")
        else:
            for k, v in data.items():
                if k not in ["status", "details", "reason"]:
                    lines.append(f"  {k}: {v}")
            status = data.get("status", "ok")
            if status == "ok":
                lines.append("  ✅ OK")
            elif status == "warning":
                lines.append(f"  ⚠️  Warning: {data.get('reason', '')}")
            elif status == "critical":
                lines.append(f"  ❌ Critical: {data.get('reason', '')}")
            elif status == "error":
                lines.append(f"  ❌ Error: {data.get('error', 'Unknown')}")
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="Check system resources")
    parser.add_argument("checks", nargs="*", default=["all"],
                        help="Checks to run: ram, storage, cpu, battery, network, or all")
    parser.add_argument("--output", choices=["text", "json"], default="text",
                        help="Output format")
    parser.add_argument("--min-ram-free", type=str, default="500M",
                        help="Minimum free RAM (e.g., 500M, 1G)")
    parser.add_argument("--min-storage-free", type=str, default="2G",
                        help="Minimum free storage")
    parser.add_argument("--min-battery", type=int, default=20,
                        help="Minimum battery percentage")
    args = parser.parse_args()

    # Parse human-friendly sizes (simple version)
    def parse_size(s):
        s = str(s).strip().upper()
        multipliers = {"K": 1024, "M": 1024**2, "G": 1024**3}
        if s[-1] in multipliers:
            return int(float(s[:-1]) * multipliers[s[-1]])
        return int(s)

    min_ram_free_bytes = parse_size(args.min_ram_free)
    min_storage_free_bytes = parse_size(args.min_storage_free)
    min_battery = args.min_battery

    results = {}
    checks_to_run = args.checks if "all" not in args.checks else ["ram", "storage", "cpu", "battery", "network"]

    if "ram" in checks_to_run:
        results["ram"] = run_check("ram")
    if "storage" in checks_to_run:
        results["storage"] = run_check("storage")
    if "cpu" in checks_to_run:
        results["cpu"] = run_check("cpu")
    if "battery" in checks_to_run:
        results["battery"] = run_check("battery")
    if "network" in checks_to_run:
        results["network"] = run_check("network")

    # Generate recommendation
    recommendation = "PROCEED"
    reasons = []
    for key, data in results.items():
        if data.get("status") == "critical":
            recommendation = "STOP"
            reasons.append(f"{key}: {data.get('reason')}")
        elif data.get("status") == "warning" and recommendation != "STOP":
            recommendation = "CAUTION"
            reasons.append(f"{key}: {data.get('reason')}")

    results["recommendation"] = recommendation
    if recommendation == "PROCEED":
        results["recommendation_reason"] = "All checks passed."
    elif recommendation == "CAUTION":
        results["recommendation_reason"] = "; ".join(reasons)
    else:
        results["recommendation_reason"] = "; ".join(reasons)

    print(format_output(results, args.output))
    sys.exit(0 if recommendation != "STOP" else 1)

if __name__ == "__main__":
    main()
