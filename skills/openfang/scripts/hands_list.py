#!/usr/bin/env python3
"""
openfang hands list — List available Hands.
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

def find_openfang_bin():
    bin_path = os.environ.get("OPENFANG_BIN", "openfang")
    for path in [f"{os.environ.get('HOME')}/.cargo/bin/openfang", "/usr/local/bin/openfang"]:
        if os.path.isfile(path):
            return path
    return None

def main():
    parser = argparse.ArgumentParser(description="List available Hands")
    parser.add_argument("--output", choices=["text", "json"], default="text")
    args = parser.parse_args()

    openfang = find_openfang_bin()
    if not openfang:
        print("[ERROR] openfang binary not found", file=sys.stderr)
        return 1

    try:
        result = subprocess.run([openfang, "hands", "list"], capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            print(f"[ERROR] {result.stderr}", file=sys.stderr)
            return 1
        lines = result.stdout.strip().split("\n")
        # Parse text output (assumes simple list)
        hands = []
        for line in lines:
            if line.strip():
                parts = line.split()
                if len(parts) >= 1:
                    name = parts[0]
                    enabled = "enabled" in line.lower()
                    hands.append({"name": name, "enabled": enabled})
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1

    if args.output == "json":
        print(json.dumps({"hands": hands}, indent=2))
        return 0

    print(f"📋 Available Hands ({len(hands)}):\n")
    for h in hands:
        status = "🟢 enabled" if h['enabled'] else "🔘 disabled"
        print(f"  {h['name']} — {status}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
