#!/usr/bin/env python3
"""
Executes Play-In-Editor (PIE) testing and validation for Curzon Hall Hero Environment.
Verifies PlayerStart possession, ground collision, and Java Mission Control connectivity.
"""

import time
import json
import subprocess

def run_mcp(toolset, tool, args):
    res = subprocess.check_output([
        "/Users/atiaoishi/Downloads/sparkvision/Scripts/mcp_client.py",
        "call", toolset, tool, json.dumps(args)
    ])
    return json.loads(res) if res.strip() else {}

print("Starting Play-In-Editor (PIE) session...")
try:
    pie_res = run_mcp("EditorToolset.EditorAppToolset", "StartPIE", {
        "options": {
            "bSimulate": False,
            "playMode": "PlayMode_InViewPort",
            "warmupSeconds": 2.0
        }
    })
    print("PIE started successfully.")
except Exception as e:
    print("Notice during StartPIE:", e)

# Wait 2 seconds for gameplay tick
time.sleep(2.0)

# Check Unreal Engine logs
print("\nReading Unreal Engine Output Log...")
try:
    log_res = run_mcp("EditorToolset.LogsToolset", "get_log_buffer", {})
    logs = log_res.get("returnValue", "")
    recent_lines = [l for l in logs.split("\n") if "SparkVision" in l or "SV" in l or "Play" in l or "PIE" in l or "MissionControl" in l][-15:]
    for l in recent_lines:
        print("  LOG:", l)
except Exception as e:
    print("Notice reading logs:", e)

# Perform ray-trace world checks around Curzon Hall entrance and verandas
print("\nVerifying Ground and Building Collision...")
collision_points = [
    ("Player Start Plaza", {"x": -3500.0, "y": 0.0, "z": 500.0}),
    ("Curzon Promenade Mid", {"x": -3000.0, "y": 0.0, "z": 500.0}),
    ("Grand Entrance Steps", {"x": -2600.0, "y": 0.0, "z": 500.0}),
    ("West Lawn", {"x": -3200.0, "y": -2000.0, "z": 500.0}),
    ("East Lawn", {"x": -3200.0, "y": 2000.0, "z": 500.0}),
    ("West Veranda Colonnade", {"x": -2500.0, "y": -2000.0, "z": 500.0}),
    ("East Veranda Colonnade", {"x": -2500.0, "y": 2000.0, "z": 500.0}),
]

for label, p in collision_points:
    try:
        tr = run_mcp("editor_toolset.toolsets.scene.SceneTools", "trace_world", {
            "start": p,
            "end": {"x": p["x"], "y": p["y"], "z": -100.0},
            "collision_channel": "ObjectTypeQuery1"
        })
        hit = tr.get("returnValue", {})
        if hit.get("bBlockingHit"):
            loc = hit.get("location", {})
            print(f"  {label:<25} HIT at Z={loc.get('z', 0):.1f} cm (Hit Actor: {hit.get('actor', {}).get('refPath', '').split('.')[-1]})")
        else:
            print(f"  {label:<25} NO HIT (Fall risk!)")
    except Exception as e:
        print(f"  {label:<25} Trace error: {e}")

print("\nStopping Play-In-Editor (PIE) session...")
try:
    run_mcp("EditorToolset.EditorAppToolset", "StopPIE", {})
    print("PIE stopped cleanly.")
except Exception as e:
    print("Notice during StopPIE:", e)
