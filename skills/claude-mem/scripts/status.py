#!/usr/bin/env python3
"""
claude-mem status — Check if worker is running.
"""

import argparse
import subprocess
import sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Check claude-mem worker status")
    args = parser.parse_args()

    pidfile = Path.home() / ".claude-mem" / "worker.pid"
    if not pidfile.exists():
        print("STOPPED")
        return 0

    try:
        pid = int(pidfile.read_text().strip())
    except:
        print("UNKNOWN (invalid pid)")
        return 1

    # Check if process exists
    try:
        subprocess.run(["kill", "-0", str(pid)], check=True)
        print(f"RUNNING (PID {pid})")
        # Also check port?
        return 0
    except subprocess.CalledProcessError:
        print("STOPPED (stale pid)")
        pidfile.unlink()
        return 0

if __name__ == "__main__":
    sys.exit(main())
