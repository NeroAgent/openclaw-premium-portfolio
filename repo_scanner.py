#!/usr/bin/env python3
"""
Repo Scanner - Analyze external repos for OpenClaw skill potential
 prioritize lightweight, single-binary tools suitable for Termux
"""

import time
import json
from pathlib import Path

WORKSPACE = Path("/root/.openclaw/workspace")
EXTERNAL = WORKSPACE / "external"
SKILLS = WORKSPACE / "skills"

def detect_language(repo_path):
    """Detect primary language from build/config files"""
    files = [f.name for f in repo_path.iterdir() if f.is_file()]

    if "go.mod" in files:
        return "go"
    elif "Cargo.toml" in files:
        return "rust"
    elif "package.json" in files:
        return "node"
    elif "requirements.txt" in files or "pyproject.toml" in files or "setup.py" in files:
        return "python"
    elif "pom.xml" in files:
        return "java"
    elif "README.md" in files:
        # Try to infer from README
        readme = (repo_path / "README.md").read_text().lower()
        if "rust" in readme or "cargo" in readme:
            return "rust"
        if "go" in readme or "golang" in readme:
            return "go"
    return "unknown"

def is_wrapped(repo_name):
    """Check if a skill already exists for this repo"""
    # Normalize name: remove hyphens, capitalize, etc.
    possible_names = [
        repo_name.lower(),
        repo_name.lower().replace("-", ""),
        repo_name.lower().replace("-", "_"),
        repo_name.lower().replace("_", "-"),
    ]
    for skill_dir in SKILLS.iterdir():
        if skill_dir.is_dir():
            skill_name = skill_dir.name.lower()
            if any(pn in skill_name or skill_name in pn for pn in possible_names):
                return True, skill_dir.name
    return False, None

def estimate_binary_type(repo_path, language):
    """Estimate if this produces a single binary or a service"""
    files = [f.name for f in repo_path.iterdir() if f.is_file()]

    # Look for Dockerfile, docker-compose, k8s, etc. → service
    if any(f in files for f in ["Dockerfile", "docker-compose.yml", "k8s", "deployment.yaml"]):
        return "service"

    # Look for main.go, main.rs, cmd/ directory → likely single binary
    if (repo_path / "main.go").exists() or (repo_path / "cmd").exists():
        return "binary"
    if (repo_path / "main.rs").exists() or (repo_path / "src" / "main.rs").exists():
        return "binary"

    # Check README for "binary", "CLI", "command"
    if "README.md" in files:
        readme = (repo_path / "README.md").read_text().lower()
        if "cli" in readme or "command" in readme or "binary" in readme:
            return "binary"

    return "unknown"

def score_repo(repo_name, language, binary_type, is_wrapped_flag):
    """Calculate suitability score for Termux/OpenClaw (0-100)"""
    score = 0

    # Language preferences
    if language == "go":
        score += 30  # Go compiles to single binary, works great on Termux
    elif language == "rust":
        score += 25  # Rust also single binary, but build may be heavy
    elif language == "python":
        score += 10  # Python can work but heavier
    elif language == "node":
        score += 5   # Node services are heavy
    else:
        score += 0

    # Binary type
    if binary_type == "binary":
        score += 40  # Single binary is ideal
    elif binary_type == "service":
        score -= 20  # Services need runtime, harder on Termux
    else:
        score += 10

    # Already wrapped?
    if is_wrapped_flag:
        score -= 100  # Don't need to wrap again

    # Name heuristics: if it's one of our known targets, boost
    lightweight_targets = ["picoclaw", "droidclaw", "off-grid-mobile", "ollama", "gh-aw", "llmfit", "openfang", "lean-ctx"]
    if repo_name in lightweight_targets:
        score += 50

    # Penalty for heavyweight infrastructure
    heavy_keywords = ["langflow", "n8n", "flow", "studio", "ui", "dashboard", "web"]
    if any(kw in repo_name.lower() for kw in heavy_keywords):
        score -= 30

    return max(0, min(100, score))

def scan_repos():
    """Main scanner"""
    results = []

    for repo_path in EXTERNAL.iterdir():
        if not repo_path.is_dir():
            continue

        repo_name = repo_path.name
        wrapped, skill_name = is_wrapped(repo_name)
        language = detect_language(repo_path)
        binary_type = estimate_binary_type(repo_path, language)
        score = score_repo(repo_name, language, binary_type, wrapped)

        results.append({
            "repo": repo_name,
            "wrapped": wrapped,
            "skill_name": skill_name if wrapped else None,
            "language": language,
            "binary_type": binary_type,
            "score": score
        })

    # Sort by score descending
    results.sort(key=lambda x: x["score"], reverse=True)

    return results

def main():
    print("🔍 Repo Scanner — OpenClaw Skill Prioritization\n")
    print(f"Scanning: {EXTERNAL}\n")

    results = scan_repos()

    # Group by status
    wrapped = [r for r in results if r["wrapped"]]
    unwrapped = [r for r in results if not r["wrapped"]]

    print(f"✅ Already wrapped: {len(wrapped)}")
    print(f"📦 Unwrapped repos: {len(unwrapped)}\n")

    print("─" * 80)
    print("TopPriority (High score, not wrapped)")
    print("─" * 80)
    for r in unwrapped[:10]:
        print(f"{r['score']:3d} • {r['repo'][:30]:30} • {r['language']:6} • {r['binary_type']}")

    print("\n" + "─" * 80)
    print("Already Wrapped (for reference)")
    print("─" * 80)
    for r in wrapped[:10]:
        print(f"{r['score']:3d} • {r['repo'][:30]:30} → {r['skill_name']}")

    # Export JSON
    out_file = WORKSPACE / "repo_scan_results.json"
    with open(out_file, "w") as f:
        json.dump({
            "scan_ts": time.time(),
            "summary": {
                "total": len(results),
                "wrapped": len(wrapped),
                "unwrapped": len(unwrapped)
            },
            "repos": results
        }, f, indent=2)
    print(f"\n💾 Results saved to: {out_file}")

if __name__ == "__main__":
    main()
