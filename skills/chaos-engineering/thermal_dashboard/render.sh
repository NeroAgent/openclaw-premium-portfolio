#!/bin/bash
# OpenClaw Chaos Engineering — Thermal Dashboard

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
RESET='\033[0m'

clear
echo -e "${CYAN}╔══════════════════════════════════════════════════╗${RESET}"
echo -e "${CYAN}║   OpenClaw — Chaos Engineering Dashboard       ║${RESET}"
echo -e "${CYAN}╚══════════════════════════════════════════════════╝${RESET}"
echo ""

# Load memory stack health if available
WAL_COUNT=0
BUF_SIZE=0
UTIL_PCT=0
if [[ -f memory/wal.jsonl ]]; then
    WAL_COUNT=$(wc -l < memory/wal.jsonl 2>/dev/null || echo 0)
fi
if [[ -f memory/working-buffer.md ]]; then
    BUF_SIZE=$(stat -c%s memory/working-buffer.md 2>/dev/null || echo 0)
fi
# Estimate token utilization from buffer (rough)
if [[ $BUF_SIZE -gt 0 ]]; then
    UTIL_PCT=$(( (BUF_SIZE * 2) / 1200 ))  # rough chars->tokens and scale to 120k context
    [[ $UTIL_PCT -gt 100 ]] && UTIL_PCT=100
fi

# Skill registry health
TOTAL_SKILLS=0
HEALTHY_SKILLS=0
if [[ -f skill_registry.json ]]; then
    TOTAL_SKILLS=$(python3 -c "import json; print(len(json.load(open('skill_registry.json'))['skills']))" 2>/dev/null || echo 0)
    HEALTHY_SKILLS=$(python3 -c "import json; data=json.load(open('skill_registry.json')); print(sum(1 for s in data['skills'].values() if s.get('health',0)>=80))" 2>/dev/null || echo 0)
fi

# Shadow skills count
SHADOW_COUNT=$(ls ~/.openclaw/chaos/shadow_skills/ 2>/dev/null | wc -l)

# Recent breaks
RECENT_BREAKS=$(tail -5 ~/.openclaw/chaos/engine/battle_log.jsonl 2>/dev/null | wc -l)

echo -e "${MAGENTA}┌─ Chaos Engineering Status ──────────────────────┐${RESET}"
printf "│ Shadow Skills (auto-heal): %-18s │\n" "$SHADOW_COUNT"
printf "│ Recent Chaos Events:     %-18s │\n" "$RECENT_BREAKS"
echo -e "${MAGENTA}└─────────────────────────────────────────────────┘${RESET}"
echo ""

echo -e "${MAGENTA}┌─ OpenClaw Memory Stack ─────────────────────────┐${RESET}"
printf "│ WAL entries:             %-18s │\n" "$WAL_COUNT"
printf "│ Working buffer:          %-10s bytes │\n" "$BUF_SIZE"
printf "│ Est. token util:         %-14s %% │\n" "$UTIL_PCT"
echo -e "${MAGENTA}└─────────────────────────────────────────────────┘${RESET}"
echo ""

echo -e "${MAGENTA}┌─ Skill Registry ─────────────────────────────────┐${RESET}"
printf "│ Total skills:            %-18s │\n" "$TOTAL_SKILLS"
printf "│ Healthy:                 %-18s │\n" "$HEALTHY_SKILLS"
echo -e "${MAGENTA}└─────────────────────────────────────────────────┘${RESET}"
echo ""

# Thermal gradient based on WAL activity (more WAL = hotter)
THERMAL_LEVEL=$(( WAL_COUNT % 5 ))
if [[ $THERMAL_LEVEL -lt 2 ]]; then
    THERMAL_COLOR=$GREEN
    THERMAL_TEXT="🟢 Cool"
elif [[ $THERMAL_LEVEL -lt 4 ]]; then
    THERMAL_COLOR=$YELLOW
    THERMAL_TEXT="🟡 Warm"
else
    THERMAL_COLOR=$RED
    THERMAL_TEXT="🔴 Hot"
fi

echo -e "${MAGENTA}┌─ Thermal State ──────────────────────────────────┐${RESET}"
printf "│ System Temperature:      %-18s │\n" "$THERMAL_TEXT"
echo -e "${MAGENTA}└─────────────────────────────────────────────────┘${RESET}"
echo ""

echo -e "${CYAN}Commands:${RESET}"
echo "  chaos.py induce [type]   — induce breakage"
echo "  chaos.py heal            — auto-heal from shadow skills"
echo "  chaos.py status          — show chaos journal"
echo "  thermal                  — refresh this dashboard"
echo ""
echo -e "${CYAN}Chaos types:${RESET} dependency_hell, port_hijack, permission_entropy, git_amnesia, memory_wal_corruption, buffer_flood"
echo ""
echo -e "${CYAN}Example:${RESET} chaos.py induce memory_wal_corruption"