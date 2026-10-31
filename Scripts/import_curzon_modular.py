#!/usr/bin/env python3
import os
import json
import subprocess

MODELS_DIR = "/Users/atiaoishi/Downloads/sparkvision/SourceAssets/Models/CurzonModular"
UE_FOLDER = "/Game/SparkVision/Campus/CurzonModular"

ASSETS = [
    {
        "name": "SM_Curzon_Veranda_Arch_Lower",
        "file": "SM_Curzon_Veranda_Arch_Lower.fbx",
        "slots": [
            "/Game/SparkVision/Materials/MI_Curzon_Brick.MI_Curzon_Brick",
            "/Game/SparkVision/Materials/MI_Curzon_WhiteTrim.MI_Curzon_WhiteTrim"
        ]
    },
    {
        "name": "SM_Curzon_Veranda_Arch_Upper",
        "file": "SM_Curzon_Veranda_Arch_Upper.fbx",
        "slots": [
            "/Game/SparkVision/Materials/MI_Curzon_Brick.MI_Curzon_Brick",
            "/Game/SparkVision/Materials/MI_Curzon_WhiteTrim.MI_Curzon_WhiteTrim"
        ]
    },
    {
        "name": "SM_Curzon_Entrance_Portal",
        "file": "SM_Curzon_Entrance_Portal.fbx",
        "slots": [
            "/Game/SparkVision/Materials/MI_Curzon_Brick.MI_Curzon_Brick",
            "/Game/SparkVision/Materials/MI_Curzon_WhiteTrim.MI_Curzon_WhiteTrim"
        ]
    },
    {
        "name": "SM_Curzon_Chattri_Dome",
        "file": "SM_Curzon_Chattri_Dome.fbx",
        "slots": [
            "/Game/SparkVision/Materials/MI_Curzon_RoofTile.MI_Curzon_RoofTile",
            "/Game/SparkVision/Materials/MI_Curzon_WhiteTrim.MI_Curzon_WhiteTrim"
        ]
    },
    {
        "name": "SM_Curzon_Tower_Octagon",
        "file": "SM_Curzon_Tower_Octagon.fbx",
        "slots": [
            "/Game/SparkVision/Materials/MI_Curzon_Brick.MI_Curzon_Brick",
            "/Game/SparkVision/Materials/MI_Curzon_WhiteTrim.MI_Curzon_WhiteTrim"
        ]
    },
    {
        "name": "SM_Curzon_Parapet_Merlons",
        "file": "SM_Curzon_Parapet_Merlons.fbx",
        "slots": [
            "/Game/SparkVision/Materials/MI_Curzon_Brick.MI_Curzon_Brick",
            "/Game/SparkVision/Materials/MI_Curzon_WhiteTrim.MI_Curzon_WhiteTrim"
        ]
    },
    {
        "name": "SM_Curzon_Bench_Colonial",
        "file": "SM_Curzon_Bench_Colonial.fbx",
        "slots": [
            "/Game/SparkVision/Materials/MI_Curzon_CastIron.MI_Curzon_CastIron",
            "/Game/SparkVision/Materials/MI_Curzon_WhiteTrim.MI_Curzon_WhiteTrim"
        ]
    },
    {
        "name": "SM_Curzon_Lamp_Colonial",
        "file": "SM_Curzon_Lamp_Colonial.fbx",
        "slots": [
            "/Game/SparkVision/Materials/MI_Curzon_CastIron.MI_Curzon_CastIron",
            "/Game/SparkVision/Materials/MI_Curzon_WhiteTrim.MI_Curzon_WhiteTrim"
        ]
    }
]

def run_mcp(toolset, tool, args):
    res = subprocess.check_output([
        "/Users/atiaoishi/Downloads/sparkvision/Scripts/mcp_client.py",
        "call", toolset, tool, json.dumps(args)
    ])
    return json.loads(res) if res.strip() else {}

print("Creating folder in Unreal Engine:", UE_FOLDER)
try:
    run_mcp("editor_toolset.toolsets.asset.AssetTools", "create_folder", {"path": UE_FOLDER})
except Exception as e:
    print(f"Folder create status: {e}")

print("Importing modular static meshes...")
for item in ASSETS:
    name = item["name"]
    src_file = os.path.join(MODELS_DIR, item["file"])
    mesh_ref = f"{UE_FOLDER}/{name}.{name}"
    
    # Delete if exists
    try:
        run_mcp("editor_toolset.toolsets.asset.AssetTools", "delete", {"path": mesh_ref})
    except Exception:
        pass

    print(f"Importing {name} from {src_file}...")
    import_res = run_mcp("editor_toolset.toolsets.static_mesh.StaticMeshTools", "import_file", {
        "folder_path": UE_FOLDER,
        "asset_name": name,
        "source_file": src_file,
        "import_materials": False,
        "import_textures": False,
        "combine_meshes": True
    })
    print(f"Imported: {mesh_ref}")

    # Assign materials to slots
    for slot_idx, mat_ref in enumerate(item["slots"]):
        try:
            run_mcp("editor_toolset.toolsets.static_mesh.StaticMeshTools", "set_material", {
                "mesh": {"refPath": mesh_ref},
                "material_index": slot_idx,
                "material": {"refPath": mat_ref}
            })
            print(f"  Slot {slot_idx} -> {mat_ref}")
        except Exception as e:
            print(f"  Error setting slot {slot_idx}: {e}")

print("All modular assets successfully imported and textured!")
