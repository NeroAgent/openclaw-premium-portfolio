#!/usr/bin/env python3
"""
openfang init — Initialize config directory.
"""

import argparse
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
    parser = argparse.ArgumentParser(description="Initialize OpenFang config")
    parser.add_argument("--force", action="store_true", help="Overwrite existing config")
    args = parser.parse_args()

    openfang = find_openfang_bin()
    if not openfang:
        print("[ERROR] openfang binary not found. Build with: cargo install openfang", file=sys.stderr)
        return 1

    config_dir = Path.home() / ".openfang"
    if config_dir.exists() and not args.force:
        print(f"[INFO] Config dir already exists: {config_dir}")
        return 0

    try:
        result = subprocess.run([openfang, "init"], timeout=30)
        return result.returncode
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
