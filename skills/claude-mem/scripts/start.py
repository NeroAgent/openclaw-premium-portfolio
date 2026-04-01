#!/usr/bin/env python3
"""
claude-mem start — Start the worker service.
"""

import argparse
import os
import subprocess
import sys
import time
import signal
from pathlib import Path

def find_worker_script():
    home = Path.home()
    worker_dir = home / ".claude-mem" / "worker"
    # The worker is likely a Bun script; look for index.ts or dist
    candidate = worker_dir / "src" / "index.ts"
    if candidate.exists():
        return candidate
    # Maybe built?
    candidate = worker_dir / "dist" / "index.js"
    if candidate.exists():
        return candidate
    return None

def main():
    parser = argparse.ArgumentParser(description="Start claude-mem worker")
    parser.add_argument("--background", action="store_true", help="Run as daemon")
    parser.add_argument("--port", type=int, default=37777, help="Port (default: 37777)")
    parser.add_argument("--log", default="~/.claude-mem/logs/worker.log", help="Log file")
    args = parser.parse_args()

    script = find_worker_script()
    if not script:
        print("[ERROR] claude-mem worker not found. Run 'claude-mem install' first.", file=sys.stderr)
        sys.exit(1)

    # Ensure log directory
    log_path = Path(args.log).expanduser()
    log_path.parent.mkdir(parents=True, exist_ok=True)

    # Build command: bun run <script> or node <dist>
    if str(script).endswith(".ts"):
        cmd = ["bun", "run", str(script)]
    else:
        cmd = ["node", str(script)]

    env = os.environ.copy()
    env["PORT"] = str(args.port)

    if args.background:
        print(f"[INFO] Starting worker on port {args.port} (daemon), logging to {log_path}")
        with open(log_path, "a") as logf:
            proc = subprocess.Popen(
                cmd,
                env=env,
                stdout=logf,
                stderr=subprocess.STDOUT,
                start_new_session=True
            )
            # Write pid file
            pidfile = Path.home() / ".claude-mem" / "worker.pid"
            pidfile.write_text(str(proc.pid))
            print(f"[OK] Worker started (PID {proc.pid})")
        return 0
    else:
        print(f"[INFO] Starting worker on port {args.port} (foreground). Ctrl+C to stop.")
        try:
            subprocess.run(cmd, env=env)
        except KeyboardInterrupt:
            print("\n[INFO] Worker stopped")
            return 0

if __name__ == "__main__":
    main()
