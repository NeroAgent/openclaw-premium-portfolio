#!/usr/bin/env python3
"""
llmfit-scan — Just run hardware detection and print specs.
"""

import argparse
import json
import os
import subprocess
import sys

def find_llmfit_bin():
    bin_path = os.environ.get("LLMFIT_BIN", "llmfit")
    try:
        subprocess.run([bin_path, "--version"], capture_output=True, timeout=2)
        return bin_path
    except:
        for path in [f"{os.environ.get('HOME')}/.cargo/bin/llmfit", "/usr/local/bin/llmfit"]:
            if os.path.isfile(path):
                return path
        return None

def main():
    parser = argparse.ArgumentParser(description="Show hardware scan results")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    llmfit = find_llmfit_bin()
    if not llmfit:
        print("[ERROR] llmfit binary not found", file=sys.stderr)
        return 1

    # llmfit has a subcommand? Actually, it's just `llmfit`. But we can extract hardware from --output json and filter.
    # For simplicity, just run llmfit --format json and extract hardware section if available.
    cmd = [llmfit, "--format", "json"]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if result.returncode != 0:
        print(f"[ERROR] {result.stderr}", file=sys.stderr)
        return 1

    try:
        data = json.loads(result.stdout)
        hw = data.get("hardware", {})
    except:
        print("[ERROR] Could not parse llmfit output", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(hw, indent=2))
    else:
        print("=== Hardware Detection ===")
        print(f"CPU: {hw.get('cpu_name', 'Unknown')} ({hw.get('cpu_cores', '?')} cores)")
        print(f"RAM: {hw.get('ram_gb', '?'):.1f} GB")
        if hw.get('gpu_name'):
            print(f"GPU: {hw.get('gpu_name')} ({hw.get('gpu_mem_gb', '?'):.1f} GB VRAM)")
        else:
            print("GPU: None (CPU-only)")
        print(f"Architecture: {hw.get('arch', '?')}")
        print(f"OS: {hw.get('os', '?')}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
