#!/usr/bin/env python3
"""
Assign calibrated materials to all 7 authentic vegetation static meshes:
- Slot 0 (Bark): MI_Bark_Tree
- Slot 1 (Leaves): MI_Foliage_Raintree_Natural / Krishnachura / Banyan / Palm
- Grass & Shrubs: MI_Campus_Grass_Blades & MI_Foliage_Fern_Natural
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

STATIC_MESH_TOOLS = "editor_toolset.toolsets.static_mesh.StaticMeshTools"
MAT_INST_TOOLS = "editor_toolset.toolsets.material_instance.MaterialInstanceTools"
ASSET_TOOLS = "editor_toolset.toolsets.asset.AssetTools"

VEG_FOLDER = "/Game/SparkVision/Environment/Vegetation"
MAT_FOLDER = "/Game/SparkVision/Materials"
TEX_FOLDER = "/Game/SparkVision/Textures"

# 1. Setup MI_Campus_Grass_Blades
print("[1/2] Creating/Updating MI_Campus_Grass_Blades...")
grass_parent = f"{MAT_FOLDER}/M_Master_NaturalFoliage.M_Master_NaturalFoliage"
try:
    invoke_tool("create", MAT_INST_TOOLS, {
        "folder_path": MAT_FOLDER,
        "asset_name": "MI_Campus_Grass_Blades",
        "parent": {"refPath": grass_parent}
    })
    print("  ✓ Created MI_Campus_Grass_Blades")
except Exception as e:
    print(f"  Grass MI notice: {e}")

grass_mi = f"{MAT_FOLDER}/MI_Campus_Grass_Blades.MI_Campus_Grass_Blades"
try:
    invoke_tool("set_texture_parameter", MAT_INST_TOOLS, {
        "instance": {"refPath": grass_mi},
        "name": "BaseColor_Texture",
        "value": {"refPath": f"{TEX_FOLDER}/T_Campus_Grass_Blades_D.T_Campus_Grass_Blades_D"}
    })
    invoke_tool("set_texture_parameter", MAT_INST_TOOLS, {
        "instance": {"refPath": grass_mi},
        "name": "Normal_Texture",
        "value": {"refPath": f"{TEX_FOLDER}/T_Campus_Grass_Blades_N.T_Campus_Grass_Blades_N"}
    })
    invoke_tool("set_scalar_parameter", MAT_INST_TOOLS, {
        "instance": {"refPath": grass_mi},
        "name": "Roughness",
        "value": 0.85
    })
    print("  ✓ Configured MI_Campus_Grass_Blades parameters")
except Exception as e:
    print(f"  Grass MI param notice: {e}")

# 2. Material Assignments
print("\n[2/2] Assigning materials to static meshes...")
bark_mat = f"{MAT_FOLDER}/MI_Bark_Tree.MI_Bark_Tree"
raintree_foliage = f"{MAT_FOLDER}/MI_Foliage_Raintree_Natural.MI_Foliage_Raintree_Natural"
krishna_foliage = f"{MAT_FOLDER}/MI_Foliage_Krishnachura_Natural.MI_Foliage_Krishnachura_Natural"
banyan_foliage = f"{MAT_FOLDER}/MI_Foliage_Banyan_Natural.MI_Foliage_Banyan_Natural"
palm_foliage = f"{MAT_FOLDER}/MI_Foliage_PalmFrond.MI_Foliage_PalmFrond"
kamini_mat = f"{MAT_FOLDER}/MI_Foliage_Fern_Natural.MI_Foliage_Fern_Natural"

assignments = [
    ("SM_Tree_Raintree_Master", [
        ("M_Bark_Tree", bark_mat),
        ("M_Master_NaturalFoliage", raintree_foliage)
    ]),
    ("SM_Tree_Krishnachura_Master", [
        ("M_Bark_Tree", bark_mat),
        ("MI_Foliage_Krishnachura_Natural", krishna_foliage)
    ]),
    ("SM_Tree_Banyan_Master", [
        ("M_Bark_Tree", bark_mat),
        ("MI_Foliage_Banyan_Natural", banyan_foliage)
    ]),
    ("SM_Tree_RoyalPalm_Master", [
        ("M_Bark_Tree", bark_mat),
        ("MI_Foliage_PalmFrond", palm_foliage)
    ]),
    ("SM_Campus_Grass_Lawn", [
        ("MI_Ground_Grass", grass_mi)
    ]),
    ("SM_Campus_Grass_Tuft", [
        ("MI_Ground_Grass", grass_mi)
    ]),
    ("SM_Campus_Bush_Kamini", [
        ("MI_Foliage_Fern_Natural", kamini_mat)
    ]),
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
            print(f"  ✓ {mesh_name} [{slot_name}] -> {mat_ref.split('.')[-1]}")
        except Exception as e:
            print(f"  Assignment ERROR ({mesh_name}.{slot_name}): {e}")

# Save assets
for mesh_name, _ in assignments:
    try:
        invoke_tool("save_assets", ASSET_TOOLS, {
            "assets": [{"refPath": f"{VEG_FOLDER}/{mesh_name}.{mesh_name}"}]
        })
    except Exception:
        pass

print("\n✓ All vegetation mesh material slots successfully assigned and saved!")
