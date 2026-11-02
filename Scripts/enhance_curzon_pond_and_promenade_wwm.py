#!/usr/bin/env python3
"""
Enhance Curzon Pond and Promenade to AAA Where Winds Meet Standard:
1. Stately Debdaru Columnar tree wall screening the northern perimeter behind the pond
2. Waterline calibration for Curzon Botanical Pond (lapping realistically against Ghat)
3. Krishnachura flower blossom drifts along Curzon Promenade and Pond Ghat
4. Brick & Trim overrides for Curzon Chemistry Physics Labs
5. Saves level
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

DEBDARU_MESH = "/Game/SparkVision/Campus/Environment/SM_Tree_Debdaru_Columnar.SM_Tree_Debdaru_Columnar"
PETAL_MESH = "/Game/SparkVision/Campus/Environment/SM_Decal_Petal_Scatter.SM_Decal_Petal_Scatter"

def main():
    print("=" * 70)
    print("ENHANCING CURZON POND & PROMENADE ATMOSPHERE (WWM AESTHETICS)")
    print("=" * 70)

    # 1. Dress Supporting_CurzonChemistryPhysicsLabs with authentic brick & white trim
    print("\n1. Applying authentic Curzon brick & trim to Science Annex...")
    res = invoke_tool("find_actors", "editor_toolset.toolsets.scene.SceneTools", {
        "name": "Supporting_CurzonChemistryPhysicsLabs", "tag": "", "collision_channels": []
    })
    actors = res.get("returnValue", [])
    if actors:
        a = actors[0]
        comps = invoke_tool("get_components", "editor_toolset.toolsets.actor.ActorTools", {"actor": a}).get("returnValue", [])
        if comps:
            override_mats = [
                {"refPath": "/Game/SparkVision/Materials/MI_Curzon_StonePaving.MI_Curzon_StonePaving"},
                {"refPath": "/Game/SparkVision/Materials/MI_Curzon_Brick.MI_Curzon_Brick"},
                {"refPath": "/Game/SparkVision/Materials/MI_Curzon_WhiteTrim.MI_Curzon_WhiteTrim"},
            ]
            invoke_tool("set_properties", "editor_toolset.toolsets.object.ObjectTools", {
                "instance": comps[0],
                "values": json.dumps({"OverrideMaterials": override_mats})
            })
            print("  ✓ Applied MI_Curzon_StonePaving, Brick & WhiteTrim overrides")

    # 2. Calibrate Pond Waterline
    print("\n2. Calibrating Curzon Pond waterline...")
    res_pond = invoke_tool("find_actors", "editor_toolset.toolsets.scene.SceneTools", {
        "name": "Curzon_Iconic_Botanical_Pond", "tag": "", "collision_channels": []
    })
    ponds = res_pond.get("returnValue", [])
    if ponds:
        p_actor = ponds[0]
        invoke_tool("set_actor_transform", "editor_toolset.toolsets.actor.ActorTools", {
            "actor": p_actor,
            "xform": {
                "location": {"x": 4800.0, "y": 0.0, "z": 7.0},
                "rotation": {"pitch": 0.0, "yaw": 0.0, "roll": 0.0},
                "scale": {"x": 52.0, "y": 36.0, "z": 0.15}
            },
            "worldspace": True
        })
        print("  ✓ Lowered pond water plane to Z=7.0 (water surface at Z=14.5, lapping 5.5cm below Ghat)")

    # 3. Plant Stately Debdaru Columnar Tree Wall along Pond North Bank
    print("\n3. Planting Debdaru Columnar screening grove behind Curzon Pond...")
    debdaru_coords = [
        # Front row along the brick wall
        {"x": 2800.0, "y": 3400.0, "z": 20.0, "yaw": 15.0, "sx": 1.2, "sy": 1.2, "sz": 1.9},
        {"x": 3200.0, "y": 3450.0, "z": 20.0, "yaw": 45.0, "sx": 1.3, "sy": 1.3, "sz": 2.1},
        {"x": 3600.0, "y": 3500.0, "z": 20.0, "yaw": 80.0, "sx": 1.1, "sy": 1.1, "sz": 1.8},
        {"x": 4100.0, "y": 3550.0, "z": 20.0, "yaw": 115.0, "sx": 1.4, "sy": 1.4, "sz": 2.2},
        {"x": 4600.0, "y": 3550.0, "z": 20.0, "yaw": -25.0, "sx": 1.2, "sy": 1.2, "sz": 2.0},
        {"x": 5100.0, "y": 3500.0, "z": 20.0, "yaw": 30.0, "sx": 1.3, "sy": 1.3, "sz": 2.1},
        {"x": 5600.0, "y": 3450.0, "z": 20.0, "yaw": 75.0, "sx": 1.2, "sy": 1.2, "sz": 1.9},
        {"x": 6100.0, "y": 3400.0, "z": 20.0, "yaw": -60.0, "sx": 1.4, "sy": 1.4, "sz": 2.3},
        {"x": 6600.0, "y": 3350.0, "z": 20.0, "yaw": 40.0, "sx": 1.3, "sy": 1.3, "sz": 2.0},
        {"x": 7100.0, "y": 3300.0, "z": 20.0, "yaw": 90.0, "sx": 1.2, "sy": 1.2, "sz": 1.8},
        # Staggered back row for deep lush foliage depth
        {"x": 3400.0, "y": 3750.0, "z": 20.0, "yaw": -40.0, "sx": 1.4, "sy": 1.4, "sz": 2.4},
        {"x": 4300.0, "y": 3800.0, "z": 20.0, "yaw": 60.0, "sx": 1.3, "sy": 1.3, "sz": 2.2},
        {"x": 5300.0, "y": 3800.0, "z": 20.0, "yaw": -15.0, "sx": 1.4, "sy": 1.4, "sz": 2.3},
        {"x": 6300.0, "y": 3750.0, "z": 20.0, "yaw": 105.0, "sx": 1.3, "sy": 1.3, "sz": 2.1},
    ]

    for idx, d in enumerate(debdaru_coords):
        aname = f"CurzonPond_Debdaru_Wall_{idx+1:02d}"
        try:
            res_sp = invoke_tool("add_to_scene_from_asset", "editor_toolset.toolsets.scene.SceneTools", {
                "asset_path": DEBDARU_MESH,
                "name": aname,
                "xform": {
                    "location": {"x": d["x"], "y": d["y"], "z": d["z"]},
                    "rotation": {"pitch": 0.0, "yaw": d["yaw"], "roll": 0.0},
                    "scale": {"x": d["sx"], "y": d["sy"], "z": d["sz"]}
                }
            })
            new_ref = res_sp.get("returnValue", {}).get("refPath")
            if new_ref:
                invoke_tool("set_actor_folder", "editor_toolset.toolsets.scene.SceneTools", {
                    "actor": {"refPath": new_ref},
                    "folder_path": "Environment/Curzon_Pond/Debdaru_Screen"
                })
                print(f"  ✓ Spawned {aname} at ({d['x']:.0f}, {d['y']:.0f}) scale_z={d['sz']:.1f}")
        except Exception as e:
            print(f"  ✗ Error spawning {aname}: {e}")

    # 4. Spawn Krishnachura Blossom Petal Drifts along Curzon Promenade & Pond Ghat
    print("\n4. Spawning Krishnachura flower petal drifts (Wuxia atmospheric breeze)...")
    petal_locations = [
        # Curzon Hero Promenade & Veranda steps
        {"name": "Petal_Drift_Curzon_Landing_1", "x": -3450.0, "y": 150.0, "z": 151.0, "yaw": 20.0, "s": 1.8},
        {"name": "Petal_Drift_Curzon_Landing_2", "x": -3450.0, "y": -150.0, "z": 151.0, "yaw": -35.0, "s": 1.6},
        {"name": "Petal_Drift_Curzon_Steps_1", "x": -3650.0, "y": 0.0, "z": 80.0, "yaw": 45.0, "s": 2.2},
        {"name": "Petal_Drift_Curzon_Promenade_1", "x": -4000.0, "y": 180.0, "z": 21.0, "yaw": -15.0, "s": 2.5},
        {"name": "Petal_Drift_Curzon_Promenade_2", "x": -4300.0, "y": -120.0, "z": 21.0, "yaw": 70.0, "s": 2.0},
        {"name": "Petal_Drift_Curzon_Promenade_3", "x": -4600.0, "y": 60.0, "z": 21.0, "yaw": 110.0, "s": 2.3},
        {"name": "Petal_Drift_Curzon_UnderTree_E", "x": -3800.0, "y": 600.0, "z": 21.0, "yaw": 5.0, "s": 2.8},
        {"name": "Petal_Drift_Curzon_UnderTree_W", "x": -3800.0, "y": -600.0, "z": 21.0, "yaw": -50.0, "s": 2.6},
        # Curzon Botanical Pond Ghat stairs
        {"name": "Petal_Drift_Pond_Ghat_1", "x": 2350.0, "y": 50.0, "z": 21.0, "yaw": 30.0, "s": 1.9},
        {"name": "Petal_Drift_Pond_Ghat_2", "x": 2400.0, "y": -80.0, "z": 21.0, "yaw": -75.0, "s": 1.7},
        {"name": "Petal_Drift_Pond_Shore_1", "x": 2600.0, "y": -600.0, "z": 21.0, "yaw": 40.0, "s": 2.4},
        {"name": "Petal_Drift_Pond_Shore_2", "x": 2800.0, "y": 700.0, "z": 21.0, "yaw": -20.0, "s": 2.2},
    ]

    for p in petal_locations:
        try:
            res_p = invoke_tool("add_to_scene_from_asset", "editor_toolset.toolsets.scene.SceneTools", {
                "asset_path": PETAL_MESH,
                "name": p["name"],
                "xform": {
                    "location": {"x": p["x"], "y": p["y"], "z": p["z"]},
                    "rotation": {"pitch": 0.0, "yaw": p["yaw"], "roll": 0.0},
                    "scale": {"x": p["s"], "y": p["s"], "z": 1.0}
                }
            })
            pref = res_p.get("returnValue", {}).get("refPath")
            if pref:
                invoke_tool("set_actor_folder", "editor_toolset.toolsets.scene.SceneTools", {
                    "actor": {"refPath": pref},
                    "folder_path": "Environment/Petal_Blossoms"
                })
                print(f"  ✓ Spawned {p['name']} at ({p['x']:.0f}, {p['y']:.0f}, {p['z']:.0f})")
        except Exception as e:
            print(f"  ✗ Error spawning petal {p['name']}: {e}")

    # 5. Save level
    print("\n5. Saving level LV_Level01_Compact_Campus...")
    try:
        invoke_tool("save_assets", "editor_toolset.toolsets.asset.AssetTools", {
            "asset_paths": ["/Game/SparkVision/Maps/Level01/LV_Level01_Compact_Campus"]
        })
        print("✅ Saved LV_Level01_Compact_Campus successfully!")
    except Exception as e:
        print(f"Notice saving level: {e}")

if __name__ == "__main__":
    main()
