#!/usr/bin/env python3
"""
openfang hands config — Show or edit Hand configuration.
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
    parser = argparse.ArgumentParser(description="View or edit a Hand's config")
    parser.add_argument("hand_name", help="Name of the Hand")
    parser.add_argument("--edit", action="store_true", help="Open in editor")
    args = parser.parse_args()

    openfang = find_openfang_bin()
    if not openfang:
        print("[ERROR] openfang binary not found", file=sys.stderr)
        return 1

    cmd = [openfang, "hands", "config", args.hand_name]
    if args.edit:
        cmd.append("--edit")

    try:
        subprocess.run(cmd)
        return 0
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
