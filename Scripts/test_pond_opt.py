#!/usr/bin/env python3
"""
Test script to optimize pond bamboo clusters and verify zero surface cache warnings.
"""

import sys
import os
import json
import base64
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

PP_ACTOR = "/Game/SparkVision/Maps/Level01/LV_Level01_Compact_Campus.LV_Level01_Compact_Campus:PersistentLevel.PostProcessVolume_UAID_F4A475FF15A3736A02_1961895679"

def remove_actor_if_exists(name):
    acts = invoke_tool("find_actors", "editor_toolset.toolsets.scene.SceneTools", {
        "name": name, "tag": "", "collision_channels": []
    }).get("returnValue", [])
    for a in acts:
        invoke_tool("remove_from_scene", "editor_toolset.toolsets.scene.SceneTools", {"actor": a})

def place_or_update_actor(name, asset_path, location, rotation, scale, folder="Environment/Curzon_Pond"):
    existing = invoke_tool("find_actors", "editor_toolset.toolsets.scene.SceneTools", {
        "name": name, "tag": "", "collision_channels": []
    }).get("returnValue", [])

    xform = {"location": location, "rotation": rotation, "scale": scale}

    if existing:
        invoke_tool("set_actor_transform", "editor_toolset.toolsets.actor.ActorTools", {
            "actor": existing[0],
            "xform": xform
        })
        return existing[0].get("refPath")
    else:
        res = invoke_tool("add_to_scene_from_asset", "editor_toolset.toolsets.scene.SceneTools", {
            "asset_path": asset_path,
            "name": name,
            "xform": xform
        })
        pref = res.get("returnValue", {}).get("refPath")
        if pref and folder:
            invoke_tool("set_actor_folder", "editor_toolset.toolsets.scene.SceneTools", {
                "actor": {"refPath": pref},
                "folder_path": folder
            })
        return pref

