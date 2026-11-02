#!/usr/bin/env python3
"""
Upgrade Remaining Campus Material Instances to M_SparkVision_Master_PBR
Eliminates all flat BasicShapeMaterial shading across buildings, foliage, roads, and monuments.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

MASTER_PBR = "/Game/SparkVision/Materials/M_SparkVision_Master_PBR.M_SparkVision_Master_PBR"

MAPPINGS = [
    # Supporting Campus Buildings (Distant skylines & background blocks)
    ("MI_Supporting_Building", "/Game/SparkVision/Textures/T_Supporting_Building_D.T_Supporting_Building_D", "/Game/SparkVision/Textures/T_Supporting_Building_N.T_Supporting_Building_N"),
    # Modernist Hall Concrete
    ("MI_Hero_Modern", "/Game/SparkVision/Textures/T_Modern_Concrete_D.T_Modern_Concrete_D", "/Game/SparkVision/Textures/T_Modern_Concrete_N.T_Modern_Concrete_N"),
    # Modernist Ribbon Glazing & Glass Doors
    ("MI_Modern_RibbonWindow", "/Game/SparkVision/Textures/T_Ribbon_Window_D.T_Ribbon_Window_D", "/Game/SparkVision/Textures/T_Ribbon_Window_N.T_Ribbon_Window_N"),
    ("MI_Modern_GlassDoor", "/Game/SparkVision/Textures/T_Ribbon_Window_D.T_Ribbon_Window_D", "/Game/SparkVision/Textures/T_Ribbon_Window_N.T_Ribbon_Window_N"),
    # Debdaru Weeping Mast Trees (Perimeter screening)
    ("MI_Foliage_Debdaru_Dark", "/Game/SparkVision/Textures/T_Debdaru_Leaf_D.T_Debdaru_Leaf_D", "/Game/SparkVision/Textures/T_Debdaru_Leaf_N.T_Debdaru_Leaf_N"),
    # Colonial Cast Iron Gates & Railings
    ("MI_Curzon_CastIron", "/Game/SparkVision/Textures/T_Curzon_CastIron_D.T_Curzon_CastIron_D", "/Game/SparkVision/Textures/T_Curzon_CastIron_N.T_Curzon_CastIron_N"),
    # Campus Roadways (Curzon, Fuller Rd, TSC, Nilkhet)
    ("MI_Primary_Road", "/Game/SparkVision/Textures/T_Road_Asphalt_D.T_Road_Asphalt_D", "/Game/SparkVision/Textures/T_Road_Asphalt_N.T_Road_Asphalt_N"),
    ("MI_Secondary_Road", "/Game/SparkVision/Textures/T_Road_Asphalt_D.T_Road_Asphalt_D", "/Game/SparkVision/Textures/T_Road_Asphalt_N.T_Road_Asphalt_N"),
    # Central Shaheed Minar Marble Altar
    ("MI_Shaheed_Marble", "/Game/SparkVision/Textures/T_Shaheed_Marble_D.T_Shaheed_Marble_D", "/Game/SparkVision/Textures/T_Shaheed_Marble_N.T_Shaheed_Marble_N"),
    # Curzon Pond Water Lilies & Shapla Pads
    ("MI_Foliage_LilyPad", "/Game/SparkVision/Textures/T_WaterLily_Pad_D.T_WaterLily_Pad_D", "/Game/SparkVision/Textures/T_WaterLily_Pad_N.T_WaterLily_Pad_N"),
    # Bamboo Stems & Groves
    ("MI_Stem_BambooGold", "/Game/SparkVision/Textures/T_Bamboo_Leaf_D.T_Bamboo_Leaf_D", "/Game/SparkVision/Textures/T_Bamboo_Leaf_N.T_Bamboo_Leaf_N"),
    # Broadleaf & Palm Foliage
    ("MI_Foliage_PalmFrond", "/Game/SparkVision/Textures/T_Hedge_D.T_Hedge_D", "/Game/SparkVision/Textures/T_Hedge_N.T_Hedge_N"),
    ("MI_Foliage_Banyan_Leaf", "/Game/SparkVision/Textures/T_Hedge_D.T_Hedge_D", "/Game/SparkVision/Textures/T_Hedge_N.T_Hedge_N"),
    ("MI_Foliage_Neem_Green", "/Game/SparkVision/Textures/T_Hedge_D.T_Hedge_D", "/Game/SparkVision/Textures/T_Hedge_N.T_Hedge_N"),
    ("MI_Foliage_Raintree_Leaf", "/Game/SparkVision/Textures/T_Hedge_D.T_Hedge_D", "/Game/SparkVision/Textures/T_Hedge_N.T_Hedge_N"),
    ("MI_Foliage_Fern_Emerald", "/Game/SparkVision/Textures/T_Hedge_D.T_Hedge_D", "/Game/SparkVision/Textures/T_Hedge_N.T_Hedge_N"),
    ("MI_Stem_ReedGreen", "/Game/SparkVision/Textures/T_Hedge_D.T_Hedge_D", "/Game/SparkVision/Textures/T_Hedge_N.T_Hedge_N"),
    ("MI_Ground_LeafLitter_Moist", "/Game/SparkVision/Textures/T_Ground_Grass_D.T_Ground_Grass_D", "/Game/SparkVision/Textures/T_Ground_Grass_N.T_Ground_Grass_N"),
    ("MI_Curzon_Brass", "/Game/SparkVision/Textures/T_Curzon_Sandstone_D.T_Curzon_Sandstone_D", "/Game/SparkVision/Textures/T_Curzon_Sandstone_N.T_Curzon_Sandstone_N"),
]

def main():
    print("=" * 60)
    print("UPGRADING REMAINING MATERIAL INSTANCES TO WWM MASTER PBR")
    print("=" * 60)

    success_count = 0
    for mi_name, diffuse_path, normal_path in MAPPINGS:
        mi_ref = f"/Game/SparkVision/Materials/{mi_name}.{mi_name}"
        print(f"\nConfiguring {mi_name}...")
        try:
            # Set parent to Master PBR
            invoke_tool("set_parent", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
                "instance": {"refPath": mi_ref},
                "parent": {"refPath": MASTER_PBR}
            })
            print(f"  ✓ Parented to {MASTER_PBR}")

            # Assign Diffuse Texture
            invoke_tool("set_texture_parameter", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
                "instance": {"refPath": mi_ref},
                "name": "BaseColor_Texture",
                "value": {"refPath": diffuse_path}
            })
            print(f"  ✓ BaseColor: {diffuse_path.split('.')[-1]}")

            # Assign Normal Texture
            invoke_tool("set_texture_parameter", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
                "instance": {"refPath": mi_ref},
                "name": "Normal_Texture",
                "value": {"refPath": normal_path}
            })
            print(f"  ✓ Normal: {normal_path.split('.')[-1]}")

            success_count += 1
        except Exception as e:
            print(f"  ✗ Error configuring {mi_name}: {e}")

    # Save all modified materials
    try:
        paths = [f"/Game/SparkVision/Materials/{m[0]}" for m in MAPPINGS]
        invoke_tool("save_assets", "editor_toolset.toolsets.asset.AssetTools", {
            "asset_paths": paths
        })
        print(f"\n✅ Successfully upgraded and saved {success_count}/{len(MAPPINGS)} materials!")
    except Exception as e:
        print(f"Notice saving assets: {e}")

if __name__ == "__main__":
    main()
