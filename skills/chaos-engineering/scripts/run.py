#!/usr/bin/env python3
# chaos-engineering skill — ToolRegistry interface

import json
import sys
import subprocess
from pathlib import Path

WORKSPACE = Path.cwd()
CHAOS_SCRIPT = WORKSPACE / "skills" / "chaos-engineering" / "scripts" / "chaos.py"
THERMAL_SCRIPT = WORKSPACE / "skills" / "chaos-engineering" / "thermal_dashboard" / "render.sh"

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "missing action"}))
        sys.exit(1)
    
    action = sys.argv[1]
    input_data = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
    
    if action == "chaos_induce":
        chaos_type = input_data.get("type", "random")
        cmd = ["python3", str(CHAOS_SCRIPT), "induce", chaos_type]
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
    
    elif action == "chaos_heal":
        cmd = ["python3", str(CHAOS_SCRIPT), "heal"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
    
    elif action == "chaos_status":
        cmd = ["python3", str(CHAOS_SCRIPT), "status"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
    
    elif action == "thermal_dashboard":
        # The shell script doesn't return JSON, just output
        format_type = input_data.get("format", "ansi")
        subprocess.run([str(THERMAL_SCRIPT)])
    
    else:
        print(json.dumps({"error": f"unknown action: {action}"}))
        sys.exit(1)

if __name__ == "__main__":
    main()