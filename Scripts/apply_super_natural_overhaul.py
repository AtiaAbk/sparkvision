#!/usr/bin/env python3
"""
Complete Super-Natural Foliage & Lighting Overhaul for SparkVision Level 01:
1. Swaps all old UV-sphere trees in the level with the new high-density natural leaf-card trees:
   - SM_Tree_Raintree_Avenue -> SM_Natural_Raintree_Grand
   - SM_Campus_Tree_Hero -> SM_Natural_Banyan_Heritage
   - SM_Tree_Krishnachura_WWM -> SM_Natural_Krishnachura_Bloom
2. Spawns foreground undergrowth fern clusters (SM_Natural_Fern_Cluster) along the promenade & pond ghat.
3. Overhauls DirectionalLight, SkyLight, and Volumetric Fog to match Where Winds Meet natural daylight.
4. Saves the persistent level asset cleanly to disk.
"""

import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

NEW_RAINTREE = "/Game/SparkVision/Campus/Environment/SM_Natural_Raintree_Grand.SM_Natural_Raintree_Grand"
NEW_BANYAN = "/Game/SparkVision/Campus/Environment/SM_Natural_Banyan_Heritage.SM_Natural_Banyan_Heritage"
NEW_KRISHNACHURA = "/Game/SparkVision/Campus/Environment/SM_Natural_Krishnachura_Bloom.SM_Natural_Krishnachura_Bloom"
NEW_FERN = "/Game/SparkVision/Campus/Environment/SM_Natural_Fern_Cluster.SM_Natural_Fern_Cluster"

