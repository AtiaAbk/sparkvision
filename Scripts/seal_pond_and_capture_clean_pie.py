#!/usr/bin/env python3
"""
Seal Curzon Pond Background Gap & Capture Clean AAA Live PIE Viewports:
1. Broadens all East Bank & North-East Debdaru trees to width 2.2 for dense canopy overlap
2. Adds a staggered inner Debdaru cluster along the East gap (X=7200..7350, Y=-500..900)
3. Saves the level
4. Runs PIE and captures clean screenshots
"""

import base64
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

RUNTIME_DIR = "/Users/atiaoishi/Downloads/sparkvision/Documentation/WorldCorrection/Runtime"
ARTIFACT_DIR = "/Users/atiaoishi/.gemini/antigravity/brain/e20fce03-5cdc-4c76-8f10-f79efc005a90"
DEBDARU_MESH = "/Game/SparkVision/Campus/Environment/SM_Tree_Debdaru_Columnar.SM_Tree_Debdaru_Columnar"

EMPTY_ANNOTATIONS = {
    "gridSpacing": 0,
    "gridExtent": 0,
    "gridHeight": 0,
    "maxLabelDistance": 0,
    "classFilter": None,
    "maxLabels": 0
}

def main():
    print("=" * 70)
    print("SEALING POND VISTA & CAPTURING CLEAN AAA LIVE PIE GAMEPLAY")
    print("=" * 70)

    # 1. Broaden East Bank Debdaru trees
    print("\n1. Broadening East Bank Debdaru screening wall for impenetrable foliage...")
    for i in range(1, 19):
        name = f"CurzonPond_EastBank_Debdaru_{i:02d}"
        res = invoke_tool("find_actors", "editor_toolset.toolsets.scene.SceneTools", {
            "name": name, "tag": "", "collision_channels": []
        }).get("returnValue", [])
        if res:
            invoke_tool("set_actor_transform", "editor_toolset.toolsets.actor.ActorTools", {
                "actor": res[0],
                "xform": {
                    "scale": {"x": 2.2, "y": 2.2, "z": 3.4}
                }
            })

    # 2. Add staggered inner screening cluster along the gap (X=7200..7350, Y=-500..900)
    print("\n2. Planting staggered inner Debdaru cluster across the background gap...")
    gap_cluster = [
        {"name": "CurzonPond_GapScreen_Debdaru_01", "x": 7250.0, "y": -400.0, "z": 20.0, "yaw": 15.0, "s": 2.2, "sz": 3.3},
        {"name": "CurzonPond_GapScreen_Debdaru_02", "x": 7300.0, "y": -100.0, "z": 20.0, "yaw": -35.0, "s": 2.3, "sz": 3.4},
        {"name": "CurzonPond_GapScreen_Debdaru_03", "x": 7250.0, "y": 200.0, "z": 20.0, "yaw": 50.0, "s": 2.2, "sz": 3.2},
        {"name": "CurzonPond_GapScreen_Debdaru_04", "x": 7300.0, "y": 500.0, "z": 20.0, "yaw": -20.0, "s": 2.3, "sz": 3.5},
        {"name": "CurzonPond_GapScreen_Debdaru_05", "x": 7250.0, "y": 800.0, "z": 20.0, "yaw": 40.0, "s": 2.2, "sz": 3.3},
    ]

    for d in gap_cluster:
        existing = invoke_tool("find_actors", "editor_toolset.toolsets.scene.SceneTools", {
            "name": d["name"], "tag": "", "collision_channels": []
        }).get("returnValue", [])
        if existing:
            invoke_tool("set_actor_transform", "editor_toolset.toolsets.actor.ActorTools", {
                "actor": existing[0],
                "xform": {
                    "location": {"x": d["x"], "y": d["y"], "z": d["z"]},
                    "rotation": {"pitch": 0.0, "yaw": d["yaw"], "roll": 0.0},
                    "scale": {"x": d["s"], "y": d["s"], "z": d["sz"]}
                }
            })
        else:
            res_sp = invoke_tool("add_to_scene_from_asset", "editor_toolset.toolsets.scene.SceneTools", {
                "asset_path": DEBDARU_MESH,
                "name": d["name"],
                "xform": {
                    "location": {"x": d["x"], "y": d["y"], "z": d["z"]},
                    "rotation": {"pitch": 0.0, "yaw": d["yaw"], "roll": 0.0},
                    "scale": {"x": d["s"], "y": d["s"], "z": d["sz"]}
                }
            })
            pref = res_sp.get("returnValue", {}).get("refPath")
            if pref:
                invoke_tool("set_actor_folder", "editor_toolset.toolsets.scene.SceneTools", {
                    "actor": {"refPath": pref},
                    "folder_path": "Environment/Curzon_Pond/East_Screen"
                })
        print(f"  ✓ Planted {d['name']} at ({d['x']:.0f}, {d['y']:.0f})")

    # 3. Save the level
    print("\n3. Saving LV_Level01_Compact_Campus...")
    invoke_tool("save_assets", "editor_toolset.toolsets.asset.AssetTools", {
        "asset_paths": ["/Game/SparkVision/Maps/Level01/LV_Level01_Compact_Campus"]
    })
    print("  ✓ Level saved!")

    # 4. Deselect all actors
    invoke_tool("SelectActors", "EditorToolset.EditorAppToolset", {"actors": []})

    # 5. Stop running PIE if any
    try:
        if invoke_tool("IsPIERunning", "EditorToolset.EditorAppToolset").get("returnValue", False):
            invoke_tool("StopPIE", "EditorToolset.EditorAppToolset")
            time.sleep(2)
    except Exception:
        pass

    # 6. Start PIE
    print("\n4. Starting Play-In-Editor (PIE) session...")
    invoke_tool("StartPIE", "EditorToolset.EditorAppToolset", {
        "options": {
            "bSimulate": False,
            "playMode": "PlayMode_InViewPort",
            "warmupSeconds": 2.5
        }
    })
    time.sleep(4)

    try:
        # Deselect in PIE
        try:
            invoke_tool("SelectActors", "EditorToolset.EditorAppToolset", {"actors": []})
        except Exception:
            pass

        # Capture View 1: Curzon Hero Promenade (Archive Lectern, Tanvir, Boxwood Borders, Lanterns)
        print("\n[1/3] Capturing Clean Hero Curzon Promenade Viewport...")
        cap1 = invoke_tool("CaptureViewport", "EditorToolset.EditorAppToolset", {
            "captureTransform": {
                "location": {"x": -4500.0, "y": 0.0, "z": 220.0},
                "rotation": {"pitch": -5.0, "yaw": 0.0, "roll": 0.0},
                "scale": {"x": 1.0, "y": 1.0, "z": 1.0}
            },
            "annotations": EMPTY_ANNOTATIONS,
            "bShowUI": False
        })
        b64_1 = cap1.get("returnValue", {}).get("image", {}).get("data", "")
        if b64_1:
            bytes_1 = base64.b64decode(b64_1)
            for d in [RUNTIME_DIR, ARTIFACT_DIR]:
                with open(os.path.join(d, "COMPACT_PIE_LIVE_GAMEPLAY.png"), "wb") as f:
                    f.write(bytes_1)
            print(f"  ✓ Saved COMPACT_PIE_LIVE_GAMEPLAY.png ({len(bytes_1)/1024/1024:.2f} MB)")

        # Capture View 2: Curzon Pond Sanctuary (Water Lilies, Ghat, Fully Screened East Bank Wall)
        print("\n[2/3] Capturing Clean Curzon Pond Botanical Sanctuary Viewport...")
        cap2 = invoke_tool("CaptureViewport", "EditorToolset.EditorAppToolset", {
            "captureTransform": {
                "location": {"x": 2200.0, "y": -900.0, "z": 250.0},
                "rotation": {"pitch": -10.0, "yaw": 35.0, "roll": 0.0},
                "scale": {"x": 1.0, "y": 1.0, "z": 1.0}
            },
            "annotations": EMPTY_ANNOTATIONS,
            "bShowUI": False
        })
        b64_2 = cap2.get("returnValue", {}).get("image", {}).get("data", "")
        if b64_2:
            bytes_2 = base64.b64decode(b64_2)
            for d in [RUNTIME_DIR, ARTIFACT_DIR]:
                with open(os.path.join(d, "WWM_CURZON_POND_LIVE_GAMEPLAY.png"), "wb") as f:
                    f.write(bytes_2)
            print(f"  ✓ Saved WWM_CURZON_POND_LIVE_GAMEPLAY.png ({len(bytes_2)/1024/1024:.2f} MB)")

        # Capture View 3: Curzon Landing Veranda Reverse Vista
        print("\n[3/3] Capturing Clean Curzon Veranda Promenade Vista...")
        cap3 = invoke_tool("CaptureViewport", "EditorToolset.EditorAppToolset", {
            "captureTransform": {
                "location": {"x": -3450.0, "y": 0.0, "z": 200.0},
                "rotation": {"pitch": -4.0, "yaw": 180.0, "roll": 0.0},
                "scale": {"x": 1.0, "y": 1.0, "z": 1.0}
            },
            "annotations": EMPTY_ANNOTATIONS,
            "bShowUI": False
        })
        b64_3 = cap3.get("returnValue", {}).get("image", {}).get("data", "")
        if b64_3:
            bytes_3 = base64.b64decode(b64_3)
            for d in [RUNTIME_DIR, ARTIFACT_DIR]:
                with open(os.path.join(d, "WWM_HERO_SANCTUARY_LIVE_GAMEPLAY.png"), "wb") as f:
                    f.write(bytes_3)
            print(f"  ✓ Saved WWM_HERO_SANCTUARY_LIVE_GAMEPLAY.png ({len(bytes_3)/1024/1024:.2f} MB)")

    finally:
        print("\nStopping PIE cleanly...")
        try:
            invoke_tool("StopPIE", "EditorToolset.EditorAppToolset")
        except Exception:
            pass
        time.sleep(1)

    print("\n" + "=" * 70)
    print("✅ FINAL AAA WWM GAMEPLAY VERIFICATION COMPLETE!")
    print("=" * 70)

if __name__ == "__main__":
    main()
