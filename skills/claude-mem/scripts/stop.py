#!/usr/bin/env python3
"""
claude-mem stop — Stop the worker service.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Stop claude-mem worker")
    args = parser.parse_args()

    pidfile = Path.home() / ".claude-mem" / "worker.pid"
    if not pidfile.exists():
        print("[WARN] No PID file found; worker may not be running.")
        # Try to kill by port? Not reliable.
        return 0

    try:
        pid = int(pidfile.read_text().strip())
    except:
        print("[ERROR] Invalid PID file", file=sys.stderr)
        sys.exit(1)

    try:
        os.kill(pid, signal.SIGTERM)
        print(f"[OK] Worker (PID {pid}) stopped")
        pidfile.unlink()
    except ProcessLookupError:
        print(f"[WARN] Process {pid} not found; cleaning up PID file")
        pidfile.unlink()
    except Exception as e:
        print(f"[ERROR] Failed to stop: {e}", file=sys.stderr)
        sys.exit(1)

    return 0

if __name__ == "__main__":
    main()
