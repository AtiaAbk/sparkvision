#!/usr/bin/env python3
"""
Imports equipment textures and configures Material Instances for Climax Cadre Squad:
- MI_Cadre_NoukaCap (Nouka Boat badge on cap)
- MI_Cadre_Helmet (Black motorcycle helmet with visor)
- MI_Bamboo_Lathi (Bamboo stick weapon)
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

MASTER_PBR = "/Game/SparkVision/Materials/M_SparkVision_Master_PBR.M_SparkVision_Master_PBR"
TEX_DIR = "/Users/atiaoishi/Downloads/sparkvision/Content/SparkVision/Textures"
MAT_FOLDER = "/Game/SparkVision/Materials"
TEX_FOLDER = "/Game/SparkVision/Textures"

TEXTURES_TO_IMPORT = [
    ("T_Cadre_NoukaCap_D", f"{TEX_DIR}/T_Cadre_NoukaCap_D.png"),
    ("T_Cadre_Helmet_D", f"{TEX_DIR}/T_Cadre_Helmet_D.png"),
    ("T_Bamboo_Lathi_D", f"{TEX_DIR}/T_Bamboo_Lathi_D.png"),
    ("T_Bamboo_Lathi_N", f"{TEX_DIR}/T_Bamboo_Lathi_N.png"),
]

CADRE_MATERIALS = [
    {
        "name": "MI_Cadre_NoukaCap",
        "diffuse": f"{TEX_FOLDER}/T_Cadre_NoukaCap_D.T_Cadre_NoukaCap_D",
        "normal": None
    },
    {
        "name": "MI_Cadre_Helmet",
        "diffuse": f"{TEX_FOLDER}/T_Cadre_Helmet_D.T_Cadre_Helmet_D",
        "normal": None
    },
    {
        "name": "MI_Bamboo_Lathi",
        "diffuse": f"{TEX_FOLDER}/T_Bamboo_Lathi_D.T_Bamboo_Lathi_D",
        "normal": f"{TEX_FOLDER}/T_Bamboo_Lathi_N.T_Bamboo_Lathi_N"
    }
]

def main():
    print("=" * 70)
    print("IMPORTING CADRE EQUIPMENT TEXTURES & SETTING UP MATERIAL INSTANCES")
    print("=" * 70)

    # 1. Import textures
    for asset_name, src_path in TEXTURES_TO_IMPORT:
        if not os.path.exists(src_path):
            print(f"Missing texture source: {src_path}")
            continue

        print(f"Importing texture: {asset_name}...")
        try:
            invoke_tool("import_file", "editor_toolset.toolsets.texture.TextureTools", {
                "folder_path": TEX_FOLDER,
                "asset_name": asset_name,
                "source_file": src_path
            })
            print(f"  ✓ Imported: {TEX_FOLDER}/{asset_name}")
        except Exception as e:
            print(f"  Notice during import {asset_name}: {e}")

    # 2. Create and configure Material Instances
    for mat in CADRE_MATERIALS:
        name = mat["name"]
        mi_ref = f"{MAT_FOLDER}/{name}.{name}"
        print(f"\nSetting up Material Instance: {name}...")

        exists = invoke_tool("exists", "editor_toolset.toolsets.asset.AssetTools", {
            "path": f"{MAT_FOLDER}/{name}"
        }).get("returnValue", False)

        if not exists:
            print(f"  Creating {name}...")
            try:
                invoke_tool("create", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
                    "folder_path": MAT_FOLDER,
                    "asset_name": name,
                    "parent": {"refPath": MASTER_PBR}
                })
            except Exception as e:
                print(f"  Create notice: {e}")
        else:
            try:
                invoke_tool("set_parent", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
                    "instance": {"refPath": mi_ref},
                    "parent": {"refPath": MASTER_PBR}
                })
            except Exception as e:
                print(f"  Set parent notice: {e}")

        # Set Diffuse
        if mat["diffuse"]:
            try:
                invoke_tool("set_texture_parameter", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
                    "instance": {"refPath": mi_ref},
                    "name": "BaseColor_Texture",
                    "value": {"refPath": mat["diffuse"]}
                })
                print(f"  ✓ BaseColor_Texture set to {mat['diffuse']}")
            except Exception as e:
                print(f"  Diffuse error: {e}")

        # Set Normal
        if mat["normal"]:
            try:
                invoke_tool("set_texture_parameter", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
                    "instance": {"refPath": mi_ref},
                    "name": "Normal_Texture",
                    "value": {"refPath": mat["normal"]}
                })
                print(f"  ✓ Normal_Texture set to {mat['normal']}")
            except Exception as e:
                print(f"  Normal error: {e}")

    # 3. Save all dirty assets
    try:
        invoke_tool("save_assets", "editor_toolset.toolsets.asset.AssetTools", {
            "asset_paths": []
        })
        print("\n✅ Successfully saved all cadre assets to disk!")
    except Exception as e:
        print(f"Save notice: {e}")

if __name__ == "__main__":
    main()
