#!/bin/bash
# NEROCLAW SURPRISE DAEMON — Adversarial training every 3 hours

# This daemon runs indefinitely, intentionally breaking the system every 10800 seconds (3 hours)
# to build resilience through recovery. Only triggers when the system is stable (vision service running).

CHRONOS_INTERVAL=10800  # 3 hours

echo "[SURPRISE] Daemon starting — will induce chaos every $((CHRONOS_INTERVAL/3600)) hours if system is stable..."

while true; do
    sleep $CHRONOS_INTERVAL
    
    # Check system stability before breaking (if vision service is up, we're healthy enough to break)
    if pgrep -f "vision_service.py" > /dev/null; then
        echo "[SURPRISE] $(date): Inducing chaos for adversarial training..."
        python3 ~/.neroclaw/surprise/chaos_engine/monkey.py break
        
        # Optional notification (Termux)
        termux-notification --title "NeroClaw Chaos Event" \
            --content "System intentionally broken. Shadow skill created. Run 'chaos.py heal' to fix." \
            2>/dev/null || true
    else
        echo "[SURPRISE] $(date): System unstable — skipping chaos cycle"
    fi
done