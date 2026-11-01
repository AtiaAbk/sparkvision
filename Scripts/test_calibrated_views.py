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
    test_shots = [
        # --- C04 Options ---
        # Looking South towards Curzon rear entrance portal (at X=-2500, Y=0)
        # Tree canopies are at X=-1600, -900, -800, -400.
        # Option A: In courtyard between trees and facade (X=-1800, Y=0, Z=450)
        {
            "name": "eval_c04_optA",
            "loc": {"x": -1850.0, "y": 0.0, "z": 450.0},
            "rot": {"pitch": -5.0, "yaw": 180.0, "roll": 0.0}
        },
        # Option B: In courtyard looking wide with subtle angle (X=-1950, Y=300, Z=500)
        {
            "name": "eval_c04_optB",
            "loc": {"x": -1950.0, "y": 300.0, "z": 500.0},
            "rot": {"pitch": -8.0, "yaw": 188.0, "roll": 0.0}
        },
        # Option C: High aerial framing from north edge over trees (X=1800, Y=0, Z=2400)
        {
            "name": "eval_c04_optC",
            "loc": {"x": 1800.0, "y": 0.0, "z": 2400.0},
            "rot": {"pitch": -26.0, "yaw": 180.0, "roll": 0.0}
        },

        # --- C07 Options ---
        # Colonnade gallery perspective (Veranda lower arches at X=-2500, Y=-1300 to -5300)
        # Option A: Walking down the West colonnade gallery looking West towards the tower
        {
            "name": "eval_c07_colonnade_inside_west",
            "loc": {"x": -2500.0, "y": -1600.0, "z": 180.0},
            "rot": {"pitch": 0.0, "yaw": -90.0, "roll": 0.0}
        },
        # Option B: Walking down the West colonnade gallery looking East towards the entrance portal
        {
            "name": "eval_c07_colonnade_inside_east",
            "loc": {"x": -2500.0, "y": -4800.0, "z": 180.0},
            "rot": {"pitch": 0.0, "yaw": 90.0, "roll": 0.0}
        },
        # Option C: Oblique courtyard angle viewing the shaded colonnade from garden
        {
            "name": "eval_c07_colonnade_garden_view",
            "loc": {"x": -2000.0, "y": -2200.0, "z": 220.0},
            "rot": {"pitch": -4.0, "yaw": -130.0, "roll": 0.0}
        },

        # --- ENV_03 Options ---
        # Bamboo thickets at X=-300, Y=2500, 3500, 4500 (East) and -2500, -3500, -4500 (West)
        # Option A: East bamboo cluster from pathway
        {
            "name": "eval_env03_bamboo_east",
            "loc": {"x": -550.0, "y": 2800.0, "z": 150.0},
            "rot": {"pitch": 2.0, "yaw": 60.0, "roll": 0.0}
        },
        # Option B: West bamboo cluster from garden path
        {
            "name": "eval_env03_bamboo_west",
            "loc": {"x": -550.0, "y": -2800.0, "z": 150.0},
            "rot": {"pitch": 2.0, "yaw": -120.0, "roll": 0.0}
        },
        # Option C: Closer direct shot of golden bamboo cluster
        {
            "name": "eval_env03_bamboo_close",
            "loc": {"x": -420.0, "y": 3200.0, "z": 120.0},
            "rot": {"pitch": 4.0, "yaw": 40.0, "roll": 0.0}
        },

        # --- ENV_08 Options ---
        # Shahidullah Lake Ecology: Palms at X=12500..17500, Y=20500..22500, Lilies at X=14500, Y=23000
        # Option A: Looking NE across the lake towards palms and lilies
        {
            "name": "eval_env08_lake_optA",
            "loc": {"x": 11500.0, "y": 19500.0, "z": 320.0},
            "rot": {"pitch": -8.0, "yaw": 45.0, "roll": 0.0}
        },
        # Option B: Elevated lakeside view overlooking palms, reeds, lilies
        {
            "name": "eval_env08_lake_optB",
            "loc": {"x": 12000.0, "y": 18500.0, "z": 450.0},
            "rot": {"pitch": -12.0, "yaw": 40.0, "roll": 0.0}
        },
        # Option C: Water level view near the lilies looking across to jarul & palms
        {
            "name": "eval_env08_lake_optC",
            "loc": {"x": 13800.0, "y": 21000.0, "z": 150.0},
            "rot": {"pitch": -5.0, "yaw": 55.0, "roll": 0.0}
        }
    ]

    for s in test_shots:
        capture_one(s["name"], s["loc"], s["rot"])
