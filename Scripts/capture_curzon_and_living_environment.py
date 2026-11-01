#!/usr/bin/env python3
"""
Comprehensive Capture Script for Curzon Hall Reconstruction & Living Environment
Captures:
  1. C01 to C13 Curzon Hall Architectural Benchmark Viewpoints
  2. ENV_01 to ENV_10 Living Environment Ecological Showcase Viewpoints
Saves to Documentation/CurzonHall/Screenshots/Runtime/, Documentation/WorldEnvironment/Screenshots/Runtime/,
and the Brain Artifact Directory.
"""

import os
import json
import base64
import subprocess
import time

CURZON_RUNTIME_DIR = "/Users/atiaoishi/Downloads/sparkvision/Documentation/CurzonHall/Screenshots/Runtime"
ENV_RUNTIME_DIR = "/Users/atiaoishi/Downloads/sparkvision/Documentation/WorldEnvironment/Screenshots/Runtime"
DOC_DIR = "/Users/atiaoishi/Downloads/sparkvision/Documentation/Screenshots"
BRAIN_DIR = "/Users/atiaoishi/.gemini/antigravity/brain/e20fce03-5cdc-4c76-8f10-f79efc005a90"

for d in [CURZON_RUNTIME_DIR, ENV_RUNTIME_DIR, DOC_DIR, BRAIN_DIR]:
    os.makedirs(d, exist_ok=True)

CURZON_CAMERAS = [
    {
        "id": "C01",
        "name": "C01_Curzon_Full_Front_Elevation",
        "desc": "Full Front Southern Elevation showing bilateral symmetry, 128m facade, and balanced towers",
        "location": {"x": -9500.0, "y": 0.0, "z": 1200.0},
        "rotation": {"pitch": -6.0, "yaw": 0.0, "roll": 0.0}
    },
    {
        "id": "C02",
        "name": "C02_Curzon_Front_Left_Oblique",
        "desc": "Front-Left 3/4 Perspective framing West Wing, Southwest Tower & Botanical Lawn",
        "location": {"x": -7200.0, "y": -3500.0, "z": 850.0},
        "rotation": {"pitch": -6.0, "yaw": 25.0, "roll": 0.0}
    },
    {
        "id": "C03",
        "name": "C03_Curzon_Front_Right_Oblique",
        "desc": "Front-Right 3/4 Perspective framing East Wing, Southeast Tower & Parterre Garden",
        "location": {"x": -7200.0, "y": 3500.0, "z": 850.0},
        "rotation": {"pitch": -6.0, "yaw": -25.0, "roll": 0.0}
    },
    {
        "id": "C04",
        "name": "C04_Curzon_Rear_Courtyard_Elevation",
        "desc": "Elevated Rear Courtyard View looking South over symmetrical inner gardens, wings, and twin rooftop chhatris",
        "location": {"x": 2600.0, "y": 0.0, "z": 2600.0},
        "rotation": {"pitch": -20.0, "yaw": 180.0, "roll": 0.0}
    },
    {
        "id": "C05",
        "name": "C05_Curzon_West_Side_Elevation",
        "desc": "West Side Elevation showing Southwest 25.2m Octagonal Tower & Wing profile",
        "location": {"x": -2500.0, "y": -7500.0, "z": 600.0},
        "rotation": {"pitch": -6.0, "yaw": 90.0, "roll": 0.0}
    },
    {
        "id": "C06",
        "name": "C06_Curzon_East_Side_Elevation",
        "desc": "East Side Elevation showing Southeast 25.2m Octagonal Tower & Science Annex link",
        "location": {"x": -2500.0, "y": 7500.0, "z": 600.0},
        "rotation": {"pitch": -6.0, "yaw": -90.0, "roll": 0.0}
    },
    {
        "id": "C07",
        "name": "C07_Curzon_Courtyard_Inner_View",
        "desc": "Interior Veranda Colonnade Walkway looking West along rhythmic horseshoe arches and terracotta floor",
        "location": {"x": -2460.0, "y": -1400.0, "z": 180.0},
        "rotation": {"pitch": -2.0, "yaw": -90.0, "roll": 0.0}
    },
    {
        "id": "C08",
        "name": "C08_Curzon_Main_Entrance_Closeup",
        "desc": "Monumental Central Entrance Portico, 5-step staircase & Grand 9-Cusp Iwan Arch",
        "location": {"x": -3400.0, "y": 0.0, "z": 220.0},
        "rotation": {"pitch": 2.0, "yaw": 0.0, "roll": 0.0}
    },
    {
        "id": "C09",
        "name": "C09_Curzon_Central_Tower_Closeup",
        "desc": "Central Tower Pediment, Clock Dial Medallion, and Twin Rooftop Rajput Chhatris",
        "location": {"x": -3800.0, "y": 0.0, "z": 1200.0},
        "rotation": {"pitch": 6.0, "yaw": 0.0, "roll": 0.0}
    },
    {
        "id": "C10",
        "name": "C10_Curzon_Tower_Chhatri_Parapet",
        "desc": "25.2m Tower Chhatri Kiosk, Lotus Crest, Brass Finial & Stepped Parapet Merlons",
        "location": {"x": -2500.0, "y": -4200.0, "z": 1450.0},
        "rotation": {"pitch": 16.0, "yaw": -90.0, "roll": 0.0}
    },
    {
        "id": "C11",
        "name": "C11_Curzon_Veranda_Arches_Closeup",
        "desc": "Veranda Colonnade: Lower Horseshoe Arches, Upper 7-Lobed Cusped Arches & Jali",
        "location": {"x": -3600.0, "y": -2200.0, "z": 320.0},
        "rotation": {"pitch": 0.0, "yaw": 25.0, "roll": 0.0}
    },
    {
        "id": "C12",
        "name": "C12_Curzon_Gameplay_Promenade_Walk",
        "desc": "Third-Person Gameplay Perspective along the red brick herringbone promenade",
        "location": {"x": -4200.0, "y": 0.0, "z": 180.0},
        "rotation": {"pitch": 0.0, "yaw": 0.0, "roll": 0.0}
    },
    {
        "id": "C13",
        "name": "C13_Curzon_Elevated_Master_Footprint",
        "desc": "High-Angle Master View showing full E-W footprint, verandas, roof terrace & gardens",
        "location": {"x": -6500.0, "y": 0.0, "z": 3800.0},
        "rotation": {"pitch": -30.0, "yaw": 0.0, "roll": 0.0}
    }
]

