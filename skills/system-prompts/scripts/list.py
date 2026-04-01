#!/usr/bin/env python3
"""
system-prompts list — List available system prompts.
"""

import argparse
import json
import os
import sys
from pathlib import Path

PROMPTS_DIR = Path("/root/.openclaw/workspace/external/system-prompts-and-models-of-ai-tools/prompts")

def list_prompts(category=None, tag=None, output="text"):
    if not PROMPTS_DIR.exists():
        print(f"[ERROR] Prompts directory not found: {PROMPTS_DIR}", file=sys.stderr)
        return []

    prompts = []
    for md in PROMPTS_DIR.glob("*.md"):
        # Parse frontmatter
        with open(md) as f:
            content = f.read()
        if not content.startswith("---"):
            continue
        parts = content.split("---", 2)
        if len(parts) < 3:
            continue
        frontmatter = parts[1]
        body = parts[2].strip()
        # Parse simple YAML key: value
        meta = {}
        for line in frontmatter.strip().split("\n"):
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip().strip('"').strip("'")
        name = md.stem
        # Filters
        if category and meta.get("category") != category:
            continue
        if tag and tag not in meta.get("tags", ""):
            continue
        meta["name"] = name
        meta["description"] = body.split("\n")[0].strip("# ")[:100] + ("..." if len(body) > 100 else "")
        prompts.append(meta)

    prompts.sort(key=lambda x: x.get("name"))

    if output == "json":
        print(json.dumps({"prompts": prompts}, indent=2))
    else:
        print(f"📚 Available system prompts ({len(prompts)}):\n")
        for p in prompts:
            print(f"  {p['name']} — {p['category']}")
            print(f"    {p['description']}")
            print()
    return prompts

def main():
    parser = argparse.ArgumentParser(description="List system prompts")
    parser.add_argument("--category", help="Filter by category")
    parser.add_argument("--tag", help="Filter by tag")
    parser.add_argument("--output", choices=["text", "json"], default="text")
    args = parser.parse_args()
    list_prompts(args.category, args.tag, args.output)

if __name__ == "__main__":
    main()
