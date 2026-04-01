#!/usr/bin/env python3
"""
off-grid-mobile status — Check if app is installed and device connected.
"""

import argparse
import subprocess
import sys

def main():
    parser = argparse.ArgumentParser(description="Check Off Grid Mobile status")
    parser.add_argument("--adb-path", default="adb")
    args = parser.parse_args()

    try:
        # Check device
        dev = subprocess.run([args.adb_path, "devices"], capture_output=True, text=True, timeout=5)
        lines = dev.stdout.strip().split("\n")[1:]
        devices = [l.split()[0] for l in lines if l.strip() and "offline" not in l and "unauthorized" not in l]
        if not devices:
            print("❌ No authorized ADB devices connected")
            return 1
        print(f"✅ Device connected: {devices[0]}")

        # Check app installed
        pkg = subprocess.run([args.adb_path, "shell", "pm", "list", "packages", "ai.offgridmobile"], capture_output=True, text=True)
        if "ai.offgridmobile" in pkg.stdout:
            print("✅ Off Grid Mobile is installed")
        else:
            print("❌ App not installed. Install from Google Play or APK.")
            return 1

        # Check if running
        ps = subprocess.run([args.adb_path, "shell", "ps", "-A"], capture_output=True, text=True)
        if "offgridmobile" in ps.stdout:
            print("✅ App is currently running")
        else:
            print("⏸️  App is not running")

        # Check models directory
        ls = subprocess.run([args.adb_path, "shell", "ls", "/sdcard/offgrid/models/"], capture_output=True, text=True)
        if ls.returncode == 0 and ls.stdout.strip():
            models = ls.stdout.strip().split("\n")
            print(f"📦 Models installed: {len(models)}")
            for m in models[:5]:
                print(f"   - {m}")
            if len(models) > 5:
                print(f"   ...and {len(models)-5} more")
        else:
            print("📭 No models installed in /sdcard/offgrid/models/")

        return 0
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
