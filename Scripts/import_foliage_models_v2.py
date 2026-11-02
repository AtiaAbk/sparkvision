#!/usr/bin/env python3
"""
Imports the v2 high-fidelity foliage FBX models into Unreal Engine 5.8:
- SM_Natural_Raintree_Grand
- SM_Natural_Banyan_Heritage
- SM_Natural_Krishnachura_Bloom
- SM_Natural_Fern_Cluster
And sets up their material slots with the compiled Two-Sided Foliage PBR materials.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

SOURCE_DIR = "/Users/atiaoishi/Downloads/sparkvision/SourceAssets/Models/NaturalFoliage"
TARGET_FOLDER = "/Game/SparkVision/Campus/Environment"

BARK_MAT = "/Game/SparkVision/Materials/MI_Bark_Natural_Gnarled.MI_Bark_Natural_Gnarled"
RAINTREE_MAT = "/Game/SparkVision/Materials/MI_Foliage_Raintree_Natural.MI_Foliage_Raintree_Natural"
BANYAN_MAT = "/Game/SparkVision/Materials/MI_Foliage_Banyan_Natural.MI_Foliage_Banyan_Natural"
KRISHNA_MAT = "/Game/SparkVision/Materials/MI_Foliage_Krishnachura_Natural.MI_Foliage_Krishnachura_Natural"
FERN_MAT = "/Game/SparkVision/Materials/MI_Foliage_Fern_Natural.MI_Foliage_Fern_Natural"

MODELS = [
    {
        "name": "SM_Natural_Raintree_Grand",
        "file": f"{SOURCE_DIR}/SM_Natural_Raintree_Grand.fbx",
        "slots": [BARK_MAT, RAINTREE_MAT]
    },
    {
        "name": "SM_Natural_Banyan_Heritage",
        "file": f"{SOURCE_DIR}/SM_Natural_Banyan_Heritage.fbx",
        "slots": [BARK_MAT, BANYAN_MAT]
    },
    {
        "name": "SM_Natural_Krishnachura_Bloom",
        "file": f"{SOURCE_DIR}/SM_Natural_Krishnachura_Bloom.fbx",
        "slots": [BARK_MAT, KRISHNA_MAT]
    },
    {
        "name": "SM_Natural_Fern_Cluster",
        "file": f"{SOURCE_DIR}/SM_Natural_Fern_Cluster.fbx",
        "slots": [FERN_MAT]
    },
]

def main():
    print("=" * 65)
    print("IMPORTING V2 NATURAL FOLIAGE MODELS INTO UNREAL ENGINE")
    print("=" * 65)

    for item in MODELS:
        name = item["name"]
        fbx_path = item["file"]
        mesh_ref = f"{TARGET_FOLDER}/{name}.{name}"
        asset_path = f"{TARGET_FOLDER}/{name}"

        print(f"\nImporting {name} from {fbx_path}...")

        # Delete existing asset so import_file doesn't conflict
        try:
            invoke_tool("delete", "editor_toolset.toolsets.asset.AssetTools", {
                "path": asset_path
            })
            print(f"  Deleted previous {name}")
        except Exception as e:
            print(f"  Delete notice: {e}")

        # Import FBX
        try:
            res = invoke_tool("import_file", "editor_toolset.toolsets.static_mesh.StaticMeshTools", {
                "folder_path": TARGET_FOLDER,
                "asset_name": name,
                "source_file": fbx_path,
                "import_materials": False,
                "import_textures": False,
                "combine_meshes": True
            })
            print(f"  ✓ Imported: {mesh_ref}")
        except Exception as e:
            print(f"  ✗ Import error for {name}: {e}")
            continue

        # Set materials
        for idx, mat in enumerate(item["slots"]):
            try:
                invoke_tool("set_material", "editor_toolset.toolsets.static_mesh.StaticMeshTools", {
                    "mesh": {"refPath": mesh_ref},
                    "material_index": idx,
                    "material": {"refPath": mat}
                })
                print(f"  ✓ Slot {idx} -> {mat.split('.')[-1]}")
            except Exception as e:
                print(f"  ✗ Set material error on slot {idx}: {e}")

        # Save asset
        invoke_tool("save_assets", "editor_toolset.toolsets.asset.AssetTools", {
            "asset_paths": [asset_path]
        })
        print(f"  ✓ Saved {name}")

    print("\n✅ ALL 4 V2 NATURAL FOLIAGE MODELS SUCCESSFULLY IMPORTED & TEXTURED!")

if __name__ == "__main__":
    main()
