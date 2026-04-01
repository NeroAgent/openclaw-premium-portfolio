#!/usr/bin/env python3
"""
file-reader skill wrapper — implements the read_file tool
"""

import json
import sys
from pathlib import Path

def main():
    # Expect arguments: tool-call <tool_name> <json_input>
    if len(sys.argv) < 4 or sys.argv[1] != "tool-call":
        print("Usage: run.py tool-call <tool_name> <json_input>")
        sys.exit(1)

    tool_name = sys.argv[2]
    input_json = sys.argv[3]

    if tool_name != "read_file":
        print(f"Unknown tool: {tool_name}")
        sys.exit(1)

    try:
        args = json.loads(input_json)
        path = args["path"]
        offset = args.get("offset", 0)
        limit = args.get("limit", 1000)

        file_path = Path(path)
        if not file_path.exists():
            print(json.dumps({"error": f"File not found: {path}"}))
            sys.exit(1)

        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        total = len(lines)
        start = max(0, offset)
        end = min(total, start + limit)
        content = ''.join(lines[start:end])

        result = {
            "path": str(file_path),
            "offset": start,
            "limit": limit,
            "total_lines": total,
            "content": content
        }
        print(json.dumps(result))
        sys.exit(0)

    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON input"}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

if __name__ == "__main__":
    main()
