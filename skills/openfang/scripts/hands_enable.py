#!/usr/bin/env python3
"""
openfang hands enable — Enable a Hand.
"""

import argparse
import os
import subprocess
import sys

def find_openfang_bin():
    bin_path = os.environ.get("OPENFANG_BIN", "openfang")
    for path in [f"{os.environ.get('HOME')}/.cargo/bin/openfang", "/usr/local/bin/openfang"]:
        if os.path.isfile(path):
            return path
    return None

def main():
    parser = argparse.ArgumentParser(description="Enable a Hand")
    parser.add_argument("hand_name", help="Name of the Hand")
    args = parser.parse_args()

    openfang = find_openfang_bin()
    if not openfang:
        print("[ERROR] openfang binary not found", file=sys.stderr)
        return 1

    try:
        result = subprocess.run([openfang, "hands", "enable", args.hand_name], capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            print(f"[ERROR] {result.stderr}", file=sys.stderr)
            return 1
        print(f"✅ Enabled hand: {args.hand_name}")
        return 0
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
