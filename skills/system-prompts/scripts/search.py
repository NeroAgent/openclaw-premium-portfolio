#!/usr/bin/env python3
"""
system-prompts search — Full-text search across prompts.
"""

import argparse
import json
import sys
from pathlib import Path
import re

PROMPTS_DIR = Path("/root/.openclaw/workspace/external/system-prompts-and-models-of-ai-tools/prompts")

def main():
    parser = argparse.ArgumentParser(description="Search prompts")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--output", choices=["text", "json"], default="text")
    args = parser.parse_args()

    if not PROMPTS_DIR.exists():
        print(f"[ERROR] Prompts directory not found: {PROMPTS_DIR}", file=sys.stderr)
        sys.exit(1)

    results = []
    for md in PROMPTS_DIR.glob("*.md"):
        with open(md) as f:
            content = f.read()
        # Simple search in title and body
        name = md.stem
        if args.query.lower() in name.lower() or args.query.lower() in content.lower():
            # Extract first line as description
            lines = content.strip().split("\n")
            # Skip frontmatter
            start = 0
            if lines and lines[0].strip() == "---":
                try:
                    end = lines[1:].index("---") + 1
                    lines = lines[end+1:]
                except:
                    lines = []
            description = lines[0].strip("# ").strip()[:100] if lines else ""
            results.append({"name": name, "description": description, "file": str(md)})

    if args.output == "json":
        print(json.dumps({"results": results}, indent=2))
    else:
        print(f"🔍 Search results for '{args.query}': {len(results)} found\n")
        for r in results:
            print(f"  {r['name']}: {r['description']}")
        print()

if __name__ == "__main__":
    main()
