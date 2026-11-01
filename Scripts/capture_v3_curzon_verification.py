#!/usr/bin/env python3
"""
Curzon Hall v3 Verification Capture Suite
Executes preflight cleanup (parking helper lights, hiding debug shapes, clearing selection)
and captures all primary viewpoints reflecting the user-requested updates:
- C01: Full Front Elevation (Open front lawn, two tall palms, 4 chhatris + 3 merlons, 12 bays)
- C02: Front-Left Oblique (West wing, SW 25.2m tower, palms, low hedge)
- C03: Front-Right Oblique (East wing, SE tower, Physics wing signboard)
- C07: Inner Veranda Walkway Corridor (Real wooden double doors, arched fanlights, shuttered windows)
- C08: Monumental Entrance Portico Closeup (6-step staircase, grand iwan, recessed double doors, brass handles)
- C09: Central Tower Top Closeup (4 corner chhatris + 3 intermediate merlons, 6 lancet niches, 2 rosettes, chhajja, 3-light jali window)
- C11: Veranda Arches Closeup (Doors and shuttered windows along inner wall, horseshoe & cusped arches, jali balustrade)
- C12: Gameplay Promenade Walk (Human eye level approaching past the two palms and low hedges)
"""

import os
import json
import base64
import subprocess
import shutil

BRAIN_DIR = "/Users/atiaoishi/.gemini/antigravity/brain/e20fce03-5cdc-4c76-8f10-f79efc005a90"
CURZON_RUNTIME_DIR = "/Users/atiaoishi/Downloads/sparkvision/Documentation/CurzonHall/Screenshots/Runtime"
DOC_SCREENSHOTS_DIR = "/Users/atiaoishi/Downloads/sparkvision/Documentation/Screenshots"

CURZON_CAMERAS_V3 = [
    {
        "id": "C01",
        "name": "C01_Curzon_Full_Front_Elevation",
        "desc": "Full South Elevation showing 128m facade, 2 tall palms, 4 chhatris + 3 merlons, and open lawn",
        "location": {"x": -7200.0, "y": 0.0, "z": 850.0},
        "rotation": {"pitch": -6.0, "yaw": 0.0, "roll": 0.0}
    },
    {
        "id": "C02",
        "name": "C02_Curzon_Front_Left_Oblique",
        "desc": "Front-Left 3/4 perspective framing West Wing, SW Tower, and left Royal Palm",
        "location": {"x": -7200.0, "y": -3500.0, "z": 850.0},
        "rotation": {"pitch": -6.0, "yaw": 25.0, "roll": 0.0}
    },
    {
        "id": "C03",
        "name": "C03_Curzon_Front_Right_Oblique",
        "desc": "Front-Right 3/4 perspective framing East Wing, SE Tower, and Physics Signboard",
        "location": {"x": -7200.0, "y": 3500.0, "z": 850.0},
        "rotation": {"pitch": -6.0, "yaw": -25.0, "roll": 0.0}
    },
    {
        "id": "C07",
        "name": "C07_Curzon_Courtyard_Inner_View",
        "desc": "Interior Veranda Walkway Corridor showing colonial double doors, arched glass fanlights & windows",
        "location": {"x": -2460.0, "y": -1400.0, "z": 180.0},
        "rotation": {"pitch": -2.0, "yaw": -90.0, "roll": 0.0}
    },
    {
        "id": "C08",
        "name": "C08_Curzon_Main_Entrance_Closeup",
        "desc": "Grand Iwan entrance portico, 6-step staircase, recessed double wooden doors & brass handles",
        "location": {"x": -3500.0, "y": 0.0, "z": 220.0},
        "rotation": {"pitch": 2.0, "yaw": 0.0, "roll": 0.0}
    },
    {
        "id": "C09",
        "name": "C09_Curzon_Central_Tower_Closeup",
        "desc": "Central Tower: 4 corner chhatris + 3 intermediate merlons, 6 lancet niches, 2 rosettes, 3-light jali window",
        "location": {"x": -3900.0, "y": 0.0, "z": 1250.0},
        "rotation": {"pitch": 8.0, "yaw": 0.0, "roll": 0.0}
    },
    {
        "id": "C11",
        "name": "C11_Curzon_Veranda_Arches_Closeup",
        "desc": "Veranda Bay Detail: Lower doors & windows, upper cusped arches, jali balustrades & shutters",
        "location": {"x": -3600.0, "y": -2200.0, "z": 320.0},
        "rotation": {"pitch": 0.0, "yaw": 25.0, "roll": 0.0}
    },
    {
        "id": "C12",
        "name": "C12_Curzon_Gameplay_Promenade_Walk",
        "desc": "Human eye level walk approaching from lawn past two Royal Palms and low hedges",
        "location": {"x": -4600.0, "y": 0.0, "z": 180.0},
        "rotation": {"pitch": 0.0, "yaw": 0.0, "roll": 0.0}
    }
]

