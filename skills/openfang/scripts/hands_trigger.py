#!/usr/bin/env python3
"""
openfang hands trigger — Manually trigger a Hand to run immediately.
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
    parser = argparse.ArgumentParser(description="Trigger a Hand to run now")
    parser.add_argument("hand_name", help="Name of the Hand")
    parser.add_argument("--output", choices=["text", "json"], default="text")
    args = parser.parse_args()

    openfang = find_openfang_bin()
    if not openfang:
        print("[ERROR] openfang binary not found", file=sys.stderr)
        return 1

    try:
        result = subprocess.run([openfang, "hands", "trigger", args.hand_name], capture_output=True, text=True, timeout=600)
        if args.output == "json":
            # Try to parse JSON from the Hand's execution summary
            try:
                # openfang might output JSON with flag; assume plain text for now
                print(json.dumps({"hand": args.hand_name, "output": result.stdout, "error": result.stderr}))
            except:
                print(result.stdout)
        else:
            print(result.stdout)
            if result.stderr:
                print(result.stderr, file=sys.stderr)
        return result.returncode
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