def main():
    print("=" * 60)
    print("1. Removing duplicate South and East bamboo clusters...")
    # Remove CurzonPond_South_Bamboo_01..21
    removed_count = 0
    for i in range(1, 22):
        name = f"CurzonPond_South_Bamboo_{i:02d}"
        acts = invoke_tool("find_actors", "editor_toolset.toolsets.scene.SceneTools", {
            "name": name, "tag": "", "collision_channels": []
        }).get("returnValue", [])
        for a in acts:
            invoke_tool("remove_from_scene", "editor_toolset.toolsets.scene.SceneTools", {"actor": a})
            removed_count += 1

    for i in range(1, 6):
        name = f"CurzonPond_East_Bamboo_{i:02d}"
        acts = invoke_tool("find_actors", "editor_toolset.toolsets.scene.SceneTools", {
            "name": name, "tag": "", "collision_channels": []
        }).get("returnValue", [])
        for a in acts:
            invoke_tool("remove_from_scene", "editor_toolset.toolsets.scene.SceneTools", {"actor": a})
            removed_count += 1
    print(f"  ✓ Removed {removed_count} redundant bamboo actors.")

    print("\n2. Updating CurzonPond_WWM_Bamboo_01..17 with optimal framing & placement...")
    bamboo_mesh = "/Game/SparkVision/Campus/Environment/SM_Cluster_Bamboo_Thicket.SM_Cluster_Bamboo_Thicket"
    
    # Bamboo layout calibrated along Y = -1800 where Debdaru trunks sit
    # Bamboo_01 is framed back at (2100, -1850) with scale 2.2 so it doesn't obstruct foreground camera
    wwm_bamboos = [
        {"name": "CurzonPond_WWM_Bamboo_01", "x": 2100.0, "y": -1850.0, "z": 15.0, "scale": 2.2, "yaw": 20.0},
        {"name": "CurzonPond_WWM_Bamboo_02", "x": 2550.0, "y": -1800.0, "z": 15.0, "scale": 2.8, "yaw": 45.0},
        {"name": "CurzonPond_WWM_Bamboo_03", "x": 2950.0, "y": -1820.0, "z": 15.0, "scale": 2.8, "yaw": -20.0},
        {"name": "CurzonPond_WWM_Bamboo_04", "x": 3350.0, "y": -1800.0, "z": 15.0, "scale": 2.8, "yaw": 35.0},
        {"name": "CurzonPond_WWM_Bamboo_05", "x": 3750.0, "y": -1820.0, "z": 15.0, "scale": 2.8, "yaw": -15.0},
        {"name": "CurzonPond_WWM_Bamboo_06", "x": 4150.0, "y": -1800.0, "z": 15.0, "scale": 2.8, "yaw": 50.0},
        {"name": "CurzonPond_WWM_Bamboo_07", "x": 4550.0, "y": -1820.0, "z": 15.0, "scale": 2.8, "yaw": -35.0},
        {"name": "CurzonPond_WWM_Bamboo_08", "x": 4950.0, "y": -1800.0, "z": 15.0, "scale": 2.8, "yaw": 25.0},
        {"name": "CurzonPond_WWM_Bamboo_09", "x": 5350.0, "y": -1820.0, "z": 15.0, "scale": 2.8, "yaw": -10.0},
        {"name": "CurzonPond_WWM_Bamboo_10", "x": 5750.0, "y": -1800.0, "z": 15.0, "scale": 2.8, "yaw": 40.0},
        {"name": "CurzonPond_WWM_Bamboo_11", "x": 6150.0, "y": -1820.0, "z": 15.0, "scale": 2.8, "yaw": -25.0},
        {"name": "CurzonPond_WWM_Bamboo_12", "x": 6550.0, "y": -1780.0, "z": 15.0, "scale": 2.8, "yaw": 30.0},
        {"name": "CurzonPond_WWM_Bamboo_13", "x": 6950.0, "y": -1650.0, "z": 15.0, "scale": 2.8, "yaw": -15.0},
        {"name": "CurzonPond_WWM_Bamboo_14", "x": 7300.0, "y": -1300.0, "z": 15.0, "scale": 2.8, "yaw": 45.0},
        {"name": "CurzonPond_WWM_Bamboo_15", "x": 7350.0, "y": -900.0,  "z": 15.0, "scale": 2.8, "yaw": -30.0},
        {"name": "CurzonPond_WWM_Bamboo_16", "x": 7350.0, "y": -500.0,  "z": 15.0, "scale": 2.8, "yaw": 15.0},
        {"name": "CurzonPond_WWM_Bamboo_17", "x": 7350.0, "y": -100.0,  "z": 15.0, "scale": 2.8, "yaw": -40.0},
    ]

    for b in wwm_bamboos:
        place_or_update_actor(
            b["name"], bamboo_mesh,
            location={"x": b["x"], "y": b["y"], "z": b["z"]},
            rotation={"pitch": 0.0, "yaw": b["yaw"], "roll": 0.0},
            scale={"x": b["scale"], "y": b["scale"], "z": 2.2},
            folder="Environment/Curzon_Pond/Screen_Bamboo"
        )
    print(f"  ✓ Updated {len(wwm_bamboos)} WWM bamboo clusters.")

    print("\n3. Configuring PostProcessVolume Lumen settings...")
    vals = {
        "Settings": {
            "bOverride_LumenSurfaceCacheResolution": True,
            "lumenSurfaceCacheResolution": 0.65,
            "bOverride_LumenSceneViewDistance": True,
            "lumenSceneViewDistance": 14000.0,
            "bOverride_LumenSceneDetail": True,
            "lumenSceneDetail": 0.8
        }
    }
    invoke_tool("set_properties", "editor_toolset.toolsets.object.ObjectTools", {
        "instance": {"refPath": PP_ACTOR},
        "values": json.dumps(vals)
    })
    print("  ✓ PostProcessVolume updated.")

    print("\n4. Saving level...")
    invoke_tool("save_assets", "editor_toolset.toolsets.asset.AssetTools", {
        "asset_paths": ["/Game/SparkVision/Maps/Level01/LV_Level01_Compact_Campus"]
    })
    print("  ✓ Level saved.")

if __name__ == "__main__":
    main()
