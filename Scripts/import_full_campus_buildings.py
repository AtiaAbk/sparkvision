#!/usr/bin/env python3
"""
Imports Full Campus Architectural Assets into Unreal Engine 5.8
via Unreal MCP, assigns PBR materials, generates collisions, and saves assets.
"""

import os
import json
import subprocess

MODELS_DIR = "/Users/atiaoishi/Downloads/sparkvision/SourceAssets/Models"
LANDMARKS_FOLDER = "/Game/SparkVision/Campus/Landmarks"
MAT_FOLDER = "/Game/SparkVision/Materials"

BUILDING_IMPORTS = [
    {
        "name": "SM_KalaBhaban",
        "file": "SM_KalaBhaban.fbx",
        "folder": LANDMARKS_FOLDER,
        "slots": {
            "M_Hero_Modern": f"{MAT_FOLDER}/MI_Hero_Modern.MI_Hero_Modern",
            "M_Curzon_Brick": f"{MAT_FOLDER}/MI_Curzon_Brick.MI_Curzon_Brick",
            "M_Curzon_StonePaving": f"{MAT_FOLDER}/MI_Curzon_StonePaving.MI_Curzon_StonePaving"
        }
    },
    {
        "name": "SM_CentralMosque",
        "file": "SM_CentralMosque.fbx",
        "folder": LANDMARKS_FOLDER,
        "slots": {
            "M_Shaheed_Marble": f"{MAT_FOLDER}/MI_Shaheed_Marble.MI_Shaheed_Marble",
            "M_Curzon_WhiteTrim": f"{MAT_FOLDER}/MI_Curzon_WhiteTrim.MI_Curzon_WhiteTrim",
            "M_Curzon_StonePaving": f"{MAT_FOLDER}/MI_Curzon_StonePaving.MI_Curzon_StonePaving"
        }
    },
    {
        "name": "SM_SalimullahMuslim_Hall",
        "file": "SM_SalimullahMuslim_Hall.fbx",
        "folder": LANDMARKS_FOLDER,
        "slots": {
            "M_Curzon_Brick": f"{MAT_FOLDER}/MI_Curzon_Brick.MI_Curzon_Brick",
            "M_Curzon_WhiteTrim": f"{MAT_FOLDER}/MI_Curzon_WhiteTrim.MI_Curzon_WhiteTrim",
            "M_Curzon_RoofTile": f"{MAT_FOLDER}/MI_Curzon_RoofTile.MI_Curzon_RoofTile",
            "M_Curzon_StonePaving": f"{MAT_FOLDER}/MI_Curzon_StonePaving.MI_Curzon_StonePaving"
        }
    },
    {
        "name": "SM_Shahidullah_Hall",
        "file": "SM_Shahidullah_Hall.fbx",
        "folder": LANDMARKS_FOLDER,
        "slots": {
            "M_Curzon_Brick": f"{MAT_FOLDER}/MI_Curzon_Brick.MI_Curzon_Brick",
            "M_Curzon_WhiteTrim": f"{MAT_FOLDER}/MI_Curzon_WhiteTrim.MI_Curzon_WhiteTrim",
            "M_Curzon_StonePaving": f"{MAT_FOLDER}/MI_Curzon_StonePaving.MI_Curzon_StonePaving"
        }
    },
    {
        "name": "SM_Curzon_ScienceAnnex",
        "file": "SM_Curzon_ScienceAnnex.fbx",
        "folder": LANDMARKS_FOLDER,
        "slots": {
            "M_Curzon_Brick": f"{MAT_FOLDER}/MI_Curzon_Brick.MI_Curzon_Brick",
            "M_Curzon_WhiteTrim": f"{MAT_FOLDER}/MI_Curzon_WhiteTrim.MI_Curzon_WhiteTrim",
            "M_Curzon_StonePaving": f"{MAT_FOLDER}/MI_Curzon_StonePaving.MI_Curzon_StonePaving"
        }
    },
    {
        "name": "SM_Jagannath_Hall",
        "file": "SM_Jagannath_Hall.fbx",
        "folder": LANDMARKS_FOLDER,
        "slots": {
            "M_Curzon_Brick": f"{MAT_FOLDER}/MI_Curzon_Brick.MI_Curzon_Brick",
            "M_Curzon_WhiteTrim": f"{MAT_FOLDER}/MI_Curzon_WhiteTrim.MI_Curzon_WhiteTrim",
            "M_Curzon_StonePaving": f"{MAT_FOLDER}/MI_Curzon_StonePaving.MI_Curzon_StonePaving"
        }
    },
    {
        "name": "SM_Rokeya_Hall",
        "file": "SM_Rokeya_Hall.fbx",
        "folder": LANDMARKS_FOLDER,
        "slots": {
            "M_Curzon_Brick": f"{MAT_FOLDER}/MI_Curzon_Brick.MI_Curzon_Brick",
            "M_Curzon_WhiteTrim": f"{MAT_FOLDER}/MI_Curzon_WhiteTrim.MI_Curzon_WhiteTrim",
            "M_Curzon_StonePaving": f"{MAT_FOLDER}/MI_Curzon_StonePaving.MI_Curzon_StonePaving"
        }
    },
    {
        "name": "SM_SurjaSen_Hall",
        "file": "SM_SurjaSen_Hall.fbx",
        "folder": LANDMARKS_FOLDER,
        "slots": {
            "M_Supporting_Building": f"{MAT_FOLDER}/MI_Supporting_Building.MI_Supporting_Building",
            "M_Hero_Modern": f"{MAT_FOLDER}/MI_Hero_Modern.MI_Hero_Modern",
            "M_Curzon_Brick": f"{MAT_FOLDER}/MI_Curzon_Brick.MI_Curzon_Brick"
        }
    },
    {
        "name": "SM_Admin_Building",
        "file": "SM_Admin_Building.fbx",
        "folder": LANDMARKS_FOLDER,
        "slots": {
            "M_Hero_Modern": f"{MAT_FOLDER}/MI_Hero_Modern.MI_Hero_Modern",
            "M_Supporting_Building": f"{MAT_FOLDER}/MI_Supporting_Building.MI_Supporting_Building",
            "M_Curzon_StonePaving": f"{MAT_FOLDER}/MI_Curzon_StonePaving.MI_Curzon_StonePaving"
        }
    },
    {
        "name": "SM_IBA_Building",
        "file": "SM_IBA_Building.fbx",
        "folder": LANDMARKS_FOLDER,
        "slots": {
            "M_Curzon_Brick": f"{MAT_FOLDER}/MI_Curzon_Brick.MI_Curzon_Brick",
            "M_Hero_Modern": f"{MAT_FOLDER}/MI_Hero_Modern.MI_Hero_Modern",
            "M_Curzon_StonePaving": f"{MAT_FOLDER}/MI_Curzon_StonePaving.MI_Curzon_StonePaving"
        }
    },
    {
        "name": "SM_BanglaAcademy",
        "file": "SM_BanglaAcademy.fbx",
        "folder": LANDMARKS_FOLDER,
        "slots": {
            "M_Curzon_WhiteTrim": f"{MAT_FOLDER}/MI_Curzon_WhiteTrim.MI_Curzon_WhiteTrim",
            "M_Curzon_Brick": f"{MAT_FOLDER}/MI_Curzon_Brick.MI_Curzon_Brick",
            "M_Curzon_StonePaving": f"{MAT_FOLDER}/MI_Curzon_StonePaving.MI_Curzon_StonePaving"
        }
    },
    {
        "name": "SM_Campus_BoundaryWall",
        "file": "SM_Campus_BoundaryWall.fbx",
        "folder": LANDMARKS_FOLDER,
        "slots": {
            "M_Curzon_Brick": f"{MAT_FOLDER}/MI_Curzon_Brick.MI_Curzon_Brick",
            "M_Curzon_CastIron": f"{MAT_FOLDER}/MI_Curzon_CastIron.MI_Curzon_CastIron",
            "M_Curzon_WhiteTrim": f"{MAT_FOLDER}/MI_Curzon_WhiteTrim.MI_Curzon_WhiteTrim"
        }
    },
    {
        "name": "SM_Campus_Skyline",
        "file": "SM_Campus_Skyline.fbx",
        "folder": LANDMARKS_FOLDER,
        "slots": {
            "M_Supporting_Building": f"{MAT_FOLDER}/MI_Supporting_Building.MI_Supporting_Building",
            "M_Hero_Modern": f"{MAT_FOLDER}/MI_Hero_Modern.MI_Hero_Modern"
        }
    }
]

