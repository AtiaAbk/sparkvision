#!/usr/bin/env python3
"""
Sets up and binds authentic architectural facade Material Instances in Unreal Engine
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

MASTER_PBR = "/Game/SparkVision/Materials/M_SparkVision_Master_PBR.M_SparkVision_Master_PBR"
MAT_FOLDER = "/Game/SparkVision/Materials"
TEX_FOLDER = "/Game/SparkVision/Textures"

FACADE_MATERIALS = [
    {
        "name": "MI_Curzon_Facade_ArchedDoorsWindows",
        "diffuse": f"{TEX_FOLDER}/T_Curzon_Facade_ArchedDoorsWindows_D.T_Curzon_Facade_ArchedDoorsWindows_D",
        "normal": f"{TEX_FOLDER}/T_Curzon_Facade_ArchedDoorsWindows_N.T_Curzon_Facade_ArchedDoorsWindows_N",
        "roughness": 0.70,
        "metallic": 0.10
    },
    {
        "name": "MI_KalaBhaban_ModernistFacade",
        "diffuse": f"{TEX_FOLDER}/T_KalaBhaban_Facade_ModernistWindows_D.T_KalaBhaban_Facade_ModernistWindows_D",
        "normal": f"{TEX_FOLDER}/T_KalaBhaban_Facade_ModernistWindows_N.T_KalaBhaban_Facade_ModernistWindows_N",
        "roughness": 0.75,
        "metallic": 0.15
    },
    {
        "name": "MI_TSC_ModernistFacade",
        "diffuse": f"{TEX_FOLDER}/T_TSC_Facade_DoxiadisWaffle_D.T_TSC_Facade_DoxiadisWaffle_D",
        "normal": f"{TEX_FOLDER}/T_TSC_Facade_DoxiadisWaffle_N.T_TSC_Facade_DoxiadisWaffle_N",
        "roughness": 0.65,
        "metallic": 0.12
    },
    {
        "name": "MI_ModernSkyline_CurtainWall",
        "diffuse": f"{TEX_FOLDER}/T_ModernSkyline_Facade_CurtainWall_D.T_ModernSkyline_Facade_CurtainWall_D",
        "normal": f"{TEX_FOLDER}/T_ModernSkyline_Facade_CurtainWall_N.T_ModernSkyline_Facade_CurtainWall_N",
        "roughness": 0.18,
        "metallic": 0.85
    },
    # Also update existing key materials so meshes using them immediately get realistic textures
    {
        "name": "MI_Curzon_Brick",
        "diffuse": f"{TEX_FOLDER}/T_Curzon_Facade_ArchedDoorsWindows_D.T_Curzon_Facade_ArchedDoorsWindows_D",
        "normal": f"{TEX_FOLDER}/T_Curzon_Facade_ArchedDoorsWindows_N.T_Curzon_Facade_ArchedDoorsWindows_N",
        "roughness": 0.72,
        "metallic": 0.08
    },
    {
        "name": "MI_Modern_RibbonWindow",
        "diffuse": f"{TEX_FOLDER}/T_KalaBhaban_Facade_ModernistWindows_D.T_KalaBhaban_Facade_ModernistWindows_D",
        "normal": f"{TEX_FOLDER}/T_KalaBhaban_Facade_ModernistWindows_N.T_KalaBhaban_Facade_ModernistWindows_N",
        "roughness": 0.25,
        "metallic": 0.60
    },
    {
        "name": "MI_Modern_Concrete_Sand",
        "diffuse": f"{TEX_FOLDER}/T_KalaBhaban_Facade_ModernistWindows_D.T_KalaBhaban_Facade_ModernistWindows_D",
        "normal": f"{TEX_FOLDER}/T_KalaBhaban_Facade_ModernistWindows_N.T_KalaBhaban_Facade_ModernistWindows_N",
        "roughness": 0.85,
        "metallic": 0.05
    },
    {
        "name": "MI_TSC_WhiteFascia",
        "diffuse": f"{TEX_FOLDER}/T_TSC_Facade_DoxiadisWaffle_D.T_TSC_Facade_DoxiadisWaffle_D",
        "normal": f"{TEX_FOLDER}/T_TSC_Facade_DoxiadisWaffle_N.T_TSC_Facade_DoxiadisWaffle_N",
        "roughness": 0.60,
        "metallic": 0.10
    },
    {
        "name": "MI_Modern_Glass_CurtainWall_Blue",
        "diffuse": f"{TEX_FOLDER}/T_ModernSkyline_Facade_CurtainWall_D.T_ModernSkyline_Facade_CurtainWall_D",
        "normal": f"{TEX_FOLDER}/T_ModernSkyline_Facade_CurtainWall_N.T_ModernSkyline_Facade_CurtainWall_N",
        "roughness": 0.15,
        "metallic": 0.90
    }
]

def main():
    print("=" * 70)
    print("CONFIGURING AUTHENTIC ARCHITECTURAL FACADE MATERIAL INSTANCES")
    print("=" * 70)

    for item in FACADE_MATERIALS:
        name = item["name"]
        mi_ref = f"{MAT_FOLDER}/{name}.{name}"
        print(f"\nProcessing {name}...")

        # 1. Check if asset exists, or create it
        exists = invoke_tool("exists", "editor_toolset.toolsets.asset.AssetTools", {
            "path": f"{MAT_FOLDER}/{name}"
        }).get("returnValue", False)

        if not exists:
            print(f"  Creating new MaterialInstance: {name}")
            try:
                invoke_tool("create", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
                    "folder_path": MAT_FOLDER,
                    "asset_name": name,
                    "parent": {"refPath": MASTER_PBR}
                })
            except Exception as e:
                print(f"  Create notice: {e}")
        else:
            # Set parent to Master PBR
            try:
                invoke_tool("set_parent", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
                    "instance": {"refPath": mi_ref},
                    "parent": {"refPath": MASTER_PBR}
                })
            except Exception as e:
                print(f"  Set parent notice: {e}")

        # 2. Assign Diffuse & Normal textures
        try:
            invoke_tool("set_texture_parameter", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
                "instance": {"refPath": mi_ref},
                "name": "BaseColor_Texture",
                "value": {"refPath": item["diffuse"]}
            })
            print(f"  ✓ Set BaseColor_Texture -> {item['diffuse']}")

            invoke_tool("set_texture_parameter", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
                "instance": {"refPath": mi_ref},
                "name": "Normal_Texture",
                "value": {"refPath": item["normal"]}
            })
            print(f"  ✓ Set Normal_Texture -> {item['normal']}")

            invoke_tool("set_scalar_parameter", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
                "instance": {"refPath": mi_ref},
                "name": "Roughness_Multiplier",
                "value": float(item["roughness"])
            })

            invoke_tool("set_scalar_parameter", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
                "instance": {"refPath": mi_ref},
                "name": "Metallic_Multiplier",
                "value": float(item["metallic"])
            })
            print(f"  ✓ Set Roughness={item['roughness']}, Metallic={item['metallic']}")
        except Exception as e:
            print(f"  ✗ Parameter error on {name}: {e}")

    print("\n✅ All facade material instances configured!")

if __name__ == "__main__":
    main()
