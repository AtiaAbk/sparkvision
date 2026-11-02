#!/usr/bin/env python3
"""
Finalize Where Winds Meet x Dhaka University Curzon Sanctuary:
1. Fix & Expand East Bank & North-East Debdaru Columnar screening grove (25-35m tall) to eliminate background exposure across Curzon Pond
2. Place neat low trimmed boxwood hedges along the wooden promenade borders (X = -4500 to -3500, Y = +/- 550)
3. Ensure ArchiveTerminal_archive_01 and NPC Tanvir are perfectly situated on the Curzon landing plinth
4. Save the level
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

DEBDARU_MESH = "/Game/SparkVision/Campus/Environment/SM_Tree_Debdaru_Columnar.SM_Tree_Debdaru_Columnar"
HEDGE_MESH = "/Game/SparkVision/Campus/CurzonModular/SM_Curzon_Hedge_Low.SM_Curzon_Hedge_Low"

def main():
    print("=" * 70)
    print("FINALIZING WWM CURZON HALL & POND BOTANICAL SANCTUARY")
    print("=" * 70)

    # 1. Update existing East Bank Debdaru 01..10 scales
    print("\n1. Calibrating East Bank Debdaru trees (01-10) to full stature (Z=3.2)...")
    for i in range(1, 11):
        name = f"CurzonPond_EastBank_Debdaru_{i:02d}"
        res = invoke_tool("find_actors", "editor_toolset.toolsets.scene.SceneTools", {
            "name": name, "tag": "", "collision_channels": []
        }).get("returnValue", [])
        if res:
            invoke_tool("set_actor_transform", "editor_toolset.toolsets.actor.ActorTools", {
                "actor": res[0],
                "xform": {
                    "scale": {"x": 1.5, "y": 1.5, "z": 3.2}
                }
            })
            print(f"  ✓ Scaled {name} to (1.5, 1.5, 3.2)")

    # 2. Add Debdaru trees 11..18 along East Bank (Y=1500..3400)
    print("\n2. Planting continuous East Bank screening wall (11-18) to connect with North Bank...")
    east_extension = [
        {"name": "CurzonPond_EastBank_Debdaru_11", "x": 7500.0, "y": 1600.0, "z": 20.0, "yaw": 25.0, "sz": 3.2},
        {"name": "CurzonPond_EastBank_Debdaru_12", "x": 7550.0, "y": 1900.0, "z": 20.0, "yaw": -40.0, "sz": 3.0},
        {"name": "CurzonPond_EastBank_Debdaru_13", "x": 7500.0, "y": 2200.0, "z": 20.0, "yaw": 60.0, "sz": 3.4},
        {"name": "CurzonPond_EastBank_Debdaru_14", "x": 7550.0, "y": 2500.0, "z": 20.0, "yaw": -15.0, "sz": 3.1},
        {"name": "CurzonPond_EastBank_Debdaru_15", "x": 7500.0, "y": 2800.0, "z": 20.0, "yaw": 45.0, "sz": 3.3},
        {"name": "CurzonPond_EastBank_Debdaru_16", "x": 7550.0, "y": 3050.0, "z": 20.0, "yaw": -60.0, "sz": 3.2},
        {"name": "CurzonPond_EastBank_Debdaru_17", "x": 7400.0, "y": 3250.0, "z": 20.0, "yaw": 30.0, "sz": 3.4},
        {"name": "CurzonPond_EastBank_Debdaru_18", "x": 7250.0, "y": 3350.0, "z": 20.0, "yaw": -10.0, "sz": 3.1},
    ]

    for d in east_extension:
        # Check if already exists
        existing = invoke_tool("find_actors", "editor_toolset.toolsets.scene.SceneTools", {
            "name": d["name"], "tag": "", "collision_channels": []
        }).get("returnValue", [])
        if existing:
            invoke_tool("set_actor_transform", "editor_toolset.toolsets.actor.ActorTools", {
                "actor": existing[0],
                "xform": {
                    "location": {"x": d["x"], "y": d["y"], "z": d["z"]},
                    "rotation": {"pitch": 0.0, "yaw": d["yaw"], "roll": 0.0},
                    "scale": {"x": 1.5, "y": 1.5, "z": d["sz"]}
                }
            })
            print(f"  ✓ Updated {d['name']}")
        else:
            res_sp = invoke_tool("add_to_scene_from_asset", "editor_toolset.toolsets.scene.SceneTools", {
                "asset_path": DEBDARU_MESH,
                "name": d["name"],
                "xform": {
                    "location": {"x": d["x"], "y": d["y"], "z": d["z"]},
                    "rotation": {"pitch": 0.0, "yaw": d["yaw"], "roll": 0.0},
                    "scale": {"x": 1.5, "y": 1.5, "z": d["sz"]}
                }
            })
            pref = res_sp.get("returnValue", {}).get("refPath")
            if pref:
                invoke_tool("set_actor_folder", "editor_toolset.toolsets.scene.SceneTools", {
                    "actor": {"refPath": pref},
                    "folder_path": "Environment/Curzon_Pond/East_Screen"
                })
                print(f"  ✓ Spawned {d['name']} at ({d['x']:.0f}, {d['y']:.0f})")

    # 3. Add Debdaru trees screening North-East Science Annex (Supporting_CurzonChemistryPhysicsLabs at 6500, 4400)
    print("\n3. Screening North-East Science Annex with dense Debdaru grove...")
    annex_screen = [
        {"name": "CurzonPond_AnnexScreen_Debdaru_01", "x": 6000.0, "y": 4100.0, "z": 20.0, "yaw": 10.0, "sz": 3.3},
        {"name": "CurzonPond_AnnexScreen_Debdaru_02", "x": 6300.0, "y": 4150.0, "z": 20.0, "yaw": 50.0, "sz": 3.5},
        {"name": "CurzonPond_AnnexScreen_Debdaru_03", "x": 6600.0, "y": 4100.0, "z": 20.0, "yaw": -30.0, "sz": 3.4},
        {"name": "CurzonPond_AnnexScreen_Debdaru_04", "x": 6900.0, "y": 4150.0, "z": 20.0, "yaw": 70.0, "sz": 3.5},
        {"name": "CurzonPond_AnnexScreen_Debdaru_05", "x": 6150.0, "y": 4350.0, "z": 20.0, "yaw": -45.0, "sz": 3.6},
        {"name": "CurzonPond_AnnexScreen_Debdaru_06", "x": 6450.0, "y": 4350.0, "z": 20.0, "yaw": 20.0, "sz": 3.6},
        {"name": "CurzonPond_AnnexScreen_Debdaru_07", "x": 6750.0, "y": 4350.0, "z": 20.0, "yaw": -15.0, "sz": 3.6},
    ]

    for d in annex_screen:
        existing = invoke_tool("find_actors", "editor_toolset.toolsets.scene.SceneTools", {
            "name": d["name"], "tag": "", "collision_channels": []
        }).get("returnValue", [])
        if existing:
            invoke_tool("set_actor_transform", "editor_toolset.toolsets.actor.ActorTools", {
                "actor": existing[0],
                "xform": {
                    "location": {"x": d["x"], "y": d["y"], "z": d["z"]},
                    "rotation": {"pitch": 0.0, "yaw": d["yaw"], "roll": 0.0},
                    "scale": {"x": 1.6, "y": 1.6, "z": d["sz"]}
                }
            })
            print(f"  ✓ Updated {d['name']}")
        else:
            res_sp = invoke_tool("add_to_scene_from_asset", "editor_toolset.toolsets.scene.SceneTools", {
                "asset_path": DEBDARU_MESH,
                "name": d["name"],
                "xform": {
                    "location": {"x": d["x"], "y": d["y"], "z": d["z"]},
                    "rotation": {"pitch": 0.0, "yaw": d["yaw"], "roll": 0.0},
                    "scale": {"x": 1.6, "y": 1.6, "z": d["sz"]}
                }
            })
            pref = res_sp.get("returnValue", {}).get("refPath")
            if pref:
                invoke_tool("set_actor_folder", "editor_toolset.toolsets.scene.SceneTools", {
                    "actor": {"refPath": pref},
                    "folder_path": "Environment/Curzon_Pond/East_Screen"
                })
                print(f"  ✓ Spawned {d['name']} at ({d['x']:.0f}, {d['y']:.0f})")

    # 4. Place neat low trimmed boxwood hedges along Promenade edges
    print("\n4. Placing low boxwood border hedges along Curzon Promenade...")
    promenade_hedges = [
        # South edge (Y = -550)
        {"name": "Curzon_Promenade_Hedge_South_01", "x": -4250.0, "y": -550.0, "z": 15.0, "yaw": 90.0},
        {"name": "Curzon_Promenade_Hedge_South_02", "x": -3800.0, "y": -550.0, "z": 15.0, "yaw": 90.0},
        # North edge (Y = +550)
        {"name": "Curzon_Promenade_Hedge_North_01", "x": -4250.0, "y": 550.0, "z": 15.0, "yaw": 90.0},
        {"name": "Curzon_Promenade_Hedge_North_02", "x": -3800.0, "y": 550.0, "z": 15.0, "yaw": 90.0},
    ]

    for h in promenade_hedges:
        existing = invoke_tool("find_actors", "editor_toolset.toolsets.scene.SceneTools", {
            "name": h["name"], "tag": "", "collision_channels": []
        }).get("returnValue", [])
        if existing:
            invoke_tool("set_actor_transform", "editor_toolset.toolsets.actor.ActorTools", {
                "actor": existing[0],
                "xform": {
                    "location": {"x": h["x"], "y": h["y"], "z": h["z"]},
                    "rotation": {"pitch": 0.0, "yaw": h["yaw"], "roll": 0.0},
                    "scale": {"x": 1.0, "y": 1.0, "z": 0.85}
                }
            })
            print(f"  ✓ Updated {h['name']}")
        else:
            res_h = invoke_tool("add_to_scene_from_asset", "editor_toolset.toolsets.scene.SceneTools", {
                "asset_path": HEDGE_MESH,
                "name": h["name"],
                "xform": {
                    "location": {"x": h["x"], "y": h["y"], "z": h["z"]},
                    "rotation": {"pitch": 0.0, "yaw": h["yaw"], "roll": 0.0},
                    "scale": {"x": 1.0, "y": 1.0, "z": 0.85}
                }
            })
            pref = res_h.get("returnValue", {}).get("refPath")
            if pref:
                invoke_tool("set_actor_folder", "editor_toolset.toolsets.scene.SceneTools", {
                    "actor": {"refPath": pref},
                    "folder_path": "Environment/Curzon_Promenade/Hedges"
                })
                print(f"  ✓ Spawned {h['name']} at ({h['x']:.0f}, {h['y']:.0f})")

    # 5. Confirm Archive Terminal and Tanvir
    print("\n5. Confirming Curzon Landing Plinth Hero Placements...")
    # Archive Terminal
    terminals = invoke_tool("find_actors", "editor_toolset.toolsets.scene.SceneTools", {
        "name": "ArchiveTerminal_archive_01", "tag": "", "collision_channels": []
    }).get("returnValue", [])
    if terminals:
        invoke_tool("set_actor_transform", "editor_toolset.toolsets.actor.ActorTools", {
            "actor": terminals[0],
            "xform": {
                "location": {"x": -3450.0, "y": 240.0, "z": 120.0},
                "rotation": {"pitch": 0.0, "yaw": -15.0, "roll": 0.0},
                "scale": {"x": 1.0, "y": 1.0, "z": 1.0}
            },
            "worldspace": True
        })
        print("  ✓ Grounded ArchiveTerminal_archive_01 at (-3450, 240, 120)")

    # NPC Tanvir
    tanvir = invoke_tool("find_actors", "editor_toolset.toolsets.scene.SceneTools", {
        "name": "NPC_Tanvir_Curzon", "tag": "", "collision_channels": []
    }).get("returnValue", [])
    if tanvir:
        invoke_tool("set_actor_transform", "editor_toolset.toolsets.actor.ActorTools", {
            "actor": tanvir[0],
            "xform": {
                "location": {"x": -3450.0, "y": -240.0, "z": 150.0},
                "rotation": {"pitch": 0.0, "yaw": 180.0, "roll": 0.0},
                "scale": {"x": 1.0, "y": 1.0, "z": 1.0}
            },
            "worldspace": True
        })
        print("  ✓ Positioned NPC_Tanvir_Curzon at (-3450, -240, 150)")

    # 6. Save Level
    print("\n6. Saving Level LV_Level01_Compact_Campus...")
    try:
        invoke_tool("save_current_level", "editor_toolset.toolsets.scene.SceneTools", {})
        invoke_tool("save_assets", "editor_toolset.toolsets.asset.AssetTools", {
            "asset_paths": ["/Game/SparkVision/Maps/Level01/LV_Level01_Compact_Campus"]
        })
        print("✅ LV_Level01_Compact_Campus successfully saved!")
    except Exception as e:
        print(f"Notice saving level: {e}")

if __name__ == "__main__":
    main()
