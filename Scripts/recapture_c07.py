#!/usr/bin/env python3
import os
import json
import base64
import subprocess
import shutil

BRAIN_DIR = "/Users/atiaoishi/.gemini/antigravity/brain/e20fce03-5cdc-4c76-8f10-f79efc005a90"
CURZON_RUNTIME_DIR = "/Users/atiaoishi/Downloads/sparkvision/Documentation/CurzonHall/Screenshots/Runtime"
DOC_SCREENSHOTS_DIR = "/Users/atiaoishi/Downloads/sparkvision/Documentation/Screenshots"

def run_mcp(toolset, tool, args):
    res = subprocess.check_output([
        "/Users/atiaoishi/Downloads/sparkvision/Scripts/mcp_client.py",
        "call", toolset, tool, json.dumps(args)
    ])
    return json.loads(res) if res.strip() else {}

def recapture_c07():
    print("Recapturing C07_Curzon_Courtyard_Inner_View...")
    # Deselect actors
    run_mcp("EditorToolset.EditorAppToolset", "SelectActors", {"actors": []})
    
    loc = {"x": -2460.0, "y": -1400.0, "z": 180.0}
    rot = {"pitch": -2.0, "yaw": -90.0, "roll": 0.0}
    
    cap_args = {
        "captureTransform": {
            "location": loc,
            "rotation": rot,
            "scale": {"x": 1.0, "y": 1.0, "z": 1.0}
        },
        "annotations": {
            "gridSpacing": 0, "gridExtent": 0, "gridHeight": 0,
            "maxLabelDistance": 0, "classFilter": {"refPath": "/Script/Engine.Actor"}, "maxLabels": 0
        },
        "bShowUI": False
    }
    cap_res = run_mcp("EditorToolset.EditorAppToolset", "CaptureViewport", cap_args)
    img_b64 = None
    if isinstance(cap_res, dict):
        ret = cap_res.get("returnValue", {})
        if isinstance(ret, dict) and "image" in ret:
            img_b64 = ret["image"].get("data")
        elif "image" in cap_res:
            img_b64 = cap_res["image"].get("data")
            
    if not img_b64:
        print("[ERROR] Failed to capture image from Unreal MCP.")
        return False
        
    raw = base64.b64decode(img_b64)
    filename = "C07_Curzon_Courtyard_Inner_View.png"
    
    targets = [
        os.path.join(CURZON_RUNTIME_DIR, filename),
        os.path.join(DOC_SCREENSHOTS_DIR, filename),
        os.path.join(BRAIN_DIR, filename)
    ]
    
    for t in targets:
        os.makedirs(os.path.dirname(t), exist_ok=True)
        with open(t, "wb") as f:
            f.write(raw)
        print(f"Saved: {t} ({len(raw):,} bytes)")
        
    return True

if __name__ == "__main__":
    recapture_c07()
