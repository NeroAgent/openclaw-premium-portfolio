#!/usr/bin/env python3
"""
RAM check — reports memory usage and availability.
"""

import subprocess
import sys
import json

def parse_size(kb_str):
    """Convert KB string to bytes."""
    try:
        kb = int(kb_str)
        return kb * 1024
    except:
        return 0

def check():
    result = {
        "total_bytes": 0,
        "used_bytes": 0,
        "free_bytes": 0,
        "swap_total_bytes": 0,
        "swap_free_bytes": 0,
        "status": "ok",
        "reason": ""
    }

    try:
        # Read /proc/meminfo for reliable numbers
        meminfo = {}
        with open("/proc/meminfo", "r") as f:
            for line in f:
                parts = line.split(":")
                if len(parts) == 2:
                    key = parts[0].strip()
                    val = parts[1].strip().split()[0]
                    meminfo[key] = int(val)

        total_kb = meminfo.get("MemTotal", 0)
        free_kb = meminfo.get("MemFree", 0)
        available_kb = meminfo.get("MemAvailable", 0)  # Best estimate of available memory
        swap_total_kb = meminfo.get("SwapTotal", 0)
        swap_free_kb = meminfo.get("SwapFree", 0)

        result["total_bytes"] = total_kb * 1024
        result["free_bytes"] = available_kb * 1024 if available_kb > 0 else free_kb * 1024
        result["used_bytes"] = result["total_bytes"] - result["free_bytes"]
        result["swap_total_bytes"] = swap_total_kb * 1024
        result["swap_free_bytes"] = swap_free_kb * 1024

        # Determine status
        free_gb = result["free_bytes"] / (1024**3)
        if free_gb < 0.5:  # Less than 500MB
            result["status"] = "critical"
            result["reason"] = f"Only {free_gb:.2f} GB free RAM"
        elif free_gb < 1.0:
            result["status"] = "warning"
            result["reason"] = f"Only {free_gb:.2f} GB free RAM"
        else:
            result["reason"] = f"{free_gb:.2f} GB free"

    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)

    return result

if __name__ == "__main__":
    print(json.dumps(check(), indent=2))
