#!/usr/bin/env python3
"""
opensandbox server-status — Check if server is running.
"""

import argparse
import subprocess
import sys
import requests

def main():
    parser = argparse.ArgumentParser(description="Check server status")
    args = parser.parse_args()

    url = os.environ.get("OPENSANDBOX_SERVER_URL", "http://localhost:8080")
    try:
        resp = requests.get(f"{url}/health", timeout=2)
        if resp.status_code == 200:
            print(f"RUNNING ({url})")
            return 0
        else:
            print(f"UNHEALTHY (HTTP {resp.status_code})")
            return 1
    except requests.ConnectionError:
        print("STOPPED")
        return 0

if __name__ == "__main__":
    import os
    sys.exit(main())
