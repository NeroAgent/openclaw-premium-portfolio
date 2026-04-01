#!/usr/bin/env python3
"""
off-grid-mobile push-model — Copy a GGUF model to the device.
"""

import argparse
import os
import subprocess
import sys

def main():
    parser = argparse.ArgumentParser(description="Push a GGUF model to device")
    parser.add_argument("local_model_path", help="Path to .gguf file")
    parser.add_argument("--device-dir", default="/sdcard/offgrid/models/", help="Destination directory on device")
    parser.add_argument("--adb-path", default=os.environ.get("OFFGRID_ADB_PATH", "adb"))
    args = parser.parse_args()

    if not os.path.isfile(args.local_model_path):
        print(f"[ERROR] Local file not found: {args.local_model_path}", file=sys.stderr)
        return 1

    # Ensure destination exists
    subprocess.run([args.adb_path, "shell", "mkdir", "-p", args.device_dir], capture_output=True)

    # Push
    try:
        print(f"[INFO] Pushing {args.local_model_path} to {args.device_dir}...")
        result = subprocess.run([args.adb_path, "push", args.local_model_path, args.device_dir], timeout=300)
        if result.returncode != 0:
            print("[ERROR] Push failed", file=sys.stderr)
            return 1
        print(f"[OK] Model pushed. Off Grid will detect it on next launch.")
        return 0
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
