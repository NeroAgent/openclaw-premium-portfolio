#!/usr/bin/env python3
"""
droidclaw check-adb — Verify ADB connection to device.
"""

import argparse
import subprocess
import sys

def main():
    parser = argparse.ArgumentParser(description="Check ADB connection")
    parser.add_argument("--adb-path", default="adb")
    args = parser.parse_args()

    try:
        # Check adb version
        subprocess.run([args.adb_path, "version"], check=True, capture_output=True)
    except:
        print("[ERROR] adb not found", file=sys.stderr)
        return 1

    # Check devices
    try:
        result = subprocess.run([args.adb_path, "devices"], capture_output=True, text=True, timeout=5)
        lines = result.stdout.strip().split("\n")[1:]  # skip header
        devices = [l.split()[0] for l in lines if l.strip() and "offline" not in l and "unauthorized" not in l]
        if devices:
            print(f"✅ Connected devices: {', '.join(devices)}")
            return 0
        else:
            print("❌ No authorized devices found. Ensure USB debugging is on and device is authorized.")
            return 1
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
