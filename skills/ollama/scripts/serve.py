#!/usr/bin/env python3
"""
ollama serve — Start/stop/check the Ollama daemon.
"""

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

def find_ollama_bin():
    bin_path = os.environ.get("OLLAMA_BIN", "ollama")
    try:
        subprocess.run([bin_path, "--version"], capture_output=True, timeout=2)
        return bin_path
    except:
        for path in [f"{os.environ.get('HOME')}/.local/bin/ollama", "/usr/local/bin/ollama"]:
            if os.path.isfile(path):
                return path
        return None

def is_running():
    """Check if ollama is listening on localhost:11434."""
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect(("127.0.0.1", 11434))
        s.close()
        return True
    except:
        return False

def main():
    parser = argparse.ArgumentParser(description="Control Ollama daemon")
    parser.add_argument("action", choices=["start", "stop", "status"], help="Action")
    parser.add_argument("--host", default="127.0.0.1", help="Bind address (start)")
    parser.add_argument("--port", type=int, default=11434, help="Port (start)")
    parser.add_argument("--background", action="store_true", help="Start in background")
    args = parser.parse_args()

    ollama = find_ollama_bin()
    if not ollama:
        print("[ERROR] ollama binary not found", file=sys.stderr)
        return 1

    if args.action == "status":
        if is_running():
            print("✅ Ollama is running (http://127.0.0.1:11434)")
            return 0
        else:
            print("⏸️  Ollama is not running")
            return 1

    elif args.action == "start":
        if is_running():
            print("✅ Already running")
            return 0
        print("[INFO] Starting Ollama daemon...")
        cmd = [ollama, "serve"]
        # Could set env vars like OLLAMA_HOST, OLLAMA_PORT
        env = os.environ.copy()
        env["OLLAMA_HOST"] = f"{args.host}:{args.port}"
        try:
            if args.background:
                subprocess.Popen(cmd, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                time.sleep(1)
                if is_running():
                    print(f"[OK] Ollama started in background on {args.host}:{args.port}")
                    return 0
                else:
                    print("[ERROR] Failed to start", file=sys.stderr)
                    return 1
            else:
                subprocess.run(cmd, env=env)
                return 0
        except Exception as e:
            print(f"[ERROR] {e}", file=sys.stderr)
            return 1

    elif args.action == "stop":
        if not is_running():
            print("⏸️  Not running")
            return 0
        print("[INFO] Stopping Ollama...")
        try:
            # On Linux, we could pkill -f ollama, but better to use PID file if available
            subprocess.run(["pkill", "-f", "ollama serve"], timeout=5)
            time.sleep(1)
            if is_running():
                print("[WARN] Still running; may need manual kill")
                return 0
            else:
                print("[OK] Stopped")
                return 0
        except Exception as e:
            print(f"[ERROR] {e}", file=sys.stderr)
            return 1

if __name__ == "__main__":
    sys.exit(main())
