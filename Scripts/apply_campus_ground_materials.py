#!/usr/bin/env python3
"""
Assign Calibrated PBR Ground Materials to Campus Ground Surfaces
Sets appropriate material instances for maintained lawns, natural turf, tree base loam, and flowerbeds.
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

FOLDER = "/Game/SparkVision/Materials"
MAT_LAWN = f"{FOLDER}/MI_Ground_Lawn_Maintained.MI_Ground_Lawn_Maintained"
MAT_TURF = f"{FOLDER}/MI_Ground_Turf_Natural.MI_Ground_Turf_Natural"
MAT_LOAM = f"{FOLDER}/MI_Ground_TreeBase_Loam.MI_Ground_TreeBase_Loam"
MAT_SOIL = f"{FOLDER}/MI_Ground_Garden_Soil.MI_Ground_Garden_Soil"

ASSIGNMENTS = [
    # Maintained Lawns
    ("Curzon_Botanical_Plaza_Ground", MAT_LAWN),
    ("Green_TSCOpenGatheringLawn", MAT_LAWN),
    ("Green_MallChattarOpenLawns", MAT_LAWN),
    
    # Natural Turf & Base Campus Terrain
    ("Green_SuhrawardyUdyanScenicBorder", MAT_TURF),
    ("Main_Campus_Ground_Terrain", MAT_TURF),
    
    # Tree Base Root Loam
    ("Curzon_Litter_Patch_1", MAT_LOAM),
    ("TheMall_Banyan1_Litter", MAT_LOAM),
    ("TheMall_Banyan2_Litter", MAT_LOAM),
    ("HakimChattar_Litter_1", MAT_LOAM),
    ("Fuller_Litter_Patch_1", MAT_LOAM),
    ("Fuller_Litter_Patch_2", MAT_LOAM),
    
    # Garden Beds & Circular Parterres
    ("Flowerbed_TSC_Raju_Plaza", MAT_SOIL),
    ("Flowerbed_Doyel_Plaza_North", MAT_SOIL),
    ("Flowerbed_Doyel_Plaza_South", MAT_SOIL),
    ("Flowerbed_CentralLibrary_Front", MAT_SOIL),
    ("Flowerbed_Shahidullah_Quad", MAT_SOIL),
    ("Flowerbed_Shaheed_Garden_Left", MAT_SOIL),
    ("Flowerbed_Shaheed_Garden_Right", MAT_SOIL),
    ("Flowerbed_KalaBhaban_Garden", MAT_SOIL),
    ("Flowerbed_TSC_Cafeteria_Lawn", MAT_SOIL),
]

def main():
    print("=" * 70)
    print("ASSIGNING CALIBRATED GROUND MATERIALS ACROSS DU CAMPUS")
    print("=" * 70)
    
    with open("Documentation/Environment/Grass/raw_surface_audit.json") as f:
        data = json.load(f)
        
    actor_map = {s["label"]: s for s in data["surfaces"]}
    
    for label, mat_path in ASSIGNMENTS:
        s = actor_map.get(label)
        if not s:
            print(f"  ? Actor '{label}' not in audit map")
            continue
            
        actor_ref = {"refPath": s["ref"]}
        comps = invoke_tool("get_components", "editor_toolset.toolsets.actor.ActorTools", {
            "actor": actor_ref
        }).get("returnValue", [])
        
        for c in comps:
            try:
                invoke_tool("set_properties", "editor_toolset.toolsets.object.ObjectTools", {
                    "instance": c,
                    "values": json.dumps({
                        "OverrideMaterials": [{"refPath": mat_path}]
                    })
                })
                print(f"  ✓ Assigned {mat_path.split('.')[-1]} to {label}")
            except Exception as e:
                print(f"  ✗ Error on {label}: {e}")
                
    # Save the current level
    lvl = invoke_tool("get_current_level", "editor_toolset.toolsets.scene.SceneTools", {}).get("returnValue", "")
    invoke_tool("save_assets", "editor_toolset.toolsets.asset.AssetTools", {
        "asset_paths": [lvl]
    })
    print(f"\n✅ Ground materials successfully assigned and level saved!")

if __name__ == "__main__":
    main()
