#!/usr/bin/env python3
"""
Refine Final WWM Curzon & Pond Vistas:
1. Ground Archive Terminal: Lower Z by 30cm so the octagonal sandstone plinth rests flush on the landing floor
2. Plant East Bank Debdaru Grove (X=7400..7600, Y=-1400..1400) to screen the background buildings across the pond
3. Save level
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

DEBDARU_MESH = "/Game/SparkVision/Campus/Environment/SM_Tree_Debdaru_Columnar.SM_Tree_Debdaru_Columnar"

def main():
    print("=" * 70)
    print("REFINING WWM VISTAS: TERMINAL GROUNDING & POND SCREENING")
    print("=" * 70)

    # 1. Ground Archive Terminal
    print("\n1. Grounding Archive Terminal on Curzon landing...")
    res = invoke_tool("find_actors", "editor_toolset.toolsets.scene.SceneTools", {
        "name": "ArchiveTerminal_archive_01", "tag": "", "collision_channels": []
    })
    actors = res.get("returnValue", [])
    if actors:
        invoke_tool("set_actor_transform", "editor_toolset.toolsets.actor.ActorTools", {
            "actor": actors[0],
            "xform": {
                "location": {"x": -3450.0, "y": 240.0, "z": 120.0},
                "rotation": {"pitch": 0.0, "yaw": -15.0, "roll": 0.0},
                "scale": {"x": 1.0, "y": 1.0, "z": 1.0}
            },
            "worldspace": True
        })
        print("  ✓ Lowered ArchiveTerminal_archive_01 to Z=120.0 (flush on landing)")

    # 2. Plant East Bank Debdaru Wall (across the pond)
    print("\n2. Planting East Bank Debdaru Screening Grove...")
    east_debdaru = [
        {"x": 7500.0, "y": -1400.0, "z": 20.0, "yaw": 20.0, "sz": 2.2},
        {"x": 7550.0, "y": -1100.0, "z": 20.0, "yaw": -45.0, "sz": 2.5},
        {"x": 7500.0, "y": -800.0, "z": 20.0, "yaw": 60.0, "sz": 2.3},
        {"x": 7600.0, "y": -500.0, "z": 20.0, "yaw": -15.0, "sz": 2.6},
        {"x": 7550.0, "y": -200.0, "z": 20.0, "yaw": 75.0, "sz": 2.4},
        {"x": 7500.0, "y": 100.0, "z": 20.0, "yaw": -30.0, "sz": 2.5},
        {"x": 7600.0, "y": 400.0, "z": 20.0, "yaw": 45.0, "sz": 2.3},
        {"x": 7550.0, "y": 700.0, "z": 20.0, "yaw": -60.0, "sz": 2.6},
        {"x": 7500.0, "y": 1000.0, "z": 20.0, "yaw": 30.0, "sz": 2.4},
        {"x": 7550.0, "y": 1300.0, "z": 20.0, "yaw": -10.0, "sz": 2.2},
    ]

    for idx, d in enumerate(east_debdaru):
        aname = f"CurzonPond_EastBank_Debdaru_{idx+1:02d}"
        try:
            res_sp = invoke_tool("add_to_scene_from_asset", "editor_toolset.toolsets.scene.SceneTools", {
                "asset_path": DEBDARU_MESH,
                "name": aname,
                "xform": {
                    "location": {"x": d["x"], "y": d["y"], "z": d["z"]},
                    "rotation": {"pitch": 0.0, "yaw": d["yaw"], "roll": 0.0},
                    "scale": {"x": 1.3, "y": 1.3, "sz": d["sz"]}
                }
            })
            pref = res_sp.get("returnValue", {}).get("refPath")
            if pref:
                invoke_tool("set_actor_folder", "editor_toolset.toolsets.scene.SceneTools", {
                    "actor": {"refPath": pref},
                    "folder_path": "Environment/Curzon_Pond/East_Screen"
                })
                print(f"  ✓ Spawned {aname} at Y={d['y']:.0f}, height scale={d['sz']:.1f}")
        except Exception as e:
            print(f"  ✗ Error spawning {aname}: {e}")

    # 3. Save level
    print("\n3. Saving level LV_Level01_Compact_Campus...")
    try:
        invoke_tool("save_assets", "editor_toolset.toolsets.asset.AssetTools", {
            "asset_paths": ["/Game/SparkVision/Maps/Level01/LV_Level01_Compact_Campus"]
        })
        print("✅ Saved LV_Level01_Compact_Campus successfully!")
    except Exception as e:
        print(f"Notice saving: {e}")

if __name__ == "__main__":
    main()
