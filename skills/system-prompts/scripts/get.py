#!/usr/bin/env python3
"""
system-prompts get — Retrieve a specific prompt.
"""

import argparse
from pathlib import Path

PROMPTS_DIR = Path("/root/.openclaw/workspace/external/system-prompts-and-models-of-ai-tools/prompts")

def main():
    parser = argparse.ArgumentParser(description="Get a system prompt")
    parser.add_argument("name", help="Prompt name (filename without .md)")
    parser.add_argument("--format", choices=["raw", "json"], default="json")
    args = parser.parse_args()

    md_path = PROMPTS_DIR / f"{args.name}.md"
    if not md_path.exists():
        print(f"[ERROR] Prompt not found: {args.name}", file=sys.stderr)
        sys.exit(1)

    with open(md_path) as f:
        content = f.read()

    # Split frontmatter and body
    if content.startswith("---"):
        parts = content.split("---", 2)
        frontmatter = parts[1]
        body = parts[2].strip()
    else:
        frontmatter = ""
        body = content

    if args.format == "raw":
        print(body)
    else:
        # Output json with metadata and body
        import json
        meta = {}
        for line in frontmatter.strip().split("\n"):
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip().strip('"').strip("'")
        out = {"name": args.name, "metadata": meta, "prompt": body}
        print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
