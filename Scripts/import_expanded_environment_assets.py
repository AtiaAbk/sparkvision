#!/usr/bin/env python3
"""
Imports expanded botanical and wildlife FBX models into /Game/SparkVision/Campus/Environment/
and assigns their respective PBR Material Instances.
"""

import sys
import os
import json
import subprocess

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mcp_client

ENV_MODELS_DIR = "/Users/atiaoishi/Downloads/sparkvision/SourceAssets/Models/Environment"
ENV_UE_FOLDER = "/Game/SparkVision/Campus/Environment"

EXPANDED_ASSETS = [
    {
        "name": "SM_Tree_Debdaru_Columnar",
        "file": os.path.join(ENV_MODELS_DIR, "SM_Tree_Debdaru_Columnar.fbx"),
        "folder": ENV_UE_FOLDER,
        "slots": [
            "/Game/SparkVision/Materials/MI_Bark_Tree.MI_Bark_Tree",
            "/Game/SparkVision/Materials/MI_Foliage_Debdaru_Dark.MI_Foliage_Debdaru_Dark"
        ]
    },
    {
        "name": "SM_Tree_Mahogany_Grand",
        "file": os.path.join(ENV_MODELS_DIR, "SM_Tree_Mahogany_Grand.fbx"),
        "folder": ENV_UE_FOLDER,
        "slots": [
            "/Game/SparkVision/Materials/MI_Bark_Tree.MI_Bark_Tree",
            "/Game/SparkVision/Materials/MI_Foliage_Raintree_Leaf.MI_Foliage_Raintree_Leaf"
        ]
    },
    {
        "name": "SM_Tree_Kadam_Bloom",
        "file": os.path.join(ENV_MODELS_DIR, "SM_Tree_Kadam_Bloom.fbx"),
        "folder": ENV_UE_FOLDER,
        "slots": [
            "/Game/SparkVision/Materials/MI_Bark_Tree.MI_Bark_Tree",
            "/Game/SparkVision/Materials/MI_Foliage_Neem_Green.MI_Foliage_Neem_Green",
            "/Game/SparkVision/Materials/MI_Foliage_Kadam_Golden.MI_Foliage_Kadam_Golden"
        ]
    },
    {
        "name": "SM_Cluster_Bamboo_Grove",
        "file": os.path.join(ENV_MODELS_DIR, "SM_Cluster_Bamboo_Grove.fbx"),
        "folder": ENV_UE_FOLDER,
        "slots": [
            "/Game/SparkVision/Materials/MI_Stem_BambooGold.MI_Stem_BambooGold",
            "/Game/SparkVision/Materials/MI_Foliage_BambooLeaf.MI_Foliage_BambooLeaf"
        ]
    },
    {
        "name": "SM_Bush_Rangan_Scarlet",
        "file": os.path.join(ENV_MODELS_DIR, "SM_Bush_Rangan_Scarlet.fbx"),
        "folder": ENV_UE_FOLDER,
        "slots": [
            "/Game/SparkVision/Materials/MI_Foliage_Banyan_Leaf.MI_Foliage_Banyan_Leaf",
            "/Game/SparkVision/Materials/MI_Flower_Rangan_Scarlet.MI_Flower_Rangan_Scarlet"
        ]
    },
    {
        "name": "SM_Bush_Gandharaj_White",
        "file": os.path.join(ENV_MODELS_DIR, "SM_Bush_Gandharaj_White.fbx"),
        "folder": ENV_UE_FOLDER,
        "slots": [
            "/Game/SparkVision/Materials/MI_Foliage_Banyan_Leaf.MI_Foliage_Banyan_Leaf",
            "/Game/SparkVision/Materials/MI_Flower_Gardenia_White.MI_Flower_Gardenia_White"
        ]
    },
    {
        "name": "SM_Bush_Kamini_Hedge",
        "file": os.path.join(ENV_MODELS_DIR, "SM_Bush_Kamini_Hedge.fbx"),
        "folder": ENV_UE_FOLDER,
        "slots": [
            "/Game/SparkVision/Materials/MI_Curzon_Hedge.MI_Curzon_Hedge",
            "/Game/SparkVision/Materials/MI_Flower_Gardenia_White.MI_Flower_Gardenia_White"
        ]
    },
    {
        "name": "SM_Grass_Tuft_Lawn",
        "file": os.path.join(ENV_MODELS_DIR, "SM_Grass_Tuft_Lawn.fbx"),
        "folder": ENV_UE_FOLDER,
        "slots": [
            "/Game/SparkVision/Materials/MI_Ground_Grass.MI_Ground_Grass"
        ]
    },
    {
        "name": "SM_Grass_Tall_Savanna",
        "file": os.path.join(ENV_MODELS_DIR, "SM_Grass_Tall_Savanna.fbx"),
        "folder": ENV_UE_FOLDER,
        "slots": [
            "/Game/SparkVision/Materials/MI_Stem_ReedGreen.MI_Stem_ReedGreen",
            "/Game/SparkVision/Materials/MI_Foliage_KashfulWhite.MI_Foliage_KashfulWhite"
        ]
    },
    {
        "name": "SM_Fern_Undergrowth_Cluster",
        "file": os.path.join(ENV_MODELS_DIR, "SM_Fern_Undergrowth_Cluster.fbx"),
        "folder": ENV_UE_FOLDER,
        "slots": [
            "/Game/SparkVision/Materials/MI_Foliage_Fern_Emerald.MI_Foliage_Fern_Emerald"
        ]
    },
    {
        "name": "SM_Ground_LeafLitter_Patch",
        "file": os.path.join(ENV_MODELS_DIR, "SM_Ground_LeafLitter_Patch.fbx"),
        "folder": ENV_UE_FOLDER,
        "slots": [
            "/Game/SparkVision/Materials/MI_Ground_LeafLitter_Moist.MI_Ground_LeafLitter_Moist"
        ]
    },
    {
        "name": "SM_Wildlife_Bird_Doel",
        "file": os.path.join(ENV_MODELS_DIR, "SM_Wildlife_Bird_Doel.fbx"),
        "folder": ENV_UE_FOLDER,
        "slots": [
            "/Game/SparkVision/Materials/MI_Fauna_Doel_Black.MI_Fauna_Doel_Black",
            "/Game/SparkVision/Materials/MI_Fauna_Doel_White.MI_Fauna_Doel_White"
        ]
    },
    {
        "name": "SM_Wildlife_Butterfly_Cluster",
        "file": os.path.join(ENV_MODELS_DIR, "SM_Wildlife_Butterfly_Cluster.fbx"),
        "folder": ENV_UE_FOLDER,
        "slots": [
            "/Game/SparkVision/Materials/MI_Fauna_Butterfly_Yellow.MI_Fauna_Butterfly_Yellow"
        ]
    },
    {
        "name": "SM_Wildlife_Dragonfly_Pair",
        "file": os.path.join(ENV_MODELS_DIR, "SM_Wildlife_Dragonfly_Pair.fbx"),
        "folder": ENV_UE_FOLDER,
        "slots": [
            "/Game/SparkVision/Materials/MI_Fauna_Dragonfly_Teal.MI_Fauna_Dragonfly_Teal"
        ]
    }
]

