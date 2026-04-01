#!/usr/bin/env python3
"""
Battery check — level, charging state, estimate.
"""

import os
import sys
import json
import subprocess

def check():
    result = {
        "level_percent": None,
        "is_charging": None,
        "estimated_runtime_minutes": None,
        "status": "ok",
        "reason": ""
    }

    # Try Termux:API first (if installed)
    try:
        # Check if termux-battery-status command exists
        subprocess.run(["which", "termux-battery-status"], check=True, capture_output=True)
        out = subprocess.run(["termux-battery-status"], capture_output=True, text=True)
        if out.returncode == 0:
            import re
            data = out.stdout
            # Parse JSON-like output
            level_match = re.search(r'"level":\s*(\d+)', data)
            status_match = re.search(r'"status":\s*"([^"]+)"', data)
            if level_match:
                result["level_percent"] = int(level_match.group(1))
            if status_match:
                result["is_charging"] = (status_match.group(1) == "CHARGING")
    except:
        pass

    # Fallback: check /sys/class/power_supply
    if result["level_percent"] is None:
        for base in ["/sys/class/power_supply", "/proc/acpi"]:
            if os.path.exists(base):
                for p in os.listdir(base):
                    if p.startswith("battery"):
                        bat_path = os.path.join(base, p)
                        capacity_path = os.path.join(bat_path, "capacity")
                        status_path = os.path.join(bat_path, "status")
                        if os.path.exists(capacity_path):
                            try:
                                with open(capacity_path) as f:
                                    result["level_percent"] = int(f.read().strip())
                            except:
                                pass
                        if os.path.exists(status_path):
                            try:
                                with open(status_path) as f:
                                    status = f.read().strip().lower()
                                    result["is_charging"] = ("charging" in status or "full" in status)
                            except:
                                pass
                        break

    # If still unknown, set to None and status info
    if result["level_percent"] is None:
        result["level_percent"] = None
        result["is_charging"] = None
        result["status"] = "info"
        result["reason"] = "Battery status unavailable (no Termux:API or sysfs)"
        return result

    # Determine status
    level = result["level_percent"]
    charging = result["is_charging"]
    if level < 20 and not charging:
        result["status"] = "critical"
        result["reason"] = f"Battery at {level}% and not charging"
    elif level < 10 and not charging:
        result["status"] = "critical"
        result["reason"] = f"Battery critically low at {level}%"
    elif not charging and level < 50:
        result["status"] = "warning"
        result["reason"] = f"Battery at {level}% not charging"
    else:
        result["reason"] = f"Battery at {level}% {'(charging)' if charging else '(discharging)'}"

    return result

if __name__ == "__main__":
    print(json.dumps(check(), indent=2))
