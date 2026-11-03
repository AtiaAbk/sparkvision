#!/usr/bin/env python3
"""
Assigns authentic architectural facade materials (doors, windows, arches, louvers)
directly to the material slots of the Static Mesh assets across Dhaka University.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

MAT_CURZON = "/Game/SparkVision/Materials/MI_Curzon_Facade_ArchedDoorsWindows.MI_Curzon_Facade_ArchedDoorsWindows"
MAT_KALA = "/Game/SparkVision/Materials/MI_KalaBhaban_ModernistFacade.MI_KalaBhaban_ModernistFacade"
MAT_TSC = "/Game/SparkVision/Materials/MI_TSC_ModernistFacade.MI_TSC_ModernistFacade"
MAT_SKYLINE = "/Game/SparkVision/Materials/MI_ModernSkyline_CurtainWall.MI_ModernSkyline_CurtainWall"

ASSIGNMENTS = [
    # Curzon Modular Meshes
    {
        "mesh": "/Game/SparkVision/Campus/CurzonModular/SM_Curzon_Tower_Octagon.SM_Curzon_Tower_Octagon",
        "slots": {
            "M_Curzon_WhiteTrim": MAT_CURZON,
            "M_Curzon_Sandstone": MAT_CURZON,
            "M_Curzon_Brick": MAT_CURZON
        }
    },
    {
        "mesh": "/Game/SparkVision/Campus/CurzonModular/SM_Curzon_Entrance_Portal.SM_Curzon_Entrance_Portal",
        "slots": {
            "M_Curzon_WhiteTrim": MAT_CURZON,
            "M_Curzon_Brick": MAT_CURZON
        }
    },
    {
        "mesh": "/Game/SparkVision/Campus/CurzonModular/SM_Curzon_Veranda_Arch_Upper.SM_Curzon_Veranda_Arch_Upper",
        "slots": {
            "M_Curzon_WhiteTrim": MAT_CURZON,
            "M_Curzon_Brick": MAT_CURZON
        }
    },
    {
        "mesh": "/Game/SparkVision/Campus/CurzonModular/SM_Curzon_Veranda_Arch_Lower.SM_Curzon_Veranda_Arch_Lower",
        "slots": {
            "M_Curzon_WhiteTrim": MAT_CURZON,
            "M_Curzon_Brick": MAT_CURZON
        }
    },
    {
        "mesh": "/Game/SparkVision/Campus/SM_CurzonHall.SM_CurzonHall",
        "slots": {
            "Material_0": MAT_CURZON
        }
    },
    # Kala Bhaban Faculty of Arts
    {
        "mesh": "/Game/SparkVision/Campus/Landmarks/SM_KalaBhaban.SM_KalaBhaban",
        "slots": {
            "M_Curzon_Brick": MAT_KALA,
            "M_Hero_Modern": MAT_KALA
        }
    },
    # TSC Complex
    {
        "mesh": "/Game/SparkVision/Campus/Landmarks/SM_TSC_Building.SM_TSC_Building",
        "slots": {
            "M_Hero_Modern": MAT_TSC,
            "M_Curzon_Accent": MAT_TSC
        }
    },
    # Central Library
    {
        "mesh": "/Game/SparkVision/Campus/Landmarks/SM_CentralLibrary.SM_CentralLibrary",
        "slots": {
            "M_Supporting_Building": MAT_KALA,
            "M_Hero_Modern": MAT_KALA
        }
    },
    # Modern Skyline Towers
    {
        "mesh": "/Game/SparkVision/Campus/ModernSkyline/SM_Modern_Building_Commercial.SM_Modern_Building_Commercial",
        "slots": {
            "M_Modern_Wall": MAT_SKYLINE
        }
    },
    {
        "mesh": "/Game/SparkVision/Campus/ModernSkyline/SM_Modern_Tower_Glass.SM_Modern_Tower_Glass",
        "slots": {
            "M_Modern_Glass": MAT_SKYLINE
        }
    }
]

def main():
    print("=" * 70)
    print("ASSIGNING AUTHENTIC ARCHITECTURAL FACADES TO STATIC MESH SLOTS")
    print("=" * 70)

    for item in ASSIGNMENTS:
        mesh_ref = item["mesh"]
        mesh_name = mesh_ref.split(".")[-1]
        print(f"\nProcessing Mesh: {mesh_name}...")

        # Get existing slots
        try:
            available_slots = invoke_tool("get_material_slots", "editor_toolset.toolsets.static_mesh.StaticMeshTools", {
                "mesh": {"refPath": mesh_ref}
            }).get("returnValue", [])
        except Exception as e:
            print(f"  Cannot query slots: {e}")
            continue

        for slot_name, mat_ref in item["slots"].items():
            if slot_name in available_slots:
                try:
                    res = invoke_tool("set_material", "editor_toolset.toolsets.static_mesh.StaticMeshTools", {
                        "mesh": {"refPath": mesh_ref},
                        "slot_name": slot_name,
                        "material": {"refPath": mat_ref}
                    })
                    print(f"  ✓ Slot '{slot_name}' -> {mat_ref.split('.')[-1]}")
                except Exception as e:
                    print(f"  ✗ Failed to set '{slot_name}': {e}")
            else:
                print(f"  (Slot '{slot_name}' not in {available_slots})")

    # Save all modified static mesh assets
    try:
        invoke_tool("save_assets", "editor_toolset.toolsets.asset.AssetTools", {
            "asset_paths": []
        })
        print("\n✅ Successfully saved all modified static mesh assets!")
    except Exception as e:
        print(f"Save notice: {e}")

if __name__ == "__main__":
    main()
