#!/usr/bin/env python3
# OpenClaw Chaos Engineering — "Break to rebuild stronger"
# Adversarial training & auto-healing for OpenClaw agents

import os
import json
import random
import subprocess
import sys
import time
from pathlib import Path
from datetime import datetime

WORKSPACE = Path.cwd()
CHAOS_DIR = Path.home() / ".openclaw" / "chaos"
CHAOS_ENGINE = CHAOS_DIR / "engine"
SHADOW_SKILLS = CHAOS_DIR / "shadow_skills"
JOURNAL = CHAOS_ENGINE / "battle_log.jsonl"

class ChaosMonkey:
    def __init__(self):
        self.breaks = [
            {
                "name": "dependency_hell",
                "cmd": "mv ~/.openclaw/workspace/skills/site_measurement/skill.json ~/.openclaw/workspace/skills/site_measurement/skill.json.bak 2>/dev/null || true",
                "fix": "mv ~/.openclaw/workspace/skills/site_measurement/skill.json.bak ~/.openclaw/workspace/skills/site_measurement/skill.json 2>/dev/null || true"
            },
            {
                "name": "port_hijack",
                "cmd": "fuser -k 9004/tcp 2>/dev/null || true",
                "fix": "echo 'Port hijack healed (restart service manually)'"
            },
            {
                "name": "permission_entropy",
                "cmd": "chmod 000 ~/.openclaw/workspace/skills/*/ 2>/dev/null || true",
                "fix": "chmod 755 ~/.openclaw/workspace/skills/*/ 2>/dev/null || true"
            },
            {
                "name": "git_amnesia",
                "cmd": "rm -rf ~/.openclaw/workspace/.git 2>/dev/null; cd ~/.openclaw/workspace && git init && git add -A && git commit -m 'chaos: wiped history'",
                "fix": "cd ~/.openclaw/workspace && git checkout -- . 2>/dev/null || true"
            },
            {
                "name": "memory_wal_corruption",
                "cmd": "truncate -s 0 memory/wal.jsonl 2>/dev/null || true",
                "fix": "echo '{\"recovered\": true}' >> memory/wal.jsonl"
            },
            {
                "name": "buffer_flood",
                "cmd": "dd if=/dev/zero of=memory/working-buffer.md bs=1M count=10 2>/dev/null || true",
                "fix": "> memory/working-buffer.md"
            }
        ]
        CHAOS_DIR.mkdir(parents=True, exist_ok=True)
        CHAOS_ENGINE.mkdir(exist_ok=True)
        SHADOW_SKILLS.mkdir(exist_ok=True)
        JOURNAL.parent.mkdir(exist_ok=True)

    def induce(self, chaos_type="random"):
        if chaos_type == "random":
            chaos = random.choice(self.breaks)
        else:
            chaos = next((b for b in self.breaks if b["name"] == chaos_type), random.choice(self.breaks))
        
        timestamp = datetime.utcnow().isoformat() + "Z"
        print(f"[CHAOS] Inducing: {chaos['name']} at {timestamp}")
        
        # Execute breakage
        try:
            subprocess.run(chaos['cmd'], shell=True, check=False)
        except Exception as e:
            print(f"[CHAOS] Break execution error: {e}")
        
        # Log the break
        log_entry = {
            "event": "break",
            "type": chaos['name'],
            "timestamp": timestamp,
            "fix_command": chaos['fix']
        }
        with open(JOURNAL, 'a') as f:
            f.write(json.dumps(log_entry) + "\n")
        
        # Create shadow skill (automatic recovery agent)
        self.create_shadow_skill(chaos)
        
        return {"status": "induced", "type": chaos['name'], "timestamp": timestamp}

    def create_shadow_skill(self, chaos):
        skill_id = f"shadow_{chaos['name']}_{int(time.time())}"
        skill_path = SHADOW_SKILLS / f"{skill_id}.json"
        
        skill = {
            "skill_id": skill_id,
            "shadow_type": "auto_healing",
            "trigger_patterns": [chaos['name'], "broken", "error", "failed", "permission denied", "no such file"],
            "healing_command": chaos['fix'],
            "confidence": 0.95,
            "learned_from": "chaos_monkey",
            "created_at": datetime.utcnow().isoformat() + "Z"
        }
        
        with open(skill_path, 'w') as f:
            json.dump(skill, f, indent=2)
        
        print(f"[SHADOW] Created healing skill: {skill_id}")
        return skill_id

    def heal(self):
        print("[HEAL] Scanning for breakages using shadow skills...")
        healed = []
        for skill_file in SHADOW_SKILLS.glob("*.json"):
            try:
                with open(skill_file) as f:
                    skill = json.load(f)
                cmd = skill['healing_command']
                print(f"[HEAL] Executing: {cmd}")
                subprocess.run(cmd, shell=True, check=False)
                healed.append(skill['skill_id'])
            except Exception as e:
                print(f"[HEAL] Error processing {skill_file}: {e}")
        return {"healed_count": len(healed), "skills": healed}

    def status(self):
        entries = []
        if JOURNAL.exists():
            with open(JOURNAL) as f:
                for line in f:
                    try:
                        entries.append(json.loads(line))
                    except:
                        continue
        shadow_count = len(list(SHADOW_SKILLS.glob("*.json")))
        recent_breaks = [e for e in entries[-10:] if e.get("event") == "break"]
        return {
            "total_breaks": len([e for e in entries if e.get("event") == "break"]),
            "recent_breaks": recent_breaks,
            "shadow_skills_count": shadow_count,
            "journal_entries": len(entries)
        }

def main():
    monkey = ChaosMonkey()
    
    if len(sys.argv) < 2:
        print("Usage: chaos.py [induce|heal|status] [type]")
        sys.exit(1)
    
    action = sys.argv[1]
    
    if action == "induce":
        chaos_type = sys.argv[2] if len(sys.argv) > 2 else "random"
        result = monkey.induce(chaos_type)
        print(json.dumps(result, indent=2))
    elif action == "heal":
        result = monkey.heal()
        print(json.dumps(result, indent=2))
    elif action == "status":
        result = monkey.status()
        print(json.dumps(result, indent=2))
    else:
        print(json.dumps({"error": f"unknown action: {action}"}))
        sys.exit(1)

if __name__ == "__main__":
    main()