#!/usr/bin/env python3
"""
claw (Claude Code rewrite) skill wrapper — Rust terminal AI agent
"""

import subprocess
import json
import os
import sys
from pathlib import Path

CLAW_BIN = Path("/root/.openclaw/workspace/external/claude-code/rust/target/release/claw")

def run_claw(args, input_text=None):
    """Execute claw with given arguments"""
    if not CLAW_BIN.exists():
        return {"success": False, "error": "binary not found", "stdout": "", "stderr": "claw binary not built. Run: cargo build --release -p claw-cli"}
    cmd = [str(CLAW_BIN)] + args
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
        print("Usage: claw [interactive|ask|run_tool|list_tools|auth|models] [args...]")
        sys.exit(1)

    action = sys.argv[1]
    args = sys.argv[2:]

    if action == "ask":
        prompt = args[0] if args else sys.stdin.read()
        result = run_claw(["ask", "--prompt", prompt] + args[1:], input_text=prompt)
        output = result.get("stdout", "") + result.get("stderr", "")
        print(json.dumps(result) if "--json" in args else output)

    elif action == "run_tool":
        # Invoke a specific tool directly and return JSON result
        if len(args) < 1:
            print("Usage: claw run_tool <tool_name> <json_input>")
            sys.exit(1)
        tool_name = args[0]
        tool_input = json.loads(args[1]) if len(args) > 1 else {}
        allowed = ["read_file", "write_file", "edit_file", "glob_search", "grep_search", "bash"]
        if tool_name not in allowed:
            print(f"Error: tool '{tool_name}' not in allowed list: {', '.join(allowed)}")
            sys.exit(1)
        # Build a prompt that forces immediate tool use
        prompt = f"Use the {tool_name} tool with this input: {json.dumps(tool_input)}. Return only the tool result."
        result = run_claw([
            "ask",
            "--prompt", prompt,
            "--output-format", "json",
            "--allowedTools", tool_name,
            "--permission-mode", "read-only" if tool_name != "bash" else "danger-full-access",
            "--dangerously-skip-permissions" if tool_name == "bash" else ""
        ], input_text=prompt)
        # Try to extract tool result from JSON output
        try:
            parsed = json.loads(result.get("stdout", "{}"))
            if "toolCalls" in parsed:
                print(json.dumps(parsed))
            else:
                print(result.get("stdout", ""))
        except json.JSONDecodeError:
            print(result.get("stdout", "") + result.get("stderr", ""))

    elif action == "list_tools":
        # Return a JSON list of available tools with their schemas
        tools = [
            {"name": "read_file", "description": "Read a text file from the workspace.", "input_schema": {"type": "object", "properties": {"path": {"type": "string"}, "offset": {"type": "integer"}, "limit": {"type": "integer"}}, "required": ["path"]}},
            {"name": "write_file", "description": "Write a text file in the workspace.", "input_schema": {"type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string"}}, "required": ["path", "content"]}},
            {"name": "edit_file", "description": "Replace text in a workspace file.", "input_schema": {"type": "object", "properties": {"path": {"type": "string"}, "old_string": {"type": "string"}, "new_string": {"type": "string"}, "replace_all": {"type": "boolean"}}, "required": ["path", "old_string", "new_string"]}},
            {"name": "glob_search", "description": "Find files by glob pattern.", "input_schema": {"type": "object", "properties": {"pattern": {"type": "string"}, "path": {"type": "string"}}, "required": ["pattern"]}},
            {"name": "grep_search", "description": "Search file contents with a regex pattern.", "input_schema": {"type": "object", "properties": {"pattern": {"type": "string"}, "path": {"type": "string"}}, "required": ["pattern"]}},
            {"name": "bash", "description": "Execute a shell command in the current workspace.", "input_schema": {"type": "object", "properties": {"command": {"type": "string"}, "timeout": {"type": "integer"}, "description": {"type": "string"}, "run_in_background": {"type": "boolean"}, "dangerouslyDisableSandbox": {"type": "boolean"}}, "required": ["command"]}},
        ]
        print(json.dumps(tools, indent=2))

    elif action == "interactive":
        os.execvp(str(CLAW_BIN), ["claw"] + args)

    elif action == "auth":
        result = run_claw(["auth"] + args)
        print(result.get("stdout", "") + result.get("stderr", ""))

    elif action == "models":
        result = run_claw(["models"] + args)
        print(result.get("stdout", ""))

    else:
        print(f"Unknown action: {action}")
        sys.exit(1)

if __name__ == "__main__":
    main()
