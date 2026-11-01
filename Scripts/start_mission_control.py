#!/usr/bin/env python3
"""
SparkVision — Java Mission Control Daemon Launcher
Starts the Java Mission Control microservice on http://localhost:8080
and verifies its health endpoint.
"""

import subprocess
import urllib.request
import json
import time
import os
import sys

MISSION_CONTROL_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "JavaMissionControl")
HEALTH_URL = "http://localhost:8080/api/v1/health"

def is_service_healthy():
    try:
        req = urllib.request.Request(HEALTH_URL)
        with urllib.request.urlopen(req, timeout=2.0) as resp:
            if resp.status == 200:
                data = json.loads(resp.read().decode("utf-8"))
                status = data.get("status")
                return status == "OK" or status == "HEALTHY"
    except Exception:
        return False
    return False

def start_service():
    if is_service_healthy():
        print("[MissionControl] Service is ALREADY RUNNING and HEALTHY at http://localhost:8080")
        return True

    print(f"[MissionControl] Starting Java Mission Control from {MISSION_CONTROL_DIR}...")
    log_file = open(os.path.join(MISSION_CONTROL_DIR, "mission_control.log"), "w")
    proc = subprocess.Popen(
        ["./gradlew", "run"],
        cwd=MISSION_CONTROL_DIR,
        stdout=log_file,
        stderr=subprocess.STDOUT
    )

    print("[MissionControl] Waiting for service to report HEALTHY (up to 20s)...")
    for i in range(20):
        time.sleep(1.0)
        if is_service_healthy():
            print(f"[MissionControl] SUCCESS: Java Mission Control online and HEALTHY (PID: {proc.pid})")
            return True
        print(".", end="", flush=True)

    print("\n[MissionControl] WARNING: Timed out waiting for health check. Check mission_control.log")
    return False

if __name__ == "__main__":
    success = start_service()
    sys.exit(0 if success else 1)
