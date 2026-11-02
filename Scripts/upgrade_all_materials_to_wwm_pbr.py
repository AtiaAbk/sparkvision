#!/usr/bin/env python3
"""
Upgrade all architectural and campus Material Instances to M_SparkVision_Master_PBR
with authentic Where Winds Meet high-fidelity PBR textures.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

MASTER_PBR = "/Game/SparkVision/Materials/M_SparkVision_Master_PBR.M_SparkVision_Master_PBR"

MAPPINGS = [
    # Sandstone steps, plinths, cornices
    ("MI_Curzon_Sandstone", "/Game/SparkVision/Textures/T_Curzon_Sandstone_D.T_Curzon_Sandstone_D", "/Game/SparkVision/Textures/T_Curzon_Sandstone_N.T_Curzon_Sandstone_N"),
    # Historic lime plaster white jali & trim
    ("MI_Curzon_WhiteTrim", "/Game/SparkVision/Textures/T_Curzon_WhiteTrim_D.T_Curzon_WhiteTrim_D", "/Game/SparkVision/Textures/T_Curzon_WhiteTrim_N.T_Curzon_WhiteTrim_N"),
    # Colonial dark teak & mahogany doors
    ("MI_Curzon_WoodDark", "/Game/SparkVision/Textures/T_Curzon_WoodDark_D.T_Curzon_WoodDark_D", "/Game/SparkVision/Textures/T_Curzon_WoodDark_N.T_Curzon_WoodDark_N"),
    # Louvers & window shutters
    ("MI_Curzon_Louvers", "/Game/SparkVision/Textures/T_Curzon_WoodDark_D.T_Curzon_WoodDark_D", "/Game/SparkVision/Textures/T_Curzon_WoodDark_N.T_Curzon_WoodDark_N"),
    # Terracotta clay barrel roof tiles
    ("MI_Curzon_RoofTile", "/Game/SparkVision/Textures/T_Curzon_RoofTiles_D.T_Curzon_RoofTiles_D", "/Game/SparkVision/Textures/T_Curzon_RoofTiles_N.T_Curzon_RoofTiles_N"),
    ("MI_Curzon_Tiles", "/Game/SparkVision/Textures/T_Curzon_RoofTiles_D.T_Curzon_RoofTiles_D", "/Game/SparkVision/Textures/T_Curzon_RoofTiles_N.T_Curzon_RoofTiles_N"),
    # Modernist concrete fins & facades
    ("MI_Modern_ConcreteFin", "/Game/SparkVision/Textures/T_Modern_Concrete_D.T_Modern_Concrete_D", "/Game/SparkVision/Textures/T_Modern_Concrete_N.T_Modern_Concrete_N"),
]

def main():
    print("=" * 60)
    print("UPGRADING MATERIAL INSTANCES TO WWM MASTER PBR")
    print("=" * 60)

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
            print(f"  ✓ BaseColor: {diffuse_path}")

            # Assign Normal Texture
            invoke_tool("set_texture_parameter", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
                "instance": {"refPath": mi_ref},
                "name": "Normal_Texture",
                "value": {"refPath": normal_path}
            })
            print(f"  ✓ Normal: {normal_path}")

        except Exception as e:
            print(f"  ✗ Error configuring {mi_name}: {e}")

    # Save all modified materials
    try:
        paths = [f"/Game/SparkVision/Materials/{m[0]}" for m in MAPPINGS]
        invoke_tool("save_assets", "editor_toolset.toolsets.asset.AssetTools", {
            "asset_paths": paths
        })
        print("\n✅ Saved all upgraded material assets!")
    except Exception as e:
        print(f"Notice saving assets: {e}")

if __name__ == "__main__":
    main()
