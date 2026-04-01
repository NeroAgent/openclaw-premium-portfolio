#!/usr/bin/env python3
"""
opensandbox stop-server — Stop OpenSandbox server.
"""

import argparse
import subprocess
import sys
import os
import signal

def main():
    parser = argparse.ArgumentParser(description="Stop OpenSandbox server")
    args = parser.parse_args()

    # Try to find PID via pidfile or pgrep
    pidfile = os.path.expanduser("~/.opensandbox/server.pid")
    if os.path.exists(pidfile):
        with open(pidfile) as f:
            pid = int(f.read().strip())
        try:
            os.kill(pid, signal.SIGTERM)
            print(f"[OK] Stopped server (PID {pid})")
            os.remove(pidfile)
            return 0
        except ProcessLookupError:
            os.remove(pidfile)
            print("[WARN] Stale PID file removed")
            return 0
        except Exception as e:
            print(f"[ERROR] {e}", file=sys.stderr)
            return 1
    else:
        # Try pkill
        try:
            subprocess.run(["pkill", "-f", "opensandbox-server"], check=True)
            print("[OK] Killed opensandbox-server processes")
            return 0
        except subprocess.CalledProcessError:
            print("[INFO] No opensandbox-server process found")
            return 0

if __name__ == "__main__":
    sys.exit(main())
