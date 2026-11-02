#!/usr/bin/env python3
"""
Import WWM Heritage Props and Flora FBXs into Unreal Engine
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

SOURCE_DIR = "/Users/atiaoishi/Downloads/sparkvision/SourceAssets/Models"

IMPORTS = [
    ("/Game/SparkVision/Campus", "SM_ArchiveTerminal", os.path.join(SOURCE_DIR, "SM_ArchiveTerminal.fbx")),
    ("/Game/SparkVision/Campus/Environment", "SM_Curzon_Lantern", os.path.join(SOURCE_DIR, "SM_Curzon_Lantern.fbx")),
    ("/Game/SparkVision/Campus/Environment", "SM_Pond_WaterLily_Cluster", os.path.join(SOURCE_DIR, "SM_Pond_WaterLily_Cluster.fbx")),
    ("/Game/SparkVision/Campus/Environment", "SM_Tree_Krishnachura_Bloom", os.path.join(SOURCE_DIR, "SM_Tree_Krishnachura_Bloom.fbx")),
]

def main():
    print("=" * 60)
    print("IMPORTING WWM HERITAGE PROPS & FLORA FBXs")
    print("=" * 60)

    for folder, asset_name, fbx_path in IMPORTS:
        print(f"\nImporting {asset_name} into {folder}...")
        try:
            res = invoke_tool("import_file", "editor_toolset.toolsets.static_mesh.StaticMeshTools", {
                "folder_path": folder,
                "asset_name": asset_name,
                "source_file": fbx_path,
                "import_materials": False,
                "import_textures": False,
                "combine_meshes": True
            })
            print(f"  ✓ Successfully imported {asset_name}: {res}")
        except Exception as e:
            print(f"  ✗ Import error for {asset_name}: {e}")

    # Now let's assign the PBR materials to the imported static meshes
    # 1. SM_ArchiveTerminal -> MI_ArchiveTerminal (or MI_Curzon_Brass / Sandstone)
    # Let's create MI_ArchiveTerminal derived from M_SparkVision_Master_PBR
    print("\nConfiguring MI_ArchiveTerminal material...")
    try:
        invoke_tool("create", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
            "folder_path": "/Game/SparkVision/Materials",
            "asset_name": "MI_ArchiveTerminal",
            "parent": {"refPath": "/Game/SparkVision/Materials/M_SparkVision_Master_PBR.M_SparkVision_Master_PBR"}
        })
    except Exception as e:
        print(f"  Notice creating MI_ArchiveTerminal: {e}")

    try:
        invoke_tool("set_texture_parameter", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
            "instance": {"refPath": "/Game/SparkVision/Materials/MI_ArchiveTerminal.MI_ArchiveTerminal"},
            "name": "BaseColor_Texture",
            "value": {"refPath": "/Game/SparkVision/Textures/T_ArchivePedestal_D.T_ArchivePedestal_D"}
        })
        invoke_tool("set_texture_parameter", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
            "instance": {"refPath": "/Game/SparkVision/Materials/MI_ArchiveTerminal.MI_ArchiveTerminal"},
            "name": "Normal_Texture",
            "value": {"refPath": "/Game/SparkVision/Textures/T_ArchivePedestal_N.T_ArchivePedestal_N"}
        })
        print("  ✓ Configured MI_ArchiveTerminal with PBR maps")
    except Exception as e:
        print(f"  ✗ Error setting params on MI_ArchiveTerminal: {e}")

    # Set static mesh materials
    mesh_mats = [
        ("/Game/SparkVision/Campus/SM_ArchiveTerminal.SM_ArchiveTerminal", "/Game/SparkVision/Materials/MI_ArchiveTerminal.MI_ArchiveTerminal"),
        ("/Game/SparkVision/Campus/Environment/SM_Curzon_Lantern.SM_Curzon_Lantern", "/Game/SparkVision/Materials/MI_Curzon_Brass.MI_Curzon_Brass"),
        ("/Game/SparkVision/Campus/Environment/SM_Pond_WaterLily_Cluster.SM_Pond_WaterLily_Cluster", "/Game/SparkVision/Materials/MI_Ground_Grass.MI_Ground_Grass"),
        ("/Game/SparkVision/Campus/Environment/SM_Tree_Krishnachura_Bloom.SM_Tree_Krishnachura_Bloom", "/Game/SparkVision/Materials/MI_Foliage_Krishnachura_Red.MI_Foliage_Krishnachura_Red"),
    ]

    for mesh_path, mat_path in mesh_mats:
        try:
            # Set on StaticMaterials[0].materialInterface
            values = {
                "StaticMaterials": [
                    {
                        "materialInterface": {"refPath": mat_path}
                    }
                ]
            }
            import json
            invoke_tool("set_properties", "editor_toolset.toolsets.object.ObjectTools", {
                "instance": {"refPath": mesh_path},
                "values": json.dumps(values)
            })
            print(f"  ✓ Set material {mat_path} on {mesh_path}")
        except Exception as e:
            print(f"  Notice setting mesh material: {e}")

    # Save assets
    try:
        invoke_tool("save_assets", "editor_toolset.toolsets.asset.AssetTools", {
            "asset_paths": [
                "/Game/SparkVision/Campus/SM_ArchiveTerminal",
                "/Game/SparkVision/Campus/Environment/SM_Curzon_Lantern",
                "/Game/SparkVision/Campus/Environment/SM_Pond_WaterLily_Cluster",
                "/Game/SparkVision/Campus/Environment/SM_Tree_Krishnachura_Bloom",
                "/Game/SparkVision/Materials/MI_ArchiveTerminal"
            ]
        })
        print("\n✅ All imported assets saved successfully!")
    except Exception as e:
        print(f"Notice saving assets: {e}")

if __name__ == "__main__":
    main()
