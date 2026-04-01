#!/usr/bin/env python3
"""
opensandbox python — Run Python code in a sandbox.
"""

import argparse
import os
import sys

def main():
    parser = argparse.ArgumentParser(description="Execute Python code in a sandbox")
    parser.add_argument("code", help="Python code string")
    parser.add_argument("--image", default=os.environ.get("OPENSANDBOX_DEFAULT_IMAGE", "python:3.11"))
    args = parser.parse_args()

    # Reuse run.py logic by importing it? Too complex for now. Just call run.
    # For simplicity, we'll construct a command.
    cmd = f"python -c {repr(args.code)}"
    # We'll exec ourselves with 'run' subcommand? Actually we could just call run.py directly.
    # Simpler: print instruction; real impl would call run.
    print(f"Would execute: {cmd} in image {args.image}")
    print("Not fully implemented yet; use 'opensandbox run' directly.")
    return 0

if __name__ == "__main__":
    main()
