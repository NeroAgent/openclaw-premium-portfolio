#!/usr/bin/env python3
"""
openfang stop — Stop the OpenFang daemon.
"""

import argparse
import os
import subprocess
import sys
import signal

def find_openfang_bin():
    bin_path = os.environ.get("OPENFANG_BIN", "openfang")
    for path in [f"{os.environ.get('HOME')}/.cargo/bin/openfang", "/usr/local/bin/openfang"]:
        if os.path.isfile(path):
            return path
    return None

def main():
    parser = argparse.ArgumentParser(description="Stop OpenFang daemon")
    args = parser.parse_args()

    openfang = find_openfang_bin()
    if not openfang:
        print("[ERROR] openfang binary not found", file=sys.stderr)
        return 1

    try:
        # Try graceful stop via signal
        # Find PID from pidfile if exists
        pidfile = Path.home() / ".openfang" / "openfang.pid"
        if pidfile.exists():
            pid = int(pidfile.read_text().strip())
            try:
                os.kill(pid, signal.SIGTERM)
                print(f"[OK] Stopped (PID {pid})")
                pidfile.unlink()
                return 0
            except ProcessLookupError:
                pidfile.unlink()
        # Fallback: pkill
        subprocess.run(["pkill", "-f", "openfang"], timeout=5)
        print("[OK] Stopped (pkill)")
        return 0
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
