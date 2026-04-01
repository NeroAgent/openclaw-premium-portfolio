#!/usr/bin/env python3
"""
Storage check — available space on Termux home and external storage.
"""

import os
import sys
import shutil
import json
import json as json_mod

def parse_size(s):
    """Convert human-friendly size to bytes."""
    s = s.strip().upper()
    if s[-1] in ('K', 'M', 'G'):
        mult = {'K': 1024, 'M': 1024**2, 'G': 1024**3}[s[-1]]
        return int(float(s[:-1]) * mult)
    return int(s)

def check():
    result = {
        "home_bytes_total": 0,
        "home_bytes_free": 0,
        "external_bytes_total": 0,
        "external_bytes_free": 0,
        "status": "ok",
        "reason": ""
    }

    paths = [
        os.path.expanduser("~"),  # Termux home
        "/storage/emulated/0",    # External storage (may not exist)
    ]

    try:
        home_path = paths[0]
        if os.path.exists(home_path):
            total, used, free = shutil.disk_usage(home_path)
            result["home_bytes_total"] = total
            result["home_bytes_free"] = free

        ext_path = paths[1]
        if os.path.exists(ext_path):
            total, used, free = shutil.disk_usage(ext_path)
            result["external_bytes_total"] = total
            result["external_bytes_free"] = free
        else:
            result["external_bytes_total"] = 0
            result["external_bytes_free"] = 0

        # Overall status based on home free space (primary)
        free_gb = result["home_bytes_free"] / (1024**3)
        if free_gb < 2:
            result["status"] = "critical"
            result["reason"] = f"Only {free_gb:.2f} GB free on home"
        elif free_gb < 5:
            result["status"] = "warning"
            result["reason"] = f"Only {free_gb:.2f} GB free on home"
        else:
            result["reason"] = f"{free_gb:.2f} GB free on home"

    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)

    return result

if __name__ == "__main__":
    print(json.dumps(check(), indent=2))
