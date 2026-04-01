#!/usr/bin/env python3
"""
openfang status — Check if OpenFang is running.
"""

import argparse
import socket

def main():
    parser = argparse.ArgumentParser(description="Check OpenFang status")
    parser.add_argument("--port", type=int, default=4200)
    args = parser.parse_args()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        if s.connect_ex(("127.0.0.1", args.port)) == 0:
            print(f"✅ OpenFang is running (http://127.0.0.1:{args.port})")
            return 0
        else:
            print("⏸️  OpenFang is not running")
            return 1

if __name__ == "__main__":
    sys.exit(main())
