#!/usr/bin/env python3
"""
picoclaw config — Show effective configuration.
"""

import argparse
import os
import json

def main():
    parser = argparse.ArgumentParser(description="Show picoclaw configuration")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    config = {
        "model": os.environ.get("PICOCLAW_MODEL", "not set (will use default)"),
        "openai_api_key_set": "yes" if os.environ.get("OPENAI_API_KEY") else "no",
        "anthropic_api_key_set": "yes" if os.environ.get("ANTHROPIC_API_KEY") else "no",
        "max_steps": int(os.environ.get("PICOCLAW_MAX_STEPS", "5")),
        "confirm_destructive": os.environ.get("PICOCLAW_CONFIRM_DESTRUCTIVE", "true").lower() == "true",
        "workdir": os.environ.get("PICOCLA_WORKDIR", os.getcwd())
    }

    if args.json:
        print(json.dumps(config, indent=2))
    else:
        print("=== Picoclaw Configuration ===")
        for k, v in config.items():
            print(f"{k}: {v}")

if __name__ == "__main__":
    main()
