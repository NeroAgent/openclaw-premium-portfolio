#!/usr/bin/env python3
"""
off-grid-mobile start — Launch the Off Grid app on device via ADB.
"""

import argparse
import os
import subprocess
import sys

def main():
    parser = argparse.ArgumentParser(description="Start Off Grid Mobile app on device")
    parser.add_argument("--adb-path", default=os.environ.get("OFFGRID_ADB_PATH", "adb"))
    args = parser.parse_args()

    # Launch activity
    try:
        subprocess.run([args.adb_path, "shell", "am", "start", "-n", "ai.offgridmobile/.MainActivity"], check=True, timeout=10)
        print("✅ Off Grid Mobile started")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to start app: {e}", file=sys.stderr)
        print("   Is the app installed? Check with: adb shell pm list packages | grep offgrid", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