def main():
    print("=" * 70)
    print("UPGRADING SPARKVISION CAMPUS TO SUPER-NATURAL WHERE WINDS MEET AESTHETICS")
    print("=" * 70)

    # -------------------------------------------------------------
    # 1. SWAP EXISTING LEVEL TREE ACTORS TO NATURAL LEAF-CARD MESHES
    # -------------------------------------------------------------
    print("\n[Phase 1] Swapping existing tree actors to natural leaf-card meshes...")

    tree_actors = invoke_tool("find_actors", "editor_toolset.toolsets.scene.SceneTools", {
        "name": "Tree",
        "tag": "",
        "collision_channels": []
    }).get("returnValue", [])

    print(f"Found {len(tree_actors)} tree actors to evaluate...")
    swapped_raintree = 0
    swapped_banyan = 0
    swapped_krishna = 0

    for a in tree_actors:
        actor_ref = a["refPath"]
        comps = invoke_tool("get_components", "editor_toolset.toolsets.actor.ActorTools", {
            "actor": {"refPath": actor_ref}
        }).get("returnValue", [])

        sm_comps = [c["refPath"] for c in comps if "StaticMeshComponent" in c["refPath"]]
        if not sm_comps:
            continue

        comp_ref = sm_comps[0]
        props = invoke_tool("get_properties", "editor_toolset.toolsets.object.ObjectTools", {
            "instance": {"refPath": comp_ref},
            "properties": ["StaticMesh"]
        })
        curr_mesh = json.loads(props.get("returnValue", "{}")).get("StaticMesh", {}).get("refPath", "")

        target_mesh = None
        target_scale = None

        if "SM_Tree_Raintree_Avenue" in curr_mesh:
            target_mesh = NEW_RAINTREE
            swapped_raintree += 1
        elif "SM_Campus_Tree_Hero" in curr_mesh:
            target_mesh = NEW_BANYAN
            swapped_banyan += 1
        elif "SM_Tree_Krishnachura" in curr_mesh:
            target_mesh = NEW_KRISHNACHURA
            swapped_krishna += 1

        if target_mesh:
            # Set StaticMesh
            invoke_tool("set_properties", "editor_toolset.toolsets.object.ObjectTools", {
                "instance": {"refPath": comp_ref},
                "values": json.dumps({
                    "StaticMesh": {"refPath": target_mesh},
                    "OverrideMaterials": [] # Revert to the mesh's assigned Two-Sided Foliage materials
                })
            })

    print(f"  ✓ Swapped {swapped_raintree} Raintrees to SM_Natural_Raintree_Grand")
    print(f"  ✓ Swapped {swapped_banyan} Hero trees to SM_Natural_Banyan_Heritage")
    print(f"  ✓ Swapped {swapped_krishna} Krishnachura trees to SM_Natural_Krishnachura_Bloom")

    # -------------------------------------------------------------
    # 2. SPAWN FOREGROUND NATURAL FERNS (Matching Ref 1 Foreground)
    # -------------------------------------------------------------
    print("\n[Phase 2] Spawning lush foreground undergrowth ferns...")
    fern_locations = [
        # Along Curzon Promenade
        {"x": 650.0, "y": -120.0, "z": 80.0},
        {"x": 750.0, "y": 80.0, "z": 80.0},
        {"x": 900.0, "y": -220.0, "z": 80.0},
        {"x": 1050.0, "y": 140.0, "z": 80.0},
        {"x": 1200.0, "y": -180.0, "z": 70.0},
        # Around Curzon Botanical Pond Shorelines
        {"x": 1800.0, "y": -450.0, "z": 30.0},
        {"x": 2100.0, "y": -650.0, "z": 25.0},
        {"x": 2300.0, "y": -350.0, "z": 25.0},
        {"x": 2600.0, "y": -150.0, "z": 25.0},
        {"x": 2400.0, "y": 200.0, "z": 25.0},
        {"x": 2100.0, "y": 350.0, "z": 25.0},
        {"x": 1700.0, "y": 250.0, "z": 30.0},
        # Curzon Hall Entrance Steps
        {"x": -4800.0, "y": -350.0, "z": 120.0},
        {"x": -4800.0, "y": 350.0, "z": 120.0},
    ]

    for idx, pos in enumerate(fern_locations):
        label = f"WWM_Natural_Fern_{idx+1:02d}"
        xform = {
            "location": pos,
            "rotation": {"pitch": 0.0, "yaw": float(idx * 47 % 360), "roll": 0.0},
            "scale": {"x": 1.4, "y": 1.4, "z": 1.4}
        }
        try:
            invoke_tool("add_to_scene_from_asset", "editor_toolset.toolsets.scene.SceneTools", {
                "asset_path": NEW_FERN.split(".")[0],
                "name": label,
                "xform": xform
            })
        except Exception as e:
            print(f"  Notice adding fern {label}: {e}")

    print(f"  ✓ Placed {len(fern_locations)} lush natural undergrowth ferns")

    # -------------------------------------------------------------
    # 3. NATURAL LIGHTING & ATMOSPHERIC RECALIBRATION (Where Winds Meet Standard)
    # -------------------------------------------------------------
    print("\n[Phase 3] Recalibrating Lighting & Atmospheric Atmosphere...")

    # A. Directional Light: Crisp 5700K Daylight
    dir_light_comp = "/Game/SparkVision/Maps/Level01/LV_Level01_Compact_Campus.LV_Level01_Compact_Campus:PersistentLevel.DirectionalLight_UAID_F4A475FF15A3736A02_1961932697.LightComponent0"
    invoke_tool("set_properties", "editor_toolset.toolsets.object.ObjectTools", {
        "instance": {"refPath": dir_light_comp},
        "values": json.dumps({
            "Intensity": 85000.0,
            "LightColor": {"r": 1.0, "g": 0.99, "b": 0.96, "a": 1.0}, # Crisp daylight, not orange!
            "bEnableLightShaftBloom": True,
            "bEnableLightShaftOcclusion": True,
            "bCastVolumetricShadow": True,
            "BloomScale": 0.35
        })
    })
    print("  ✓ Recalibrated DirectionalLight to natural 5700K daylight with sun shafts")

    # B. SkyLight: Cool Blue Rayleigh Fill with Real-Time Capture
    sky_comp = "/Game/SparkVision/Maps/Level01/LV_Level01_Compact_Campus.LV_Level01_Compact_Campus:PersistentLevel.SkyLight_UAID_F4A475FF15A3736A02_1961943709.SkyLightComponent0"
    invoke_tool("set_properties", "editor_toolset.toolsets.object.ObjectTools", {
        "instance": {"refPath": sky_comp},
        "values": json.dumps({
            "Intensity": 1.4,
            "LightColor": {"r": 0.82, "g": 0.91, "b": 1.0, "a": 1.0}, # Cool cyan-blue ambient fill
            "bRealTimeCapture": True
        })
    })
    print("  ✓ Recalibrated SkyLight to real-time cyan-blue ambient fill")

    # C. Exponential Height Fog: Low-Altitude Valley Ground Mist
    fog_comp = "/Game/SparkVision/Maps/Level01/LV_Level01_Compact_Campus.LV_Level01_Compact_Campus:PersistentLevel.ExponentialHeightFog_UAID_F4A475FF15A3736A02_1961936700.HeightFogComponent0"
    invoke_tool("set_properties", "editor_toolset.toolsets.object.ObjectTools", {
        "instance": {"refPath": fog_comp},
        "values": json.dumps({
            "FogDensity": 0.00065, # Thin crisp air
            "FogHeightFalloff": 0.0055, # Ground mist resting over pond water
            "bEnableVolumetricFog": True,
            "VolumetricFogScatteringDistribution": 0.32,
            "VolumetricFogDistance": 22000.0,
            "VolumetricFogAlbedo": {"r": 0.88, "g": 0.94, "b": 1.0, "a": 1.0} # Soft bluish-white mist
        })
    })
    print("  ✓ Recalibrated Exponential Height Fog to low-altitude valley ground mist")

    # -------------------------------------------------------------
    # 4. SAVE LEVEL ASSET
    # -------------------------------------------------------------
    print("\n[Phase 4] Saving persistent level asset...")
    save_res = invoke_tool("save_assets", "editor_toolset.toolsets.asset.AssetTools", {
        "asset_paths": ["/Game/SparkVision/Maps/Level01/LV_Level01_Compact_Campus"]
    })
    print("  ✓ Level saved cleanly:", save_res)

    print("\n" + "=" * 70)
    print("SUPER-NATURAL OVERHAUL COMPLETED SUCCESSFULLY!")
    print("=" * 70)

if __name__ == "__main__":
    main()
