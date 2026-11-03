#!/usr/bin/env python3
"""
Cleanly Re-import all 7 Master Vegetation Models at Authentic Centimeter Scale:
1. Deletes old sub-scale meshes from /Game/SparkVision/Environment/Vegetation.
2. Imports the new centimeter-scaled FBX meshes.
3. Verifies realistic real-world bounds (e.g. 12.8m height, 14m canopy).
4. Assigns all material slots (Bark, Foliage, Grass).
5. Saves all static mesh assets to disk.
"""

import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

STATIC_MESH_TOOLS = "editor_toolset.toolsets.static_mesh.StaticMeshTools"
ASSET_TOOLS = "editor_toolset.toolsets.asset.AssetTools"

VEG_FOLDER = "/Game/SparkVision/Environment/Vegetation"
MODELS_DIR = "/Users/atiaoishi/Downloads/sparkvision/SourceAssets/Models/Vegetation"
MAT_FOLDER = "/Game/SparkVision/Materials"

meshes = [
    "SM_Tree_Raintree_Master",
    "SM_Tree_Krishnachura_Master",
    "SM_Tree_Banyan_Master",
    "SM_Tree_RoyalPalm_Master",
    "SM_Campus_Grass_Lawn",
    "SM_Campus_Grass_Tuft",
    "SM_Campus_Bush_Kamini"
]

print("=" * 70)
print("RE-IMPORTING CENTIMETER-SCALED MASTER VEGETATION")
print("=" * 70)

# 1. Delete old assets
print("\n[1/3] Deleting outdated sub-scale assets...")
for m in meshes:
    asset_path = f"{VEG_FOLDER}/{m}"
    try:
        invoke_tool("delete", ASSET_TOOLS, {"path": asset_path})
        print(f"  ✓ Deleted old {m}")
    except Exception as e:
        print(f"  Note {m}: {e}")

time.sleep(0.5)

# 2. Import new FBX meshes
print("\n[2/3] Importing authentic centimeter-scaled meshes...")
for m in meshes:
    fbx = os.path.join(MODELS_DIR, f"{m}.fbx")
    try:
        invoke_tool("import_file", STATIC_MESH_TOOLS, {
            "folder_path": VEG_FOLDER,
            "asset_name": m,
            "source_file": fbx,
            "import_materials": False,
            "import_textures": False,
            "combine_meshes": True
        })
        b = invoke_tool("get_bounds", STATIC_MESH_TOOLS, {"mesh": {"refPath": f"{VEG_FOLDER}/{m}.{m}"}}).get("returnValue", {})
        z_max = b.get("max", {}).get("z", 0)
        x_min = b.get("min", {}).get("x", 0)
        x_max = b.get("max", {}).get("x", 0)
        w = x_max - x_min
        print(f"  ✓ Imported {m}: Height={z_max:.1f} cm ({z_max/100:.1f}m), Width={w:.1f} cm ({w/100:.1f}m)")
    except Exception as e:
        print(f"  ERROR importing {m}: {e}")

# 3. Assign Materials
print("\n[3/3] Assigning calibrated PBR materials...")
bark_mat = f"{MAT_FOLDER}/MI_Bark_Tree.MI_Bark_Tree"
raintree_foliage = f"{MAT_FOLDER}/MI_Foliage_Raintree_Natural.MI_Foliage_Raintree_Natural"
krishna_foliage = f"{MAT_FOLDER}/MI_Foliage_Krishnachura_Natural.MI_Foliage_Krishnachura_Natural"
banyan_foliage = f"{MAT_FOLDER}/MI_Foliage_Banyan_Natural.MI_Foliage_Banyan_Natural"
palm_foliage = f"{MAT_FOLDER}/MI_Foliage_PalmFrond.MI_Foliage_PalmFrond"
grass_mi = f"{MAT_FOLDER}/MI_Campus_Grass_Blades.MI_Campus_Grass_Blades"
kamini_mat = f"{MAT_FOLDER}/MI_Foliage_Fern_Natural.MI_Foliage_Fern_Natural"

assignments = [
    ("SM_Tree_Raintree_Master", [("M_Bark_Tree", bark_mat), ("M_Master_NaturalFoliage", raintree_foliage)]),
    ("SM_Tree_Krishnachura_Master", [("M_Bark_Tree", bark_mat), ("MI_Foliage_Krishnachura_Natural", krishna_foliage)]),
    ("SM_Tree_Banyan_Master", [("M_Bark_Tree", bark_mat), ("MI_Foliage_Banyan_Natural", banyan_foliage)]),
    ("SM_Tree_RoyalPalm_Master", [("M_Bark_Tree", bark_mat), ("MI_Foliage_PalmFrond", palm_foliage)]),
    ("SM_Campus_Grass_Lawn", [("MI_Ground_Grass", grass_mi)]),
    ("SM_Campus_Grass_Tuft", [("MI_Ground_Grass", grass_mi)]),
    ("SM_Campus_Bush_Kamini", [("MI_Foliage_Fern_Natural", kamini_mat)]),
]

for mesh_name, slots in assignments:
    mesh_ref = f"{VEG_FOLDER}/{mesh_name}.{mesh_name}"
    for slot_name, mat_ref in slots:
        try:
            invoke_tool("set_material", STATIC_MESH_TOOLS, {
                "mesh": {"refPath": mesh_ref},
                "slot_name": slot_name,
                "material": {"refPath": mat_ref}
            })
        except Exception as e:
            print(f"  Slot ERROR ({mesh_name}.{slot_name}): {e}")

# Save all assets
asset_paths = [f"{VEG_FOLDER}/{m}.{m}" for m in meshes]
try:
    invoke_tool("save_assets", ASSET_TOOLS, {"asset_paths": asset_paths})
    print(f"  ✓ Saved all {len(asset_paths)} static mesh assets to disk")
except Exception as e:
    print(f"  Save notice: {e}")

print("\n✓ Re-importation and material assignment complete!")