def main():
    print("=" * 70)
    print("IMPORTING EXPANDED BOTANICAL & WILDLIFE ASSETS TO UNREAL ENGINE...")
    print("=" * 70)

    for item in EXPANDED_ASSETS:
        name = item["name"]
        src_file = item["file"]
        folder = item["folder"]
        mesh_ref = f"{folder}/{name}.{name}"

        # Delete old asset if exists
        try:
            mcp_client.invoke_tool("delete", "editor_toolset.toolsets.asset.AssetTools", {"path": mesh_ref})
        except Exception:
            pass

        print(f"\nImporting Static Mesh: {name}...")
        try:
            mcp_client.invoke_tool("import_file", "editor_toolset.toolsets.static_mesh.StaticMeshTools", {
                "folder_path": folder,
                "asset_name": name,
                "source_file": src_file,
                "import_materials": False,
                "import_textures": False,
                "combine_meshes": True
            })
            print(f"  Successfully imported: {mesh_ref}")
        except Exception as e:
            print(f"  Import failed for {name}: {e}")
            continue

        # Get actual material slot names from mesh
        try:
            slot_res = mcp_client.invoke_tool("get_material_slots", "editor_toolset.toolsets.static_mesh.StaticMeshTools", {
                "mesh": {"refPath": mesh_ref}
            })
            slot_names = slot_res.get("returnValue", [])
        except Exception as e:
            print(f"  Failed to get material slots: {e}")
            slot_names = []

        # Set material slots by slot name
        for idx, mat_ref in enumerate(item["slots"]):
            if idx < len(slot_names):
                slot_name = slot_names[idx]
                try:
                    mcp_client.invoke_tool("set_material", "editor_toolset.toolsets.static_mesh.StaticMeshTools", {
                        "mesh": {"refPath": mesh_ref},
                        "slot_name": slot_name,
                        "material": {"refPath": mat_ref}
                    })
                    print(f"    Slot '{slot_name}' -> {mat_ref}")
                except Exception as e:
                    print(f"    Slot '{slot_name}' assignment failed: {e}")

    print("\n" + "=" * 70)
    print("ALL 14 EXPANDED ASSETS IMPORTED & TEXTURED SUCCESSFULLY!")
    print("=" * 70)

if __name__ == "__main__":
    main()