def run_mcp(toolset, tool, args):
    res = subprocess.check_output([
        "/Users/atiaoishi/Downloads/sparkvision/Scripts/mcp_client.py",
        "call", toolset, tool, json.dumps(args)
    ])
    return json.loads(res) if res.strip() else {}

print("=" * 70)
print("STARTING FULL CAMPUS ASSET IMPORT PIPELINE...")
print("=" * 70)

saved_asset_paths = []
for item in BUILDING_IMPORTS:
    name = item["name"]
    folder = item["folder"]
    src_file = os.path.join(MODELS_DIR, item["file"])
    mesh_ref = f"{folder}/{name}.{name}"

    if not os.path.exists(src_file):
        print(f"Skipping {name}: file {src_file} does not exist")
        continue

    print(f"\n--- Importing {name} ---")
    try:
        res = run_mcp(
            "editor_toolset.toolsets.static_mesh.StaticMeshTools",
            "import_file",
            {
                "folder_path": folder,
                "asset_name": name,
                "source_file": src_file,
                "import_materials": False,
                "import_textures": False,
                "combine_meshes": True
            }
        )
        print(f"Imported: {res}")
        saved_asset_paths.append(mesh_ref)
    except Exception as e:
        print(f"Error importing {name}: {e}")

    # Inspect material slots
    try:
        slots_res = run_mcp(
            "editor_toolset.toolsets.static_mesh.StaticMeshTools",
            "get_material_slots",
            {"mesh": {"refPath": mesh_ref}}
        )
        avail_slots = slots_res.get("returnValue", [])
        print(f"Slots found on {name}: {avail_slots}")

        for slot_name, mat_path in item["slots"].items():
            matched_slot = None
            for s in avail_slots:
                if slot_name.lower() in s.lower():
                    matched_slot = s
                    break
            if not matched_slot and avail_slots:
                # If only one or slot order matches
                matched_slot = avail_slots[0]

            if matched_slot:
                print(f"Assigning {mat_path} to slot '{matched_slot}' on {name}...")
                run_mcp(
                    "editor_toolset.toolsets.static_mesh.StaticMeshTools",
                    "set_material",
                    {
                        "mesh": {"refPath": mesh_ref},
                        "slot_name": matched_slot,
                        "material": {"refPath": mat_path}
                    }
                )
    except Exception as e:
        print(f"Error setting materials for {name}: {e}")

    # Generate convex collisions
    try:
        print(f"Generating convex collisions for {name}...")
        run_mcp(
            "editor_toolset.toolsets.static_mesh.StaticMeshTools",
            "generate_convex_collisions",
            {
                "mesh": {"refPath": mesh_ref},
                "hull_count": 8,
                "max_hull_verts": 24,
                "hull_precision": 100000
            }
        )
    except Exception as e:
        print(f"Error generating collisions for {name}: {e}")

# Save all imported assets
print("\nSaving imported assets to disk...")
for asset in saved_asset_paths:
    try:
        run_mcp(
            "editor_toolset.toolsets.asset.AssetTools",
            "save_asset",
            {"asset": {"refPath": asset}}
        )
        print(f"Saved {asset}")
    except Exception as e:
        print(f"Error saving {asset}: {e}")

print("\n" + "=" * 70)
print("ALL FULL CAMPUS ARCHITECTURAL ASSETS IMPORTED & CONFIGURED!")
print("=" * 70)
