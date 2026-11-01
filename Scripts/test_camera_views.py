import sys
import os
import json
import base64
import subprocess

BRAIN_DIR = "/Users/atiaoishi/.gemini/antigravity/brain/e20fce03-5cdc-4c76-8f10-f79efc005a90"

def run_mcp(toolset, tool, args):
    res = subprocess.check_output([
        "/Users/atiaoishi/Downloads/sparkvision/Scripts/mcp_client.py",
        "call", toolset, tool, json.dumps(args)
    ])
    return json.loads(res) if res.strip() else {}

def capture_one(name, loc, rot):
    # Deselect any actors first
    run_mcp("EditorToolset.EditorAppToolset", "SelectActors", {"actors": []})
    
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
            
    if img_b64:
        raw = base64.b64decode(img_b64)
        out_path = os.path.join(BRAIN_DIR, f"{name}.png")
        with open(out_path, "wb") as f:
            f.write(raw)
        print(f"[CAPTURED] {name} -> {out_path} ({len(raw):,} bytes)")
        return out_path
    else:
        print(f"[FAILED] {name}")
        return None

if __name__ == "__main__":
    test_cams = [
        # C04 test options
        {
            "name": "test_c04_high_pitch",
            "loc": {"x": 2200.0, "y": 0.0, "z": 2200.0},
            "rot": {"pitch": -22.0, "yaw": 180.0, "roll": 0.0}
        },
        {
            "name": "test_c04_closer_elevated",
            "loc": {"x": 200.0, "y": 0.0, "z": 800.0},
            "rot": {"pitch": -12.0, "yaw": 180.0, "roll": 0.0}
        },
        # C05 West side
        {
            "name": "test_c05_west",
            "loc": {"x": -2500.0, "y": -9500.0, "z": 900.0},
            "rot": {"pitch": -6.0, "yaw": 90.0, "roll": 0.0}
        },
        # C06 East side
        {
            "name": "test_c06_east",
            "loc": {"x": -2500.0, "y": 9500.0, "z": 900.0},
            "rot": {"pitch": -6.0, "yaw": -90.0, "roll": 0.0}
        },
        # C07 Courtyard inner view
        {
            "name": "test_c07_inner",
            "loc": {"x": 800.0, "y": -2000.0, "z": 450.0},
            "rot": {"pitch": -6.0, "yaw": 155.0, "roll": 0.0}
        },
        # ENV_03 Bamboo
        {
            "name": "test_env03_bamboo",
            "loc": {"x": -800.0, "y": 3200.0, "z": 180.0},
            "rot": {"pitch": 2.0, "yaw": -80.0, "roll": 0.0}
        },
        # ENV_08 Lake reflection
        {
            "name": "test_env08_lake",
            "loc": {"x": 6200.0, "y": 1000.0, "z": 300.0},
            "rot": {"pitch": -8.0, "yaw": 195.0, "roll": 0.0}
        }
    ]
    for cam in test_cams:
        capture_one(cam["name"], cam["loc"], cam["rot"])
