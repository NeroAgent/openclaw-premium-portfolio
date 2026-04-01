#!/usr/bin/env python3
"""
lean-ctx mcp-server — Start the MCP server in background.
"""

import argparse
import os
import subprocess
import sys
import time
import signal

def find_lean_ctx_bin():
    bin_path = os.environ.get("LEAN_CTX_BIN")
    if bin_path and os.path.isfile(bin_path):
        return bin_path
    for path in os.environ.get("PATH", "").split(":"):
        candidate = os.path.join(path, "lean-ctx")
        if os.path.isfile(candidate):
            return candidate
    return None

def main():
    parser = argparse.ArgumentParser(description="Start lean-ctx MCP server")
    parser.add_argument("--port", type=int, default=3333,
                        help="Port for MCP server (default: 3333)")
    parser.add_argument("--daemon", action="store_true",
                        help="Run as daemon (detached)")
    args = parser.parse_args()

    lean_ctx = find_lean_ctx_bin()
    if not lean_ctx:
        print("[ERROR] lean-ctx binary not found.", file=sys.stderr)
        sys.exit(1)

    cmd = [lean_ctx, "mcp-server"]
    if args.port != 3333:
        cmd.extend(["--port", str(args.port)])

    if args.daemon:
        try:
            proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                    start_new_session=True)  # detach
            print(f"[INFO] MCP server started (PID {proc.pid}) on port {args.port}")
            # Write pidfile? Could be ~/.lean-ctx/mcp-server.pid
            sys.exit(0)
        except Exception as e:
            print(f"[ERROR] Failed to start daemon: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Run in foreground, propagate signals
        try:
            result = subprocess.run(cmd)
            sys.exit(result.returncode)
        except KeyboardInterrupt:
            print("\n[INFO] MCP server stopped")
            sys.exit(0)

if __name__ == "__main__":
    main()
