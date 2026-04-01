#!/usr/bin/env python3
"""
CPU check — core count, load average, optional temperature.
"""

import os
import sys
import subprocess
import json
import json as json_mod

def check():
    result = {
        "cores": 0,
        "load1": 0.0,
        "load5": 0.0,
        "load15": 0.0,
        "temperature_celsius": None,
        "status": "ok",
        "reason": ""
    }

    try:
        # Get core count
        try:
            with open("/proc/cpuinfo", "r") as f:
                result["cores"] = sum(1 for line in f if line.strip().startswith("processor"))
        except:
            result["cores"] = os.cpu_count() or 1

        # Get load average
        with open("/proc/loadavg", "r") as f:
            loadavgs = f.read().split()[:3]
            result["load1"], result["load5"], result["load15"] = [float(x) for x in loadavgs]

        # Check temperature (may not be accessible)
        # Try common Android thermal zones
        temp_paths = [
            "/sys/class/thermal/thermal_zone0/temp",
            "/sys/class/hwmon/hwmon0/temp1_input",
        ]
        for path in temp_paths:
            if os.path.exists(path):
                try:
                    with open(path, "r") as f:
                        temp_milli = int(f.read().strip())
                        result["temperature_celsius"] = temp_milli / 1000.0
                        break
                except:
                    pass

        # Evaluate load
        load_ratio = result["load1"] / result["cores"] if result["cores"] > 0 else 0
        if load_ratio > 1.5:
            result["status"] = "warning"
            result["reason"] = f"Load {result['load1']:.2f} > {result['cores']} cores"
        elif load_ratio > 2.0:
            result["status"] = "critical"
            result["reason"] = f"Load {result['load1']:.2f} >> {result['cores']} cores"
        else:
            result["reason"] = f"Load {result['load1']:.2f}/{result['cores']} cores"

    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)

    return result

if __name__ == "__main__":
    print(json.dumps(check(), indent=2))