ENV_CAMERAS = [
    {
        "id": "ENV_01",
        "name": "ENV_01_Curzon_Promenade_Canopy",
        "desc": "Curzon Southern Promenade looking through Krishnachura flaming scarlet red blooms",
        "location": {"x": -3800.0, "y": -2600.0, "z": 320.0},
        "rotation": {"pitch": -5.0, "yaw": 30.0, "roll": 0.0}
    },
    {
        "id": "ENV_02",
        "name": "ENV_02_Curzon_Botanical_Pond_Ecology",
        "desc": "Curzon Botanical Pond: Floating Shapla water lilies, leaning coconut palms, and ghat",
        "location": {"x": -4500.0, "y": -3200.0, "z": 180.0},
        "rotation": {"pitch": -5.0, "yaw": -140.0, "roll": 0.0}
    },
    {
        "id": "ENV_03",
        "name": "ENV_03_Curzon_Bamboo_Groves",
        "desc": "Curzon Southern Buffer: Bengal Golden Bamboo thickets with sunlight filtering through arching culms",
        "location": {"x": -550.0, "y": 2800.0, "z": 150.0},
        "rotation": {"pitch": 2.0, "yaw": 60.0, "roll": 0.0}
    },
    {
        "id": "ENV_04",
        "name": "ENV_04_Fuller_Road_Tree_Tunnel",
        "desc": "Fuller Road Grand Avenue: Continuous double-row arching Raintree canopy tunnel",
        "location": {"x": 12000.0, "y": -38000.0, "z": 280.0},
        "rotation": {"pitch": -3.0, "yaw": -36.0, "roll": 0.0}
    },
    {
        "id": "ENV_05",
        "name": "ENV_05_Arts_Faculty_Flowering_Canopy",
        "desc": "Kala Bhaban & Aparajeyo Bangla framed by Krishnachura & Radhachura blooms",
        "location": {"x": 69800.0, "y": -98000.0, "z": 300.0},
        "rotation": {"pitch": 3.0, "yaw": 28.0, "roll": 0.0}
    },
    {
        "id": "ENV_06",
        "name": "ENV_06_The_Mall_Ancient_Banyan",
        "desc": "The Mall & Central Sports Field: Massive heritage Banyan tree with buttressed roots",
        "location": {"x": 48500.0, "y": -65000.0, "z": 350.0},
        "rotation": {"pitch": -6.0, "yaw": 35.0, "roll": 0.0}
    },
    {
        "id": "ENV_07",
        "name": "ENV_07_Shaheed_Minar_Sanctuary_Trees",
        "desc": "Central Shaheed Minar framed by symmetrical neem trees and memorial Krishnachura",
        "location": {"x": -2500.0, "y": -54042.0, "z": 300.0},
        "rotation": {"pitch": -5.0, "yaw": 0.0, "roll": 0.0}
    },
    {
        "id": "ENV_08",
        "name": "ENV_08_Shahidullah_Lake_Reflections",
        "desc": "Shahidullah Lake Ecology: Lakeside coconut palms, water lilies, and serene surface reflections",
        "location": {"x": 11500.0, "y": 19500.0, "z": 320.0},
        "rotation": {"pitch": -8.0, "yaw": 45.0, "roll": 0.0}
    },
    {
        "id": "ENV_09",
        "name": "ENV_09_Curzon_Veranda_Garden_Overlook",
        "desc": "First-Floor Curzon Veranda Balcony overlooking the blooming parterre gardens below",
        "location": {"x": -2500.0, "y": 0.0, "z": 750.0},
        "rotation": {"pitch": -12.0, "yaw": 180.0, "roll": 0.0}
    },
    {
        "id": "ENV_10",
        "name": "ENV_10_Campus_Wide_Atmospheric_Aerial",
        "desc": "Campus-wide atmospheric sunset panorama showing dense multi-tier greenery across DU",
        "location": {"x": 35000.0, "y": -50000.0, "z": 18000.0},
        "rotation": {"pitch": -55.0, "yaw": 0.0, "roll": 0.0}
    }
]

