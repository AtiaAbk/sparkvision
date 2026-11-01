#!/usr/bin/env python3
"""
Import Curzon Modular Assets (v3) into Unreal Engine 5.5 and map materials by slot name
"""

import os
import json
import subprocess

MODELS_DIR = "/Users/atiaoishi/Downloads/sparkvision/SourceAssets/Models/CurzonModular"
UE_FOLDER = "/Game/SparkVision/Campus/CurzonModular"

ASSETS = [
    "SM_Curzon_Entrance_Portal",
    "SM_Curzon_Veranda_Arch_Lower",
    "SM_Curzon_Veranda_Arch_Upper",
    "SM_Curzon_Parapet_Merlons",
    "SM_Curzon_Tower_Octagon",
    "SM_Curzon_Hedge_Low",
    "SM_Curzon_Sign_Physics"
]

MATERIAL_MAP = {
    "M_Curzon_Brick": "/Game/SparkVision/Materials/MI_Curzon_Brick.MI_Curzon_Brick",
    "M_Curzon_WhiteTrim": "/Game/SparkVision/Materials/MI_Curzon_WhiteTrim.MI_Curzon_WhiteTrim",
    "M_Curzon_WoodDark": "/Game/SparkVision/Materials/MI_Curzon_WoodDark.MI_Curzon_WoodDark",
    "M_Curzon_Louvers": "/Game/SparkVision/Materials/MI_Curzon_Louvers.MI_Curzon_Louvers",
    "M_Curzon_Glass": "/Game/SparkVision/Materials/MI_Curzon_Glass.MI_Curzon_Glass",
    "M_Curzon_Sandstone": "/Game/SparkVision/Materials/MI_Curzon_Sandstone.MI_Curzon_Sandstone",
    "M_Curzon_Brass": "/Game/SparkVision/Materials/MI_Curzon_Brass.MI_Curzon_Brass",
    "M_Curzon_Tiles": "/Game/SparkVision/Materials/MI_Curzon_Tiles.MI_Curzon_Tiles",
    "M_Curzon_CastIron": "/Game/SparkVision/Materials/MI_Curzon_CastIron.MI_Curzon_CastIron",
    "M_Curzon_SignBlue": "/Game/SparkVision/Materials/MI_Curzon_SignBlue.MI_Curzon_SignBlue",
    "M_Curzon_Hedge": "/Game/SparkVision/Materials/MI_Curzon_Hedge.MI_Curzon_Hedge"
}

def run_mcp(toolset, tool, args):
    res = subprocess.check_output([
        "/Users/atiaoishi/Downloads/sparkvision/Scripts/mcp_client.py",
        "call", toolset, tool, json.dumps(args)
    ])
    return json.loads(res) if res.strip() else {}

def main():
    print("=" * 70)
    print("CONFIGURING MATERIALS FOR V3 CURZON MODULAR ARCHITECTURAL ASSETS...")
    print("=" * 70)

    for name in ASSETS:
        mesh_ref = f"{UE_FOLDER}/{name}.{name}"
        src_file = os.path.join(MODELS_DIR, f"{name}.fbx")

        # Import or re-import
        print(f"\nImporting {name} from {src_file}...")
        try:
            run_mcp("editor_toolset.toolsets.asset.AssetTools", "delete", {"path": mesh_ref})
        except Exception:
            pass

        run_mcp("editor_toolset.toolsets.static_mesh.StaticMeshTools", "import_file", {
            "folder_path": UE_FOLDER,
            "asset_name": name,
            "source_file": src_file,
            "import_materials": False,
            "import_textures": False,
            "combine_meshes": True
        })
        print(f"Imported: {mesh_ref}")

        # Query slot names
        slots_res = run_mcp("editor_toolset.toolsets.static_mesh.StaticMeshTools", "get_material_slots", {
            "mesh": {"refPath": mesh_ref}
        })
        slots = slots_res.get("returnValue", slots_res) if isinstance(slots_res, dict) else []
        print(f"  Slots found ({len(slots)}): {slots}")

        for sname in slots:
            mat_ref = MATERIAL_MAP.get(sname)
            if mat_ref:
                try:
                    run_mcp("editor_toolset.toolsets.static_mesh.StaticMeshTools", "set_material", {
                        "mesh": {"refPath": mesh_ref},
                        "slot_name": sname,
                        "material": {"refPath": mat_ref}
                    })
                    print(f"    Slot '{sname}' -> {mat_ref.split('/')[-1]}")
                except Exception as e:
                    print(f"    Error setting slot '{sname}': {e}")
            else:
                print(f"    Warning: No material mapping for slot '{sname}'")

    print("\nAll v3 modular assets successfully imported and textured!")

if __name__ == "__main__":
    main()
