#!/bin/bash
# OpenClaw Ghost Protocol — Emergency recovery when primary skills fail

# If this is sourced (as the skill.json action implies), execute healing
if [[ "$0" == "${BASH_SOURCE[0]}" ]]; then
    echo "[GHOST] Activating emergency protocol..."
    # Load all shadow skills and execute healing
    SHADOW_DIR=~/.openclaw/chaos/shadow_skills
    if [[ -d "$SHADOW_DIR" ]]; then
        for skill in "$SHADOW_DIR"/*.json; do
            [[ -f "$skill" ]] || continue
            CMD=$(python3 -c "import json,sys; print(json.load(open('$skill'))['healing_command'])" 2>/dev/null)
            if [[ -n "$CMD" ]]; then
                echo "[GHOST] Executing heal: $CMD"
                eval "$CMD"
            fi
        done
    fi
    echo "[GHOST] Emergency recovery complete."
fi