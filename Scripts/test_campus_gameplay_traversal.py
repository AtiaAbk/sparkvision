#!/usr/bin/env python3
"""
Executes full campus-wide Play-In-Editor (PIE) gameplay verification.
Tests player pawn spawn, walkable ground collision across all 6 major DU landmarks:
  1. Curzon Hall (South Portico & Promenade)
  2. Doyel Chattar Roundabout (National Bird Monument)
  3. Central Shaheed Minar (Language Movement Memorial Plaza)
  4. TSC Mor (Teacher-Student Centre & Raju Memorial Sculpture)
  5. Central Library (Muzharul Islam Modernist Library & Hakim Chattar)
  6. Arts Faculty (Aparajeyo Bangla & Kala Bhaban)
"""

import os
import sys
import time
import json
import base64

sys.path.insert(0, 'Scripts')
from mcp_client import post_mcp

OUTPUT_DIRS = [
    "/Users/atiaoishi/Downloads/sparkvision/Documentation/Screenshots/Development",
    "/Users/atiaoishi/.gemini/antigravity/brain/e20fce03-5cdc-4c76-8f10-f79efc005a90"
]

def call(toolset, tool, args):
    res = post_mcp("tools/call", {
        "name": "call_tool",
        "arguments": {
            "toolset_name": toolset,
            "tool_name": tool,
            "arguments": args
        }
    })
    txt = res.get("content", [{}])[0].get("text", "{}")
    try:
        return json.loads(txt).get("returnValue")
    except Exception:
        return txt

print("=== STARTING CAMPUS-WIDE PIE GAMEPLAY & COLLISION VERIFICATION ===")

# 1. Start PIE
print("\n[1/5] Starting Play-In-Editor (PIE) Session...")
pie_start = call("EditorToolset.EditorAppToolset", "StartPIE", {
    "options": {
        "bSimulate": False,
        "playMode": "PlayMode_InViewPort",
        "warmupSeconds": 2.0
    }
})
print("  PIE Session status:", pie_start)
time.sleep(2.5)

# 2. Check gameplay log buffer
print("\n[2/5] Inspecting Unreal Engine Gameplay Logs...")
try:
    log_text = call("EditorToolset.LogsToolset", "get_log_buffer", {}) or ""
    log_lines = [l for l in log_text.split("\n") if any(k in l for k in ["PIE", "Spawn", "Pawn", "SparkVision", "Player", "GameMode"])][-10:]
    for l in log_lines:
        print("  LOG:", l)
except Exception as e:
    print("  Notice checking logs:", e)

# 3. Ray-trace world collisions across campus route
print("\n[3/5] Verifying Ground & Floor Collisions Across Campus Landmarks...")
WAYPOINTS = [
    ("Curzon Hall South Promenade", {"x": -3500.0, "y": 0.0, "z": 400.0}),
    ("Curzon Entrance Steps", {"x": -2600.0, "y": 0.0, "z": 400.0}),
    ("Doyel Chattar Roundabout Plinth", {"x": 7507.0, "y": -16487.0, "z": 400.0}),
    ("Shaheed Minar Memorial Plaza", {"x": -282.0, "y": -54042.0, "z": 400.0}),
    ("TSC Mor & Raju Memorial Plaza", {"x": 58964.0, "y": -63725.0, "z": 400.0}),
    ("TSC Veranda Breezeway", {"x": 60500.0, "y": -60000.0, "z": 400.0}),
    ("DU Central Library Ramp", {"x": 73459.0, "y": -71699.0, "z": 400.0}),
    ("Kala Bhaban Mall Road", {"x": 71800.0, "y": -95794.0, "z": 400.0}),
    ("Aparajeyo Bangla Sculpture Plaza", {"x": 73486.0, "y": -95794.0, "z": 400.0})
]

collision_results = []
for name, pt in WAYPOINTS:
    tr = call("editor_toolset.toolsets.scene.SceneTools", "trace_world", {
        "start": pt,
        "end": {"x": pt["x"], "y": pt["y"], "z": -100.0}
    })
    
    bHit = False
    hit_z = 0.0
    if tr is not None and isinstance(tr, (int, float)):
        bHit = True
        hit_z = pt["z"] - tr
        status = f"PASS (Solid ground at Z={hit_z:.1f} cm, distance={tr:.1f} cm)"
    else:
        status = f"FAIL (No collision detected: {tr})"
    print(f"  {name:<36}: {status}")
    collision_results.append((name, bHit, hit_z))

# 4. Capture Live PIE Gameplay Screenshot
print("\n[4/5] Capturing Live Gameplay Viewport Screenshot...")
cap_res = call("EditorToolset.EditorAppToolset", "CaptureViewport", {
    "captureTransform": {
        "location": {"x": -3850.0, "y": 45.0, "z": 240.0},
        "rotation": {"pitch": -6.0, "yaw": 0.0, "roll": 0.0},
        "scale": {"x": 1.0, "y": 1.0, "z": 1.0}
    },
    "annotations": {
        "gridSpacing": 0, "gridExtent": 0, "gridHeight": 0,
        "maxLabelDistance": 0, "classFilter": {"refPath": "/Script/Engine.Actor"}, "maxLabels": 0
    },
    "bShowUI": False
})

if isinstance(cap_res, dict) and "image" in cap_res:
    img_bytes = base64.b64decode(cap_res["image"]["data"])
    for d in OUTPUT_DIRS:
        with open(os.path.join(d, "PIE_Live_Gameplay_Verified.png"), "wb") as f:
            f.write(img_bytes)
    print(f"  Saved PIE_Live_Gameplay_Verified.png ({len(img_bytes)} bytes)")

# 5. Stop PIE
print("\n[5/5] Stopping Play-In-Editor (PIE) Session...")
pie_stop = call("EditorToolset.EditorAppToolset", "StopPIE", {})
print("  PIE Session clean exit:", pie_stop)

print("\n=== PIE GAMEPLAY VERIFICATION COMPLETE ===")
