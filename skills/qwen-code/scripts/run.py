#!/usr/bin/env python3
"""
qwen-code skill wrapper - AI coding agent for terminal
"""

import subprocess
import json
import os
import sys
from pathlib import Path

def run_qwen(args, input_text=None):
    """Execute qwen with given arguments"""
    cmd = ["qwen"] + args
    try:
        result = subprocess.run(
            cmd,
            input=input_text,
            capture_output=True,
            text=True,
            timeout=300
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "code": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "timeout", "stdout": "", "stderr": "Process timed out"}
    except Exception as e:
        return {"success": False, "error": str(e), "stdout": "", "stderr": ""}

def main():
    if len(sys.argv) < 2:
        print("Usage: qwen-code [ask|interactive|auth|list-models] [args...]")
        sys.exit(1)

    action = sys.argv[1]
    args = sys.argv[2:]

    if action == "ask":
        # Pass a single prompt to qwen in non-interactive mode
        # qwen typically runs interactive; for non-interactive we might use heredoc or specific flags
        # For now, we'll pass the prompt via stdin if provided
        prompt = args[0] if args else sys.stdin.read()
        result = run_qwen(["--non-interactive", "--prompt", prompt] if args else ["--non-interactive"], input_text=prompt)
        print(json.dumps(result) if "--json" in args else result.get("stdout", "") + result.get("stderr", ""))
    elif action == "interactive":
        # Launch interactive qwen session (handed off to user)
        os.execvp("qwen", ["qwen"] + args)
    elif action == "auth":
        # Run authentication flow
        result = run_qwen(["auth"] + args)
        print(result.get("stdout", "") + result.get("stderr", ""))
    elif action == "list-models":
        # List available models (via settings)
        settings_path = Path.home() / ".qwen" / "settings.json"
        if settings_path.exists():
            try:
                with open(settings_path) as f:
                    settings = json.load(f)
                providers = settings.get("modelProviders", {})
                print(json.dumps(providers, indent=2))
            except Exception as e:
                print(f"Error reading settings: {e}")
        else:
            print("Settings not found. Run qwen/auth first.")
    else:
        print(f"Unknown action: {action}")
        sys.exit(1)

if __name__ == "__main__":
    main()
