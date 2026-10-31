#!/usr/bin/env python3
"""
Imports Phase 3 Landmark Meshes and Environment Foliage into Unreal Engine 5.8
via Unreal MCP, assigns PBR materials, and saves assets to disk.
"""

import os
import json
import subprocess

MODELS_DIR = "/Users/atiaoishi/Downloads/sparkvision/SourceAssets/Models"
LANDMARKS_FOLDER = "/Game/SparkVision/Campus/Landmarks"
FOLIAGE_FOLDER = "/Game/SparkVision/Campus/Foliage"
MAT_FOLDER = "/Game/SparkVision/Materials"

LANDMARK_IMPORTS = [
    {
        "name": "SM_DoyelMonument",
        "file": "SM_DoyelMonument.fbx",
        "folder": LANDMARKS_FOLDER,
        "slots": {
            "M_Hero_Modern": f"{MAT_FOLDER}/MI_Hero_Modern.MI_Hero_Modern",
            "M_Water_Pond": f"{MAT_FOLDER}/MI_Water_Pond.MI_Water_Pond",
            "M_Curzon_Accent": f"{MAT_FOLDER}/MI_Curzon_CastIron.MI_Curzon_CastIron"
        }
    },
    {
        "name": "SM_ShaheedMinar_Monument",
        "file": "SM_ShaheedMinar_Monument.fbx",
        "folder": LANDMARKS_FOLDER,
        "slots": {
            "M_Shaheed_Marble": f"{MAT_FOLDER}/MI_Shaheed_Marble.MI_Shaheed_Marble",
            "M_Shaheed_Sun": f"{MAT_FOLDER}/MI_Shaheed_Sun.MI_Shaheed_Sun",
            "M_Curzon_StonePaving": f"{MAT_FOLDER}/MI_Curzon_StonePaving.MI_Curzon_StonePaving"
        }
    },
    {
        "name": "SM_NazrulMausoleum",
        "file": "SM_NazrulMausoleum.fbx",
        "folder": LANDMARKS_FOLDER,
        "slots": {
            "M_Shaheed_Marble": f"{MAT_FOLDER}/MI_Shaheed_Marble.MI_Shaheed_Marble",
            "M_Curzon_WhiteTrim": f"{MAT_FOLDER}/MI_Curzon_WhiteTrim.MI_Curzon_WhiteTrim"
        }
    },
    {
        "name": "SM_Campus_Tree_Hero",
        "file": "SM_Campus_Tree_Hero.fbx",
        "folder": FOLIAGE_FOLDER,
        "slots": {
            "M_Curzon_Accent": f"{MAT_FOLDER}/MI_Curzon_CastIron.MI_Curzon_CastIron",
            "M_Ground_Grass": f"{MAT_FOLDER}/MI_Ground_Grass.MI_Ground_Grass"
        }
    },
    {
        "name": "SM_TSC_Building",
        "file": "SM_TSC_Building.fbx",
        "folder": LANDMARKS_FOLDER,
        "slots": {
            "M_Hero_Modern": f"{MAT_FOLDER}/MI_Hero_Modern.MI_Hero_Modern",
            "M_Curzon_StonePaving": f"{MAT_FOLDER}/MI_Curzon_StonePaving.MI_Curzon_StonePaving",
            "M_Curzon_Accent": f"{MAT_FOLDER}/MI_Curzon_CastIron.MI_Curzon_CastIron"
        }
    },
    {
        "name": "SM_RajuSculpture",
        "file": "SM_RajuSculpture.fbx",
        "folder": LANDMARKS_FOLDER,
        "slots": {
            "M_Curzon_StonePaving": f"{MAT_FOLDER}/MI_Curzon_StonePaving.MI_Curzon_StonePaving",
            "M_Hero_Modern": f"{MAT_FOLDER}/MI_Hero_Modern.MI_Hero_Modern"
        }
    },
    {
        "name": "SM_CentralLibrary",
        "file": "SM_CentralLibrary.fbx",
        "folder": LANDMARKS_FOLDER,
        "slots": {
            "M_Supporting_Building": f"{MAT_FOLDER}/MI_Supporting_Building.MI_Supporting_Building",
            "M_Hero_Modern": f"{MAT_FOLDER}/MI_Hero_Modern.MI_Hero_Modern",
            "M_Water_Pond": f"{MAT_FOLDER}/MI_Water_Pond.MI_Water_Pond"
        }
    },
    {
        "name": "SM_AparajeyoBangla",
        "file": "SM_AparajeyoBangla.fbx",
        "folder": LANDMARKS_FOLDER,
        "slots": {
            "M_Curzon_StonePaving": f"{MAT_FOLDER}/MI_Curzon_StonePaving.MI_Curzon_StonePaving",
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

print("Ensuring target folders exist in Unreal Engine...")
for fld in [LANDMARKS_FOLDER, FOLIAGE_FOLDER]:
    try:
        run_mcp("editor_toolset.toolsets.asset.AssetTools", "create_folder", {"path": fld})
    except Exception as e:
        pass

print("\nImporting Phase 3 Landmark & Foliage Meshes...")
saved_asset_paths = []
for item in LANDMARK_IMPORTS:
    name = item["name"]
    folder = item["folder"]
    src_file = os.path.join(MODELS_DIR, item["file"])
    mesh_ref = f"{folder}/{name}.{name}"

    if not os.path.exists(src_file):
        print(f"Skipping {name}: {src_file} does not exist")
        continue

    # Delete existing asset for clean re-import
    try:
        run_mcp("editor_toolset.toolsets.asset.AssetTools", "delete", {"path": mesh_ref})
    except Exception:
        pass

    # Import asset
    print(f"Importing {name}...")
    run_mcp("editor_toolset.toolsets.static_mesh.StaticMeshTools", "import_file", {
        "folder_path": folder,
        "asset_name": name,
        "source_file": src_file,
        "import_materials": False,
        "import_textures": False,
        "combine_meshes": True
    })
    saved_asset_paths.append(mesh_ref)

    # Assign materials to slots
    try:
        slots_res = run_mcp("editor_toolset.toolsets.static_mesh.StaticMeshTools", "get_material_slots", {"mesh": {"refPath": mesh_ref}})
        actual_slots = slots_res.get("returnValue", [])
        print(f"  Slots found on {name}: {actual_slots}")
        for s_name in actual_slots:
            mat = item["slots"].get(s_name, f"{MAT_FOLDER}/MI_Hero_Modern.MI_Hero_Modern")
            run_mcp("editor_toolset.toolsets.static_mesh.StaticMeshTools", "set_material", {
                "mesh": {"refPath": mesh_ref},
                "slot_name": s_name,
                "material": {"refPath": mat}
            })
            print(f"    Assigned {s_name} -> {mat}")
    except Exception as e:
        print(f"  Error setting materials for {name}: {e}")

# Save all newly imported assets
print("\nSaving imported assets to disk...")
try:
    run_mcp("editor_toolset.toolsets.asset.AssetTools", "save_assets", {"asset_paths": saved_asset_paths})
    print("All Phase 3 landmark assets saved successfully!")
except Exception as e:
    print(f"Error saving assets: {e}")

print("\nRebinding StaticMesh references on scene actors...")
actor_mesh_map = {
    "Hero_ShaheedMinar_Monument": f"{LANDMARKS_FOLDER}/SM_ShaheedMinar_Monument.SM_ShaheedMinar_Monument",
    "Hero_DoyelChattar_Monument": f"{LANDMARKS_FOLDER}/SM_DoyelMonument.SM_DoyelMonument",
    "Hero_NazrulIslam_Mausoleum": f"{LANDMARKS_FOLDER}/SM_NazrulMausoleum.SM_NazrulMausoleum",
    "Hero_CentralLibrary_Building": f"{LANDMARKS_FOLDER}/SM_CentralLibrary.SM_CentralLibrary",
    "Hero_AparajeyoBangla_Sculpture": f"{LANDMARKS_FOLDER}/SM_AparajeyoBangla.SM_AparajeyoBangla",
    "Hero_TSC_AuditoriumComplex": f"{LANDMARKS_FOLDER}/SM_TSC_Building.SM_TSC_Building",
    "RajuMemorialSculpture_CustomArtMesh": f"{LANDMARKS_FOLDER}/SM_RajuSculpture.SM_RajuSculpture",
}
for actor_name, m_path in actor_mesh_map.items():
    found = run_mcp("editor_toolset.toolsets.scene.SceneTools", "find_actors", {"name": actor_name, "tag": "", "collision_channels": []})
    for a in found.get("returnValue", []):
        comps = run_mcp("editor_toolset.toolsets.actor.ActorTools", "get_components", {"actor": a})
        for c in comps.get("returnValue", []):
            if "StaticMeshComponent" in c.get("refPath", ""):
                run_mcp("editor_toolset.toolsets.object.ObjectTools", "set_properties", {
                    "instance": c,
                    "values": json.dumps({"StaticMesh": m_path})
                })
                print(f"  Rebound {actor_name} -> {m_path}")

# Also rebind trees
tree_mesh_path = f"{FOLIAGE_FOLDER}/SM_Campus_Tree_Hero.SM_Campus_Tree_Hero"
for i in range(1, 15):
    found = run_mcp("editor_toolset.toolsets.scene.SceneTools", "find_actors", {"name": f"Campus_HeroTree_{i}", "tag": "", "collision_channels": []})
    for a in found.get("returnValue", []):
        comps = run_mcp("editor_toolset.toolsets.actor.ActorTools", "get_components", {"actor": a})
        for c in comps.get("returnValue", []):
            if "StaticMeshComponent" in c.get("refPath", ""):
                run_mcp("editor_toolset.toolsets.object.ObjectTools", "set_properties", {
                    "instance": c,
                    "values": json.dumps({"StaticMesh": tree_mesh_path})
                })
                print(f"  Rebound Campus_HeroTree_{i} -> {tree_mesh_path}")

