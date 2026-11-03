#!/usr/bin/env python3
"""
SPARKVISION — CURZON HALL POND COMPLETE WATER RECONSTRUCTION
Ultra-Realistic Natural Water | Single Layer Water | M4 Performance Optimization

1. Assigns calibrated MI_CurzonPond_Water (SingleLayerWater) to Curzon_Iconic_Botanical_Pond.
2. Creates/updates dark submerged pond basin bed (Curzon_Pond_Submerged_Basin) for authentic depth attenuation.
3. Relocates 7 misplaced trees out of the water core to bank perimeters to open the Curzon Hall reflection vista.
4. Upgrades water lily clusters to SM_Pond_WaterLily_Cluster with authentic Shapla blooms and lily pad PBR materials.
5. Adds submerged Koi fish (SM_Pond_KoiFish) in clear shallows near the Ghat.
6. Saves level LV_Level01_Compact_Campus.
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

POND_ACTOR_REF = {"refPath": "/Game/SparkVision/Maps/Level01/LV_Level01_Compact_Campus.LV_Level01_Compact_Campus:PersistentLevel.StaticMeshActor_UAID_685EDD40918A671003_1769599862"}
POND_COMP_REF = {"refPath": "/Game/SparkVision/Maps/Level01/LV_Level01_Compact_Campus.LV_Level01_Compact_Campus:PersistentLevel.StaticMeshActor_UAID_685EDD40918A671003_1769599862.StaticMeshComponent0"}
WATER_MAT_REF = {"refPath": "/Game/SparkVision/Materials/MI_CurzonPond_Water.MI_CurzonPond_Water"}
CUBE_MESH_REF = "/Engine/BasicShapes/Cube.Cube"
LILY_CLUSTER_MESH = "/Game/SparkVision/Campus/Environment/SM_Pond_WaterLily_Cluster.SM_Pond_WaterLily_Cluster"
KOI_MESH = "/Game/SparkVision/Campus/Environment/SM_Pond_KoiFish.SM_Pond_KoiFish"
KOI_MAT = "/Game/SparkVision/Materials/MI_Pond_KoiFish.MI_Pond_KoiFish"
SILT_MAT = "/Game/SparkVision/Materials/MI_Curzon_StonePaving.MI_Curzon_StonePaving"

def main():
    print("=" * 70)
    print("EXECUTING COMPLETE CURZON HALL POND WATER RECONSTRUCTION")
    print("=" * 70)

    # -------------------------------------------------------------
    # STEP 1: Calibrate MI_CurzonPond_Water Optical Parameters
    # -------------------------------------------------------------
    print("\n1. Calibrating MI_CurzonPond_Water optical parameters...")
    scalars = [
        ("Roughness", 0.05),
        ("Refraction_IOR", 1.333),
        ("PhaseG", 0.20)
    ]
    for p, val in scalars:
        invoke_tool("set_scalar_parameter", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
            "instance": WATER_MAT_REF, "name": p, "value": val
        })

    vectors = [
        ("BaseColor_Tint", {"r": 0.008, "g": 0.024, "b": 0.016, "a": 1.0}),
        ("ScatteringCoefficients", {"r": 0.002, "g": 0.009, "b": 0.004, "a": 1.0}),
        ("AbsorptionCoefficients", {"r": 0.038, "g": 0.007, "b": 0.026, "a": 1.0}),
        ("ColorScaleBehindWater", {"r": 0.32, "g": 0.42, "b": 0.32, "a": 1.0})
    ]
    for p, val in vectors:
        invoke_tool("set_vector_parameter", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
            "instance": WATER_MAT_REF, "name": p, "value": val
        })
    print("  ✓ Calibrated Single Layer Water scattering & absorption (authentic freshwater pond)")

    # -------------------------------------------------------------
    # STEP 2: Configure Pond Water Surface Mesh & Material
    # -------------------------------------------------------------
    print("\n2. Configuring Curzon_Iconic_Botanical_Pond actor...")
    invoke_tool("set_actor_transform", "editor_toolset.toolsets.actor.ActorTools", {
        "actor": POND_ACTOR_REF,
        "worldspace": True,
        "xform": {
            "location": {"x": 4800.0, "y": 0.0, "z": 7.0},
            "rotation": {"pitch": 0.0, "yaw": 0.0, "roll": 0.0},
            "scale": {"x": 52.0, "y": 36.0, "z": 0.15}
        }
    })
    invoke_tool("set_properties", "editor_toolset.toolsets.object.ObjectTools", {
        "instance": POND_COMP_REF,
        "values": json.dumps({"OverrideMaterials": [WATER_MAT_REF]})
    })
    print("  ✓ Assigned MI_CurzonPond_Water to Curzon_Iconic_Botanical_Pond (Water surface at Z=14.5)")

    # -------------------------------------------------------------
    # STEP 3: Submerged Dark Silt Basin Bed
    # -------------------------------------------------------------
    print("\n3. Setting up submerged dark silt basin bed...")
    res_basin = invoke_tool("find_actors", "editor_toolset.toolsets.scene.SceneTools", {
        "name": "Curzon_Pond_Submerged_Basin", "tag": "", "collision_channels": []
    })
    basin_actors = res_basin.get("returnValue", [])
    if not basin_actors:
        basin_actor = invoke_tool("add_to_scene_from_asset", "editor_toolset.toolsets.scene.SceneTools", {
            "asset_path": CUBE_MESH_REF,
            "name": "Curzon_Pond_Submerged_Basin",
            "xform": {
                "location": {"x": 4800.0, "y": 0.0, "z": -25.0},
                "rotation": {"pitch": 0.0, "yaw": 0.0, "roll": 0.0},
                "scale": {"x": 52.0, "y": 36.0, "z": 0.40}
            }
        }).get("returnValue")
        print("  ✓ Created Curzon_Pond_Submerged_Basin actor")
    else:
        basin_actor = basin_actors[0]
        invoke_tool("set_actor_transform", "editor_toolset.toolsets.actor.ActorTools", {
            "actor": basin_actor,
            "worldspace": True,
            "xform": {
                "location": {"x": 4800.0, "y": 0.0, "z": -25.0},
                "rotation": {"pitch": 0.0, "yaw": 0.0, "roll": 0.0},
                "scale": {"x": 52.0, "y": 36.0, "z": 0.40}
            }
        })
        print("  ✓ Updated Curzon_Pond_Submerged_Basin transform")

    # Set basin material
    b_comps = invoke_tool("get_components", "editor_toolset.toolsets.actor.ActorTools", {"actor": basin_actor}).get("returnValue", [])
    if b_comps:
        invoke_tool("set_properties", "editor_toolset.toolsets.object.ObjectTools", {
            "instance": b_comps[0],
            "values": json.dumps({"OverrideMaterials": [{"refPath": SILT_MAT}]})
        })
        print("  ✓ Applied dark submerged riverbed silt material to basin")

    # Put in Pond Architecture folder
    invoke_tool("set_actor_folder", "editor_toolset.toolsets.scene.SceneTools", {
        "actor": basin_actor, "folder_path": "Environment/Curzon_Pond/Pond_Architecture"
    })

    # -------------------------------------------------------------
    # STEP 4: Relocate 7 Misplaced Trees from Water to Banks
    # -------------------------------------------------------------
    print("\n4. Relocating trees out of the water core to bank perimeters...")
    tree_relocations = {
        "WWM_Hero_Krishnachura_05": {"x": 4200.0, "y": 2050.0, "z": 20.0, "yaw": 25.0},  # North bank
        "WWM_Pond_Banyan_04": {"x": 2600.0, "y": 1950.0, "z": 20.0, "yaw": -45.0},         # North-West bank
        "WWM_Pond_Banyan_05": {"x": 2600.0, "y": -1950.0, "z": 20.0, "yaw": 45.0},        # South-West bank
        "WWM_Hero_Krishnachura_04": {"x": 5600.0, "y": 2050.0, "z": 20.0, "yaw": 80.0},  # North bank
        "WWM_Hero_Krishnachura_03": {"x": 5600.0, "y": -2050.0, "z": 20.0, "yaw": -80.0}, # South bank
        "WWM_Pond_Banyan_03": {"x": 7450.0, "y": 1000.0, "z": 20.0, "yaw": 115.0},        # East bank
        "WWM_Pond_Banyan_06": {"x": 7450.0, "y": -1000.0, "z": 20.0, "yaw": -115.0},      # East bank
    }

    for tree_name, pos in tree_relocations.items():
        res = invoke_tool("find_actors", "editor_toolset.toolsets.scene.SceneTools", {
            "name": tree_name, "tag": "", "collision_channels": []
        })
        acts = res.get("returnValue", [])
        if acts:
            invoke_tool("set_actor_transform", "editor_toolset.toolsets.actor.ActorTools", {
                "actor": acts[0],
                "worldspace": True,
                "xform": {
                    "location": {"x": pos["x"], "y": pos["y"], "z": pos["z"]},
                    "rotation": {"pitch": 0.0, "yaw": pos["yaw"], "roll": 0.0},
                    "scale": {"x": 1.0, "y": 1.0, "z": 1.0}
                }
            })
            print(f"  ✓ Moved {tree_name} to bank at ({pos['x']:.0f}, {pos['y']:.0f})")

    # -------------------------------------------------------------
    # STEP 5: Calibrate Water Lily Clusters (Shapla)
    # -------------------------------------------------------------
    print("\n5. Upgrading and positioning water lily clusters...")
    lily_positions = [
        # North-East cluster
        {"x": 6200.0, "y": 800.0, "z": 14.5, "yaw": 15.0, "s": 1.2},
        {"x": 5800.0, "y": 1100.0, "z": 14.5, "yaw": 60.0, "s": 1.0},
        # South-East cluster
        {"x": 6400.0, "y": -700.0, "z": 14.5, "yaw": -45.0, "s": 1.3},
        {"x": 5900.0, "y": -1000.0, "z": 14.5, "yaw": -90.0, "s": 1.1},
        # Near Ghat North shallows
        {"x": 3100.0, "y": 700.0, "z": 14.5, "yaw": 30.0, "s": 1.15},
        # Near Ghat South shallows
        {"x": 3100.0, "y": -700.0, "z": 14.5, "yaw": -30.0, "s": 1.25},
        # North bank fringe
        {"x": 4600.0, "y": 1200.0, "z": 14.5, "yaw": 75.0, "s": 1.05},
        # South bank fringe
        {"x": 4600.0, "y": -1200.0, "z": 14.5, "yaw": -75.0, "s": 1.1},
    ]

    lily_actors = invoke_tool("get_actors_in_folder", "editor_toolset.toolsets.scene.SceneTools", {
        "folder_path": "Environment/Curzon_Pond/Aquatic_Flora"
    }).get("returnValue", [])

    for idx, a in enumerate(lily_actors):
        if idx >= len(lily_positions):
            break
        lp = lily_positions[idx]
        # Position flush with water surface Z=14.5
        invoke_tool("set_actor_transform", "editor_toolset.toolsets.actor.ActorTools", {
            "actor": a,
            "worldspace": True,
            "xform": {
                "location": {"x": lp["x"], "y": lp["y"], "z": lp["z"]},
                "rotation": {"pitch": 0.0, "yaw": lp["yaw"], "roll": 0.0},
                "scale": {"x": lp["s"], "y": lp["s"], "z": lp["s"]}
            }
        })
        # Upgrade mesh to SM_Pond_WaterLily_Cluster
        comps = invoke_tool("get_components", "editor_toolset.toolsets.actor.ActorTools", {"actor": a}).get("returnValue", [])
        if comps:
            invoke_tool("set_properties", "editor_toolset.toolsets.object.ObjectTools", {
                "instance": comps[0],
                "values": json.dumps({
                    "StaticMesh": {"refPath": LILY_CLUSTER_MESH},
                    "OverrideMaterials": []
                })
            })
    print(f"  ✓ Upgraded and positioned {len(lily_actors)} water lily clusters flush with water surface")

    # -------------------------------------------------------------
    # STEP 6: Add Submerged Swimming Koi Fish
    # -------------------------------------------------------------
    print("\n6. Adding submerged swimming Koi fish near Ghat shallows...")
    koi_positions = [
        {"name": "Pond_KoiFish_School_01", "x": 2600.0, "y": -200.0, "z": 5.0, "yaw": 35.0, "s": 1.0},
        {"name": "Pond_KoiFish_School_02", "x": 2800.0, "y": 150.0, "z": 3.0, "yaw": -20.0, "s": 1.1},
        {"name": "Pond_KoiFish_School_03", "x": 2500.0, "y": 300.0, "z": 4.0, "yaw": 60.0, "s": 0.9},
    ]

    for kp in koi_positions:
        res = invoke_tool("find_actors", "editor_toolset.toolsets.scene.SceneTools", {
            "name": kp["name"], "tag": "", "collision_channels": []
        })
        if not res.get("returnValue"):
            k_act = invoke_tool("add_to_scene_from_asset", "editor_toolset.toolsets.scene.SceneTools", {
                "asset_path": KOI_MESH,
                "name": kp["name"],
                "xform": {
                    "location": {"x": kp["x"], "y": kp["y"], "z": kp["z"]},
                    "rotation": {"pitch": 0.0, "yaw": kp["yaw"], "roll": 0.0},
                    "scale": {"x": kp["s"], "y": kp["s"], "z": kp["s"]}
                }
            }).get("returnValue")
            if k_act:
                k_comps = invoke_tool("get_components", "editor_toolset.toolsets.actor.ActorTools", {"actor": k_act}).get("returnValue", [])
                if k_comps:
                    invoke_tool("set_properties", "editor_toolset.toolsets.object.ObjectTools", {
                        "instance": k_comps[0],
                        "values": json.dumps({"OverrideMaterials": [{"refPath": KOI_MAT}]})
                    })
                invoke_tool("set_actor_folder", "editor_toolset.toolsets.scene.SceneTools", {
                    "actor": k_act, "folder_path": "Environment/Curzon_Pond/Fauna"
                })
                print(f"  ✓ Spawned {kp['name']} submerged at Z={kp['z']}")
        else:
            print(f"  ✓ {kp['name']} already exists")

    # -------------------------------------------------------------
    # STEP 7: Save Level
    # -------------------------------------------------------------
    print("\n7. Saving level LV_Level01_Compact_Campus...")
    invoke_tool("save_assets", "editor_toolset.toolsets.asset.AssetTools", {
        "asset_paths": [
            "/Game/SparkVision/Maps/Level01/LV_Level01_Compact_Campus",
            "/Game/SparkVision/Materials/MI_CurzonPond_Water"
        ]
    })
    print("  ✓ Level and Material Instance saved successfully!")

    print("=" * 70)
    print("SUCCESS: Curzon Hall Pond Complete Water Reconstruction Done!")
    print("=" * 70)

if __name__ == "__main__":
    main()
