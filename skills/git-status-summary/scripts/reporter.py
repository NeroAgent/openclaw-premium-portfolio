#!/usr/bin/env python3
"""
Reporter — formats repository data for output (text or JSON).
"""

import json
from datetime import datetime

class TextReporter:
    def __init__(self, verbose=False):
        self.verbose = verbose

    def format(self, repo_data_list):
        """Format a list of repo data dicts into a human-readable table."""
        lines = []
        total = len(repo_data_list)

        lines.append(f"=== Git Summary ({total} repos scanned) ===\n")

        for data in repo_data_list:
            if "error" in data:
                lines.append(f"❌ {data['path']}")
                lines.append(f"   Error: {data['error']}")
                lines.append("")
                continue

            path = data["path"]
            branch = data.get("branch", "unknown")
            ahead = data.get("ahead_count", 0)
            behind = data.get("behind_count", 0)
            last = data.get("last_commit", {})
            dirty = data.get("dirty", False)
            staged = data.get("staged_count", 0)
            modified = data.get("modified_count", 0)
            untracked = data.get("untracked_count", 0)
            stashes = data.get("stash_count", 0)
            open_prs = data.get("open_prs", 0)

            # Status icon
            if dirty:
                icon = "⚠️"
            elif branch.startswith("DETACHED"):
                icon = "❓"
            else:
                icon = "✅"

            lines.append(f"{icon} {path}")
            lines.append(f"   branch: {branch}{self._format_ahead_behind(ahead, behind)}")

            if last:
                time_ago = last.get("date", "?")
                msg = last.get("message", "")
                hash_ = last.get("hash", "")
                lines.append(f"   last: {hash_} ({time_ago}) \"{self._truncate(msg, 50)}\"")

            if dirty:
                parts = []
                if staged > 0:
                    parts.append(f"{staged} staged")
                if modified > 0:
                    parts.append(f"{modified} modified")
                if untracked > 0:
                    parts.append(f"{untracked} untracked")
                lines.append(f"   status: {', '.join(parts)}")

            if stashes > 0:
                lines.append(f"   stashes: {stashes}")

            if open_prs > 0:
                lines.append(f"   PR: {open_prs} open" + (f" (#{data['pr_list'][0]['number']})" if data.get("pr_list") else ""))

            if self.verbose and dirty:
                if modified:
                    lines.append("   Modified files:")
                    for f in modified[:5]:
                        lines.append(f"     - {f}")
                    if len(modified) > 5:
                        lines.append(f"     ...and {len(modified)-5} more")
                if untracked:
                    lines.append("   Untracked files:")
                    for f in untracked[:5]:
                        lines.append(f"     - {f}")
                    if len(untracked) > 5:
                        lines.append(f"     ...and {len(untracked)-5} more")

            lines.append("")

        return "\n".join(lines)

    def _format_ahead_behind(self, ahead, behind):
        if ahead > 0 and behind > 0:
            return f" ↑{ahead} ↓{behind}"
        elif ahead > 0:
            return f" ↑{ahead}"
        elif behind > 0:
            return f" ↓{behind}"
        return ""

    def _truncate(self, s, max_len):
        if len(s) <= max_len:
            return s
        return s[:max_len-3] + "..."

class JSONReporter:
    def format(self, repo_data_list):
        return json.dumps({
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "repos": repo_data_list
        }, indent=2)

if __name__ == "__main__":
    import sys
    # Test with sample data
    sample = [
        {
            "path": "/home/user/project1",
            "branch": "main",
            "ahead_count": 1,
            "behind_count": 0,
            "last_commit": {"hash": "abc123", "date": "2h ago", "message": "Fix bug"},
            "dirty": False,
            "staged_count": 0,
            "modified_count": 0,
            "untracked_count": 0,
            "stash_count": 0,
            "open_prs": 0
        }
    ]
    print(TextReporter().format(sample))
