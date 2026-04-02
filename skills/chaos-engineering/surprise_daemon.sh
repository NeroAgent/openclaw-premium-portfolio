#!/bin/bash
# OpenClaw Chaos Daemon — Adversarial training every 3 hours

# This daemon runs indefinitely, intentionally breaking the system every 10800 seconds (3 hours)
# to build resilience through recovery. Only triggers when the system is stable.

CHRONOS_INTERVAL=10800  # 3 hours

echo "[CHAOS] Daemon starting — will induce chaos every $((CHRONOS_INTERVAL/3600)) hours if system is stable..."

while true; do
    sleep $CHRONOS_INTERVAL
    
    # Check system stability before breaking (if memory stack is active, we're healthy enough)
    if [[ -f memory/wal.jsonl ]]; then
        echo "[CHAOS] $(date): Inducing chaos for adversarial training..."
        python3 ~/.openclaw/chaos/engine/monkey.py break
        
        # Optional notification (Termux)
        termux-notification --title "OpenClaw Chaos Event" \
            --content "System intentionally broken. Shadow skill created. Run 'chaos.py heal' to fix." \
            2>/dev/null || true
    else
        echo "[CHAOS] $(date): Memory stack not active — skipping chaos cycle"
    fi
done