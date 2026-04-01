#!/usr/bin/env python3
"""
Git wrapper — runs git commands safely and parses output.
"""

import subprocess
import json
import os
from pathlib import Path

class GitRepo:
    def __init__(self, path, github_token=None):
        self.path = Path(path)
        self.github_token = github_token

    def _run_git(self, *args, capture_output=True, text=True, check=False):
        """Run a git command in the repo directory."""
        try:
            result = subprocess.run(
                ["git"] + list(args),
                cwd=self.path,
                capture_output=capture_output,
                text=text,
                timeout=10,
                env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"}  # Faster for read-only
            )
            if check and result.returncode != 0:
                raise RuntimeError(f"Git command failed: git {' '.join(args)}\n{result.stderr}")
            return result
        except subprocess.TimeoutExpired:
            return None
        except Exception as e:
            if check:
                raise
            return None

    def get_current_branch(self):
        """Get current branch name, or detached HEAD info."""
        result = self._run_git("branch", "--show-current")
        if result and result.returncode == 0:
            branch = result.stdout.strip()
            if branch:
                return branch
        # If no branch, we're in detached HEAD
        result = self._run_git("rev-parse", "--short", "HEAD")
        if result and result.returncode == 0:
            return f"DETACHED:{result.stdout.strip()}"
        return "unknown"

    def get_branch_ahead_behind(self):
        """
        Returns (ahead, behind) counts vs upstream.
        If no upstream, returns (0, 0).
        """
        result = self._run_git("rev-list", "--left-right", "--count", "@{upstream}...HEAD")
        if result and result.returncode == 0:
            parts = result.stdout.strip().split("\t")
            if len(parts) == 2:
                behind = int(parts[0]) if parts[0] else 0
                ahead = int(parts[1]) if parts[1] else 0
                return ahead, behind
        return 0, 0

    def get_upstream_remote(self):
        """Get the upstream remote name for current branch."""
        result = self._run_git("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}")
        if result and result.returncode == 0:
            ref = result.stdout.strip()
            if "/" in ref:
                return ref.split("/")[0]
        return None

    def get_last_commit(self):
        """Get dict with short hash, author, relative date, and message."""
        result = self._run_git("log", "-1", "--pretty=format:%h|%an|%cr|%s")
        if result and result.returncode == 0:
            parts = result.stdout.strip().split("|", 3)
            if len(parts) == 4:
                return {
                    "hash": parts[0],
                    "author": parts[1],
                    "date": parts[2],
                    "message": parts[3]
                }
        return None

    def get_status(self):
        """
        Returns a dict with:
        - dirty: bool (any changes)
        - modified: list of modified files
        - untracked: list of untracked files
        - staged: list of staged files
        """
        result = self._run_git("status", "--porcelain")
        modified = []
        untracked = []
        staged = []

        if result and result.returncode == 0:
            for line in result.stdout.strip().split("\n"):
                if not line:
                    continue
                # Porcelain format: XY path
                status = line[:2]
                path = line[3:]
                if status == "??":
                    untracked.append(path)
                elif status[0] in ("A", "M", "D", "R", "C"):
                    staged.append(path)
                elif status[1] in ("M", "D", "R", "C"):
                    modified.append(path)

        return {
            "dirty": bool(modified or untracked or staged),
            "modified": modified,
            "untracked": untracked,
            "staged": staged
        }

    def get_stash_count(self):
        """Count number of stashes."""
        result = self._run_git("stash", "list")
        if result and result.returncode == 0:
            return len([l for l in result.stdout.strip().split("\n") if l])
        return 0

    def get_github_pr_info(self):
        """
        If GitHub remote detected and token available, fetch open PRs.
        Returns dict with pr_count and list of PR numbers/titles.
        """
        remote = self.get_upstream_remote()
        if not remote or not self.github_token:
            return {"pr_count": 0, "prs": []}

        # Get remote URL to extract owner/repo
        result = self._run_git("remote", "get-url", remote)
        if not result or result.returncode != 0:
            return {"pr_count": 0, "prs": []}

        url = result.stdout.strip()
        # Parse github.com/owner/repo(.git)
        import re
        m = re.search(r"github\.com[:/]([^/]+/[^/]+?)(?:\.git)?$", url)
        if not m:
            return {"pr_count": 0, "prs": []}

        repo_full = m.group(1)
        api_url = f"https://api.github.com/repos/{repo_full}/pulls?state=open&per_page=3"

        try:
            import urllib.request
            import urllib.error
            req = urllib.request.Request(
                api_url,
                headers={"Authorization": f"token {self.github_token}" if self.github_token.startswith("ghp") else {}}
            )
            with urllib.request.urlopen(req, timeout=5) as resp:
                if resp.status == 200:
                    prs = json.loads(resp.read().decode())
                    return {
                        "pr_count": len(prs),
                        "prs": [{"number": pr["number"], "title": pr["title"], "user": pr["user"]["login"]} for pr in prs]
                    }
        except:
            pass

        return {"pr_count": 0, "prs": []}

    def collect_status(self, verbose=False):
        """
        Collect all status information for this repo into a dict.
        """
        branch = self.get_current_branch()
        ahead, behind = self.get_branch_ahead_behind()
        last_commit = self.get_last_commit() or {}
        status = self.get_status()
        stash_count = self.get_stash_count()

        data = {
            "branch": branch,
            "ahead_count": ahead,
            "behind_count": behind,
            "last_commit": last_commit,
            "dirty": status["dirty"],
            "staged_count": len(status["staged"]),
            "modified_count": len(status["modified"]),
            "untracked_count": len(status["untracked"]),
            "stash_count": stash_count
        }

        if verbose:
            data["staged_files"] = status["staged"]
            data["modified_files"] = status["modified"]
            data["untracked_files"] = status["untracked"]

        # Try GitHub PR info
        pr_info = self.get_github_pr_info()
        data["open_prs"] = pr_info["pr_count"]
        if pr_info["prs"]:
            data["pr_list"] = pr_info["prs"]

        return data

if __name__ == "__main__":
    # Quick test
    import sys
    repo = GitRepo(sys.argv[1] if len(sys.argv) > 1 else ".")
    print(json.dumps(repo.collect_status(verbose=True), indent=2))
