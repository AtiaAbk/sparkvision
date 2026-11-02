#!/usr/bin/env python3
"""
Upgrade Curzon Pond Flora & Atmosphere to Where Winds Meet AAA Standard:
- Swaps CurzonPond_Jarul_* to SM_Tree_Krishnachura_WWM with rich foliage
- Swaps CurzonPond_WaterLily_* to SM_Pond_WaterLily_WWM with blooming lotuses
- Adds Bamboo Groves along pond periphery
- Saves level
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

TREE_MESH = "/Game/SparkVision/Campus/Environment/SM_Tree_Krishnachura_WWM.SM_Tree_Krishnachura_WWM"
LILY_MESH = "/Game/SparkVision/Campus/Environment/SM_Pond_WaterLily_WWM.SM_Pond_WaterLily_WWM"
BAMBOO_MESH = "/Game/SparkVision/Campus/Environment/SM_Cluster_Bamboo_Grove.SM_Cluster_Bamboo_Grove"

def main():
    print("=" * 60)
    print("UPGRADING CURZON POND FLORA TO WWM AESTHETICS")
    print("=" * 60)

    # 1. Update Riparian Trees
    trees = invoke_tool("get_actors_in_folder", "editor_toolset.toolsets.scene.SceneTools", {
        "folder_path": "Environment/Curzon_Pond/Riparian_Trees"
    }).get("returnValue", [])

    print(f"Processing {len(trees)} pond trees...")
    for t in trees:
        lbl = invoke_tool("get_label", "editor_toolset.toolsets.actor.ActorTools", {
            "actor": {"refPath": t["refPath"]}
        }).get("returnValue", "")

        comps = invoke_tool("get_components", "editor_toolset.toolsets.actor.ActorTools", {
            "actor": {"refPath": t["refPath"]}
        }).get("returnValue", [])

        if not comps:
            continue

        comp_ref = comps[0]["refPath"]
        if "Jarul" in lbl:
            # Swap mesh to WWM Krishnachura Bloom
            invoke_tool("set_properties", "editor_toolset.toolsets.object.ObjectTools", {
                "instance": {"refPath": comp_ref},
                "values": json.dumps({"StaticMesh": {"refPath": TREE_MESH}})
            })
            # Give natural organic scale via RootComponent RelativeScale3D
            invoke_tool("set_properties", "editor_toolset.toolsets.object.ObjectTools", {
                "instance": {"refPath": comp_ref},
                "values": json.dumps({"RelativeScale3D": {"x": 1.6, "y": 1.6, "z": 1.5}})
            })
            print(f"  ✓ Upgraded {lbl} to Krishnachura WWM")

    # 2. Update Water Lilies
    lilies = invoke_tool("get_actors_in_folder", "editor_toolset.toolsets.scene.SceneTools", {
        "folder_path": "Environment/Curzon_Pond/Aquatic_Flora"
    }).get("returnValue", [])

    print(f"\nProcessing {len(lilies)} aquatic lilies...")
    for l in lilies:
        lbl = invoke_tool("get_label", "editor_toolset.toolsets.actor.ActorTools", {
            "actor": {"refPath": l["refPath"]}
        }).get("returnValue", "")

        comps = invoke_tool("get_components", "editor_toolset.toolsets.actor.ActorTools", {
            "actor": {"refPath": l["refPath"]}
        }).get("returnValue", [])

        if not comps:
            continue

        comp_ref = comps[0]["refPath"]
        invoke_tool("set_properties", "editor_toolset.toolsets.object.ObjectTools", {
            "instance": {"refPath": comp_ref},
            "values": json.dumps({"StaticMesh": {"refPath": LILY_MESH}, "RelativeScale3D": {"x": 1.4, "y": 1.4, "z": 1.4}})
        })
        print(f"  ✓ Upgraded {lbl} to WWM Blooming Lotus")

    # 3. Add Bamboo Groves along Pond Perimeter (Wuxia aesthetic)
    print("\nAdding Bamboo Groves around Curzon Pond periphery...")
    bamboo_locs = [
        (2600, -1400, 20),
        (3400, -1500, 20),
        (4200, -1550, 20),
        (5000, -1500, 20),
        (5800, -1400, 20),
        (6600, -1300, 20),
        # East bank
        (7200, -600, 20),
        (7200, 600, 20),
    ]

    for i, (bx, by, bz) in enumerate(bamboo_locs):
        bname = f"CurzonPond_WWM_Bamboo_{i+1:02d}"
        try:
            res = invoke_tool("add_to_scene_from_asset", "editor_toolset.toolsets.scene.SceneTools", {
                "asset_path": BAMBOO_MESH,
                "name": bname,
                "xform": {
                    "location": {"x": bx, "y": by, "z": bz},
                    "rotation": {"pitch": 0.0, "yaw": float(i * 45 % 360), "roll": 0.0},
                    "scale": {"x": 1.5, "y": 1.5, "z": 1.6}
                }
            })
            ref = res.get("returnValue", {}).get("refPath", "")
            if ref:
                invoke_tool("set_actor_folder", "editor_toolset.toolsets.scene.SceneTools", {
                    "actor": {"refPath": ref},
                    "folder_path": "Environment/Curzon_Pond/Bamboo_Sanctuary"
                })
                print(f"  ✓ Placed {bname} at ({bx}, {by}, {bz})")
        except Exception as e:
            print(f"  Notice placing bamboo: {e}")

    # Save level
    try:
        invoke_tool("save_assets", "editor_toolset.toolsets.asset.AssetTools", {
            "asset_paths": ["/Game/SparkVision/Maps/Level01/LV_Level01_Compact_Campus"]
        })
        print("\n✅ Saved level changes successfully!")
    except Exception as e:
        print(f"Notice saving level: {e}")

if __name__ == "__main__":
    main()
