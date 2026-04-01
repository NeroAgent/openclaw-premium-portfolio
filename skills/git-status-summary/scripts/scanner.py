#!/usr/bin/env python3
"""
Scanner — finds git repositories in given directories.
"""

import os
from pathlib import Path

def find_git_repos(start_path, max_depth=None):
    """
    Recursively find repositories (directories containing .git).

    Args:
        start_path: path to begin scan
        max_depth: maximum recursion depth (None = unlimited)

    Returns:
        List of Path objects pointing to git repo roots.
    """
    repos = []
    start = Path(start_path).resolve()

    if not start.exists():
        return repos

    # Use BFS to avoid deep recursion issues
    queue = [(start, 0)]
    while queue:
        current, depth = queue.pop(0)

        # Check depth limit
        if max_depth is not None and depth > max_depth:
            continue

        try:
            for item in current.iterdir():
                if item.name == ".git" and item.is_dir():
                    repos.append(current)
                elif item.is_dir() and not item.name.startswith("."):
                    # Avoid recursing into .git and common cache dirs
                    if item.name in ("node_modules", "__pycache__", ".venv", "venv", ".tox"):
                        continue
                    queue.append((item, depth + 1))
        except (PermissionError, OSError):
            # Skip directories we can't read
            continue

    return repos

if __name__ == "__main__":
    import sys
    import json
    repos = find_git_repos(sys.argv[1] if len(sys.argv) > 1 else ".")
    print(json.dumps([str(r) for r in repos], indent=2))
