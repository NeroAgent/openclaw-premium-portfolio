#!/usr/bin/env python3
"""
Git Status Summary — main entry point

Scans directories for git repos and produces a concise overview.
"""

import argparse
import json
import os
import sys
from pathlib import Path

# Add scripts directory to path for imports
SCRIPT_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(SCRIPT_DIR))

from scanner import find_git_repos
from reporter import TextReporter, JSONReporter
from git_wrapper import GitRepo

def main():
    parser = argparse.ArgumentParser(description="Quick overview of git repositories")
    parser.add_argument("paths", nargs="*", default=["."],
                        help="Directories to scan (default: current)")
    parser.add_argument("--max-repos", type=int, default=50,
                        help="Maximum repos to display")
    parser.add_argument("--verbose", action="store_true",
                        help="Show full commit messages and file lists")
    parser.add_argument("--output", choices=["text", "json"], default="text",
                        help="Output format")
    parser.add_argument("--filter", default="",
                        help="Comma-separated filters: dirty,behind,ahead,pr-open,clean")
    parser.add_argument("--github-token", default=None,
                        help="GitHub token for PR/issue API")
    args = parser.parse_args()

    # Discover repositories
    repos = []
    for path in args.paths:
        repos.extend(find_git_repos(path))

    # Limit count
    repos = repos[:args.max_repos]

    # Gather data for each repo
    repo_data = []
    filters = set(args.filter.split(",")) if args.filter else set()

    for repo_path in repos:
        try:
            repo = GitRepo(repo_path, github_token=args.github_token)
            data = repo.collect_status(verbose=args.verbose)
            data["path"] = str(repo_path)

            # Apply filters
            if filters:
                matched = False
                if "dirty" in filters and data.get("dirty", False):
                    matched = True
                if "behind" in filters and data.get("behind_count", 0) > 0:
                    matched = True
                if "ahead" in filters and data.get("ahead_count", 0) > 0:
                    matched = True
                if "pr-open" in filters and data.get("open_prs", 0) > 0:
                    matched = True
                if "clean" in filters and not data.get("dirty", False):
                    matched = True
                if not matched:
                    continue

            repo_data.append(data)
        except Exception as e:
            # Record error but continue
            repo_data.append({
                "path": str(repo_path),
                "error": str(e)
            })

    # Output
    if args.output == "json":
        reporter = JSONReporter()
        print(reporter.format(repo_data))
    else:
        reporter = TextReporter(verbose=args.verbose)
        print(reporter.format(repo_data))

    return 0

if __name__ == "__main__":
    sys.exit(main())
