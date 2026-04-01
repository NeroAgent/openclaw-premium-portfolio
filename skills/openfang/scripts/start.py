#!/usr/bin/env python3
"""
openfang start — Start the OpenFang daemon.
"""

import argparse
import os
import subprocess
import sys
import time
import socket

def find_openfang_bin():
    bin_path = os.environ.get("OPENFANG_BIN", "openfang")
    for path in [f"{os.environ.get('HOME')}/.cargo/bin/openfang", "/usr/local/bin/openfang"]:
        if os.path.isfile(path):
            return path
    return None

def is_running(port=4200):
    """Check if dashboard port is open (and likely running)."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0

def main():
    parser = argparse.ArgumentParser(description="Start OpenFang daemon")
    parser.add_argument("--background", action="store_true", help="Run in background")
    parser.add_argument("--port", type=int, default=4200, help="Dashboard port")
    args = parser.parse_args()

    openfang = find_openfang_bin()
    if not openfang:
        print("[ERROR] openfang binary not found", file=sys.stderr)
        return 1

    if is_running(args.port):
        print("✅ Already running")
        return 0

    cmd = [openfang, "start"]
    # Could set OPENFANG_PORT if needed
    env = os.environ.copy()

    try:
        if args.background:
            subprocess.Popen(cmd, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(2)
            if is_running(args.port):
                print(f"[OK] OpenFang started in background on port {args.port}")
                return 0
            else:
                print("[ERROR] Failed to start", file=sys.stderr)
                return 1
        else:
            subprocess.run(cmd, env=env)
            return 0
    except KeyboardInterrupt:
        print("\n[INFO] Stopped")
        return 0
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
