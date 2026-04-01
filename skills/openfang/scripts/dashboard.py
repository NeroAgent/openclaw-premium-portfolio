#!/usr/bin/env python3
"""
openfang dashboard — Open the web dashboard.
"""

import argparse
import subprocess
import sys
import webbrowser

def main():
    parser = argparse.ArgumentParser(description="Open OpenFang dashboard")
    parser.add_argument("--port", type=int, default=4200)
    args = parser.parse_args()

    url = f"http://localhost:{args.port}"
    try:
        webbrowser.open(url)
        print(f"🌐 Opening {url}")
        return 0
    except Exception as e:
        print(f"[ERROR] Could not open browser: {e}", file=sys.stderr)
        print(f"   Manually navigate to {url}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
