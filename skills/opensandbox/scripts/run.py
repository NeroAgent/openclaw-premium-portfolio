#!/usr/bin/env python3
"""
opensandbox run — Execute a command in a sandbox.
"""

import argparse
import os
import subprocess
import json
import sys

def main():
    parser = argparse.ArgumentParser(description="Run a command in a sandbox")
    parser.add_argument("command", help="Command to run (quoted)")
    parser.add_argument("--image", default=os.environ.get("OPENSANDBOX_DEFAULT_IMAGE", "python:3.11"),
                        help="Docker image to use")
    parser.add_argument("--mount", action="append", help="Mount host:container")
    parser.add_argument("--env", action="append", help="Environment variable KEY=VALUE")
    parser.add_argument("--timeout", type=int, default=int(os.environ.get("OPENSANDBOX_TIMEOUT", "600")),
                        help="Timeout in seconds")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    server_url = os.environ.get("OPENSANDBOX_SERVER_URL", "http://localhost:8080")

    payload = {
        "image": args.image,
        "command": args.command,
        "mounts": args.mount or [],
        "env": args.env or {},
        "timeout": args.timeout
    }

    try:
        import requests
    except ImportError:
        print("[ERROR] 'requests' library required. Install: pip install requests", file=sys.stderr)
        sys.exit(1)

    try:
        resp = requests.post(f"{server_url}/api/v1/execute", json=payload, timeout=args.timeout + 5)
        if resp.status_code != 200:
            print(f"[ERROR] {resp.status_code}: {resp.text}", file=sys.stderr)
            return 1
        result = resp.json()

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(result.get("stdout", ""))
            if result.get("stderr"):
                print(result.get("stderr"), file=sys.stderr)
            if result.get("exit_code", 0) != 0:
                print(f"[ERROR] Command exited with code {result['exit_code']}", file=sys.stderr)
                return result['exit_code']
        return 0
    except requests.ConnectionError:
        print("[ERROR] Cannot connect to OpenSandbox server. Is it running?", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    import os
    sys.exit(main())
