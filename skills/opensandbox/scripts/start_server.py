#!/usr/bin/env python3
"""
opensandbox start-server — Start OpenSandbox server.
"""

import argparse
import subprocess
import sys
import os

def main():
    parser = argparse.ArgumentParser(description="Start OpenSandbox server")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind")
    parser.add_argument("--port", type=int, default=8080, help="Port")
    parser.add_argument("--daemon", action="store_true", help="Run in background")
    args = parser.parse_args()

    # Find the server executable
    server_cmd = os.environ.get("OPENSANDBOX_SERVER_CMD", "opensandbox-server")
    # Check if it exists
    try:
        subprocess.run([server_cmd, "--help"], capture_output=True, timeout=2)
    except:
        print(f"[ERROR] '{server_cmd}' not found. Install with: opensandbox install-server", file=sys.stderr)
        return 1

    cmd = [server_cmd, "--host", args.host, "--port", str(args.port)]

    if args.daemon:
        print(f"[INFO] Starting server on {args.host}:{args.port} (daemon)")
        subprocess.Popen(cmd)
    else:
        print(f"[INFO] Starting server on {args.host}:{args.port} (foreground). Ctrl+C to stop.")
        try:
            subprocess.run(cmd)
        except KeyboardInterrupt:
            print("\n[INFO] Server stopped")
    return 0

if __name__ == "__main__":
    sys.exit(main())
