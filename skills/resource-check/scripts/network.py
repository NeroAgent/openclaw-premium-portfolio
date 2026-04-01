#!/usr/bin/env python3
"""
Network check — connectivity and latency.
"""

import subprocess
import sys
import json
import socket

def check():
    result = {
        "online": False,
        "latency_ms": None,
        "metered": None,  # Unknown on Android without extra APIs
        "status": "ok",
        "reason": ""
    }

    # Quick connectivity check (ping 8.8.8.8 with 1 packet, 2s timeout)
    try:
        # Try ping
        out = subprocess.run(
            ["ping", "-c", "1", "-W", "2", "8.8.8.8"],
            capture_output=True,
            text=True,
            timeout=3
        )
        if out.returncode == 0:
            result["online"] = True
            # Extract time from ping output
            import re
            match = re.search(r"time=([\d.]+) ms", out.stdout)
            if match:
                result["latency_ms"] = float(match.group(1))
    except (subprocess.TimeoutExpired, FileNotFoundError):
        # Fallback: try TCP connect to google.com:443
        try:
            s = socket.create_connection(("8.8.8.8", 53), timeout=2)
            s.close()
            result["online"] = True
            result["latency_ms"] = None
        except:
            result["online"] = False

    if not result["online"]:
        result["status"] = "critical"
        result["reason"] = "No network connectivity"
    else:
        result["status"] = "ok"
        if result["latency_ms"]:
            result["reason"] = f"Online, {result['latency_ms']:.0f}ms latency"
        else:
            result["reason"] = "Online (latency unknown)"

    return result

if __name__ == "__main__":
    print(json.dumps(check(), indent=2))
