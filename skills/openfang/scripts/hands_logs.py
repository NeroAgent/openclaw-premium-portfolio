#!/usr/bin/env python3
"""
openfang hands logs — View logs for a specific Hand.
"""

import argparse
import subprocess
import sys

def find_openfang_bin():
    bin_path = os.environ.get("OPENFANG_BIN", "openfang")
    for path in [f"{os.environ.get('HOME')}/.cargo/bin/openfang", "/usr/local/bin/openfang"]:
        if os.path.isfile(path):
            return path
    return None

def main():
    parser = argparse.ArgumentParser(description="View logs for a Hand")
    parser.add_argument("hand_name", help="Name of the Hand")
    parser.add_argument("--lines", type=int, default=50, help="Number of lines to show")
    parser.add_argument("--follow", action="store_true", help="Follow log output")
    args = parser.parse_args()

    openfang = find_openfang_bin()
    if not openfang:
        print("[ERROR] openfang binary not found", file=sys.stderr)
        return 1

    cmd = [openfang, "hands", "logs", args.hand_name, "--lines", str(args.lines)]
    if args.follow:
        cmd.append("--follow")

    try:
        subprocess.run(cmd)
        return 0
    except KeyboardInterrupt:
        return 0
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
