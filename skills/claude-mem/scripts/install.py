#!/usr/bin/env python3
"""
claude-mem install — Install and configure the claude-mem worker.
"""

import argparse
import os
import subprocess
import sys
import json
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Install claude-mem worker")
    parser.add_argument("--force", action="store_true", help="Reinstall even if already installed")
    args = parser.parse_args()

    # Check for Node and Bun
    try:
        subprocess.run(["node", "--version"], check=True, capture_output=True)
    except:
        print("[ERROR] Node.js not found. Install Node.js 18+ first.", file=sys.stderr)
        sys.exit(1)

    try:
        subprocess.run(["bun", "--version"], check=True, capture_output=True)
    except:
        print("[ERROR] Bun not found. Install with: curl -fsSL https://bun.sh/install | bash", file=sys.stderr)
        sys.exit(1)

    # Determine install location
    home = Path.home()
    data_dir = home / ".claude-mem"
    data_dir.mkdir(parents=True, exist_ok=True)

    # Check if already installed
    worker_dir = data_dir / "worker"
    if worker_dir.exists() and not args.force:
        print(f"[INFO] claude-mem appears already installed in {worker_dir}")
        print("   Use --force to reinstall")
        return 0

    # Clone if not present
    if not worker_dir.exists():
        print("[INFO] Cloning claude-mem repository...")
        subprocess.run(["git", "clone", "https://github.com/thedotmack/claude-mem.git", str(worker_dir)], check=True)

    # Install dependencies
    print("[INFO] Installing dependencies with Bun...")
    subprocess.run(["bun", "install"], cwd=worker_dir, check=True)

    # Create config
    config_path = data_dir / "settings.json"
    if not config_path.exists() or args.force:
        print("[INFO] Creating default configuration...")
        config = {
            "worker_port": 37777,
            "data_dir": str(data_dir / "data"),
            "auto_capture": True,
            "capture_prompts": False,
            "max_output_tokens": 2000,
            "ui_enabled": True
        }
        config_path.write_text(json.dumps(config, indent=2))
        print(f"   Config written to {config_path}")

    print("[OK] claude-mem installed.")
    print("Next: run 'claude-mem start' to launch the worker.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