def run_mcp(toolset, tool, args):
    res = subprocess.check_output([
        "/Users/atiaoishi/Downloads/sparkvision/Scripts/mcp_client.py",
        "call", toolset, tool, json.dumps(args)
    ])
    return json.loads(res) if res.strip() else {}

def preflight_cleanup():
    print("=" * 70)
    print("RUNNING PREFLIGHT CLEANUP (PARKING HELPERS & HIDING DEBUG GIZMOS)...")
    print("=" * 70)
    
    try:
        actors_res = run_mcp("editor_toolset.toolsets.scene.SceneTools", "find_actors", {"name": "", "tag": "", "collision_channels": []})
        actors = actors_res.get("returnValue", actors_res) if isinstance(actors_res, dict) else []
        
        park_keywords = ['DirectionalLight', 'SkyLight', 'PostProcessVolume', 'VolumetricCloud', 'SkyAtmosphere', 'ChaosDebugDrawActor']
        for a in actors:
            ref = a.get("refPath", "")
            if any(k in ref for k in park_keywords):
                xform = {
                    "location": {"x": -150000.0, "y": -150000.0, "z": 50000.0},
                    "rotation": {"pitch": -50.0, "yaw": -30.0, "roll": 0.0} if "DirectionalLight" in ref else {"pitch": 0.0, "yaw": 0.0, "roll": 0.0},
                    "scale": {"x": 1.0, "y": 1.0, "z": 1.0}
                }
                try:
                    run_mcp("editor_toolset.toolsets.actor.ActorTools", "set_actor_transform", {
                        "actor": {"refPath": ref}, "xform": xform, "worldspace": True
                    })
                except Exception:
                    pass
        
        # Deselect actors
        run_mcp("EditorToolset.EditorAppToolset", "SelectActors", {"actors": []})
        print("Preflight cleanup completed successfully.")
    except Exception as e:
        print(f"Warning during preflight: {e}")

def capture_viewpoints():
    print("\n" + "=" * 70)
    print("CAPTURING V3 CURZON HALL VERIFICATION VIEWPOINTS...")
    print("=" * 70)

    for cam in CURZON_CAMERAS_V3:
        cid = cam["id"]
        cname = cam["name"]
        print(f"\nCapturing {cid}: {cname}...")
        
        # Deselect any actors
        run_mcp("EditorToolset.EditorAppToolset", "SelectActors", {"actors": []})
        
        cap_args = {
            "captureTransform": {
                "location": cam["location"],
                "rotation": cam["rotation"],
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
            print(f"  [ERROR] Viewport capture failed for {cid}")
            continue
            
        raw = base64.b64decode(img_b64)
        filename = f"{cname}.png"
        
        targets = [
            os.path.join(CURZON_RUNTIME_DIR, filename),
            os.path.join(DOC_SCREENSHOTS_DIR, filename),
            os.path.join(BRAIN_DIR, filename)
        ]
        
        for t in targets:
            os.makedirs(os.path.dirname(t), exist_ok=True)
            with open(t, "wb") as f:
                f.write(raw)
        print(f"  [PASS] Saved: {filename} ({len(raw):,} bytes)")

if __name__ == "__main__":
    preflight_cleanup()
    capture_viewpoints()