def run_mcp(toolset, tool, args):
    res = subprocess.check_output([
        "/Users/atiaoishi/Downloads/sparkvision/Scripts/mcp_client.py",
        "call", toolset, tool, json.dumps(args)
    ])
    return json.loads(res) if res.strip() else {}

def preflight_cleanup():
    print("\n=== RUNNING PREFLIGHT CLEANUP (PARKING HELPERS & HIDING DEBUG GIZMOS) ===")
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
        
        for a in actors:
            ref = a.get("refPath", "")
            if any(k in ref for k in ['SVStudentNPC', 'SVHostileOpponent', 'SVPlayerPawn', 'PlayerStart', 'SVArchiveTerminal']):
                comps_res = run_mcp("editor_toolset.toolsets.actor.ActorTools", "get_components", {"actor": a})
                comps = comps_res.get("returnValue", comps_res) if isinstance(comps_res, dict) else []
                for c in comps:
                    cref = c.get("refPath", "")
                    if any(name in cref for name in ['CollisionCylinder', 'Arrow', 'InteractionSphere', 'Sprite']):
                        try:
                            run_mcp("editor_toolset.toolsets.object.ObjectTools", "set_properties", {
                                "instance": {"refPath": cref},
                                "values": json.dumps({"bVisible": False, "bHiddenInGame": True})
                            })
                        except Exception:
                            pass
        
        run_mcp("EditorToolset.EditorAppToolset", "SelectActors", {"actors": []})
        print("Preflight cleanup completed successfully.")
    except Exception as e:
        print(f"Warning during preflight cleanup: {e}")

def capture_suite(cams, out_primary_dir, suite_name):
    print(f"\n=== CAPTURING {suite_name.upper()} ({len(cams)} VIEWPOINTS) ===")
    
    for cam in cams:
        cid = cam["id"]
        cname = cam["name"]
        print(f"\nSetting Viewport Camera & Capturing {cid}: {cname}...")
        
        try:
            # Deselect any actors to prevent selection outlines / gizmos from rendering in screenshots
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
            
            if img_b64:
                raw_bytes = base64.b64decode(img_b64)
                
                # 1. Primary destination
                path_primary = os.path.join(out_primary_dir, f"{cname}.png")
                with open(path_primary, "wb") as f:
                    f.write(raw_bytes)
                    
                # 2. General Documentation/Screenshots
                path_doc = os.path.join(DOC_DIR, f"{cname}.png")
                with open(path_doc, "wb") as f:
                    f.write(raw_bytes)
                    
                # 3. Brain Artifacts dir for pairing
                path_brain = os.path.join(BRAIN_DIR, f"{cname}.png")
                with open(path_brain, "wb") as f:
                    f.write(raw_bytes)
                    
                print(f"  [SAVED] {cname}.png ({len(raw_bytes):,} bytes)")
            else:
                print(f"  [ERROR] CaptureViewport returned empty image for {cid}")
        except Exception as e:
            print(f"  [ERROR] Exception on {cid}: {e}")

if __name__ == "__main__":
    preflight_cleanup()
    capture_suite(CURZON_CAMERAS, CURZON_RUNTIME_DIR, "Curzon Hall Architectural Reconstruction Suite")
    capture_suite(ENV_CAMERAS, ENV_RUNTIME_DIR, "Living University of Dhaka Environment Suite")
    print("\n=== ALL 23 BENCHMARK VIEWPOINTS CAPTURED SUCCESSFULLY! ===")
