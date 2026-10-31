#!/usr/bin/env python3
import os
import json
import subprocess

CURZON_MODELS_DIR = "/Users/atiaoishi/Downloads/sparkvision/SourceAssets/Models/CurzonModular"
ENV_MODELS_DIR = "/Users/atiaoishi/Downloads/sparkvision/SourceAssets/Models/Environment"

CURZON_UE_FOLDER = "/Game/SparkVision/Campus/CurzonModular"
ENV_UE_FOLDER = "/Game/SparkVision/Campus/Environment"

CURZON_ASSETS = [
    {
        "name": "SM_Curzon_Veranda_Arch_Lower",
        "file": os.path.join(CURZON_MODELS_DIR, "SM_Curzon_Veranda_Arch_Lower.fbx"),
        "folder": CURZON_UE_FOLDER,
        "slots": [
            "/Game/SparkVision/Materials/MI_Curzon_Brick.MI_Curzon_Brick",
            "/Game/SparkVision/Materials/MI_Curzon_WhiteTrim.MI_Curzon_WhiteTrim",
            "/Game/SparkVision/Materials/MI_Curzon_Sandstone.MI_Curzon_Sandstone",
            "/Game/SparkVision/Materials/MI_Curzon_Tiles.MI_Curzon_Tiles"
        ]
    },
    {
        "name": "SM_Curzon_Veranda_Arch_Upper",
        "file": os.path.join(CURZON_MODELS_DIR, "SM_Curzon_Veranda_Arch_Upper.fbx"),
        "folder": CURZON_UE_FOLDER,
        "slots": [
            "/Game/SparkVision/Materials/MI_Curzon_Brick.MI_Curzon_Brick",
            "/Game/SparkVision/Materials/MI_Curzon_WhiteTrim.MI_Curzon_WhiteTrim",
            "/Game/SparkVision/Materials/MI_Curzon_Sandstone.MI_Curzon_Sandstone",
            "/Game/SparkVision/Materials/MI_Curzon_Tiles.MI_Curzon_Tiles"
        ]
    },
    {
        "name": "SM_Curzon_Entrance_Portal",
        "file": os.path.join(CURZON_MODELS_DIR, "SM_Curzon_Entrance_Portal.fbx"),
        "folder": CURZON_UE_FOLDER,
        "slots": [
            "/Game/SparkVision/Materials/MI_Curzon_Brick.MI_Curzon_Brick",
            "/Game/SparkVision/Materials/MI_Curzon_WhiteTrim.MI_Curzon_WhiteTrim",
            "/Game/SparkVision/Materials/MI_Curzon_Sandstone.MI_Curzon_Sandstone",
            "/Game/SparkVision/Materials/MI_Curzon_Brass.MI_Curzon_Brass",
            "/Game/SparkVision/Materials/MI_Curzon_CastIron.MI_Curzon_CastIron"
        ]
    },
    {
        "name": "SM_Curzon_Tower_Octagon",
        "file": os.path.join(CURZON_MODELS_DIR, "SM_Curzon_Tower_Octagon.fbx"),
        "folder": CURZON_UE_FOLDER,
        "slots": [
            "/Game/SparkVision/Materials/MI_Curzon_Brick.MI_Curzon_Brick",
            "/Game/SparkVision/Materials/MI_Curzon_WhiteTrim.MI_Curzon_WhiteTrim",
            "/Game/SparkVision/Materials/MI_Curzon_Sandstone.MI_Curzon_Sandstone",
            "/Game/SparkVision/Materials/MI_Curzon_Brass.MI_Curzon_Brass"
        ]
    },
    {
        "name": "SM_Curzon_Parapet_Merlons",
        "file": os.path.join(CURZON_MODELS_DIR, "SM_Curzon_Parapet_Merlons.fbx"),
        "folder": CURZON_UE_FOLDER,
        "slots": [
            "/Game/SparkVision/Materials/MI_Curzon_Brick.MI_Curzon_Brick",
            "/Game/SparkVision/Materials/MI_Curzon_WhiteTrim.MI_Curzon_WhiteTrim"
        ]
    },
    {
        "name": "SM_Curzon_Chattri_Dome",
        "file": os.path.join(CURZON_MODELS_DIR, "SM_Curzon_Chattri_Dome.fbx"),
        "folder": CURZON_UE_FOLDER,
        "slots": [
            "/Game/SparkVision/Materials/MI_Curzon_Brick.MI_Curzon_Brick",
            "/Game/SparkVision/Materials/MI_Curzon_WhiteTrim.MI_Curzon_WhiteTrim",
            "/Game/SparkVision/Materials/MI_Curzon_Sandstone.MI_Curzon_Sandstone",
            "/Game/SparkVision/Materials/MI_Curzon_Brass.MI_Curzon_Brass"
        ]
    },
    {
        "name": "SM_Curzon_Lamp_Colonial",
        "file": os.path.join(CURZON_MODELS_DIR, "SM_Curzon_Lamp_Colonial.fbx"),
        "folder": CURZON_UE_FOLDER,
        "slots": [
            "/Game/SparkVision/Materials/MI_Curzon_CastIron.MI_Curzon_CastIron",
            "/Game/SparkVision/Materials/MI_Curzon_Brass.MI_Curzon_Brass"
        ]
    }
]

ENV_ASSETS = [
    {
        "name": "SM_Tree_Banyan_Mature",
        "file": os.path.join(ENV_MODELS_DIR, "SM_Tree_Banyan_Mature.fbx"),
        "folder": ENV_UE_FOLDER,
        "slots": [
            "/Game/SparkVision/Materials/MI_Bark_Tree.MI_Bark_Tree",
            "/Game/SparkVision/Materials/MI_Foliage_Banyan_Leaf.MI_Foliage_Banyan_Leaf"
        ]
    },
    {
        "name": "SM_Tree_Raintree_Avenue",
        "file": os.path.join(ENV_MODELS_DIR, "SM_Tree_Raintree_Avenue.fbx"),
        "folder": ENV_UE_FOLDER,
        "slots": [
            "/Game/SparkVision/Materials/MI_Bark_Tree.MI_Bark_Tree",
            "/Game/SparkVision/Materials/MI_Foliage_Raintree_Leaf.MI_Foliage_Raintree_Leaf"
        ]
    },
    {
        "name": "SM_Tree_Krishnachura_Bloom",
        "file": os.path.join(ENV_MODELS_DIR, "SM_Tree_Krishnachura_Bloom.fbx"),
        "folder": ENV_UE_FOLDER,
        "slots": [
            "/Game/SparkVision/Materials/MI_Bark_Tree.MI_Bark_Tree",
            "/Game/SparkVision/Materials/MI_Foliage_Krishnachura_Red.MI_Foliage_Krishnachura_Red"
        ]
    },
    {
        "name": "SM_Tree_Radhachura_Yellow",
        "file": os.path.join(ENV_MODELS_DIR, "SM_Tree_Radhachura_Yellow.fbx"),
        "folder": ENV_UE_FOLDER,
        "slots": [
            "/Game/SparkVision/Materials/MI_Bark_Tree.MI_Bark_Tree",
            "/Game/SparkVision/Materials/MI_Foliage_Radhachura_Yellow.MI_Foliage_Radhachura_Yellow"
        ]
    },
    {
        "name": "SM_Tree_Jarul_Purple",
        "file": os.path.join(ENV_MODELS_DIR, "SM_Tree_Jarul_Purple.fbx"),
        "folder": ENV_UE_FOLDER,
        "slots": [
            "/Game/SparkVision/Materials/MI_Bark_Tree.MI_Bark_Tree",
            "/Game/SparkVision/Materials/MI_Foliage_Jarul_Lilac.MI_Foliage_Jarul_Lilac"
        ]
    },
    {
        "name": "SM_Tree_Neem_Delicate",
        "file": os.path.join(ENV_MODELS_DIR, "SM_Tree_Neem_Delicate.fbx"),
        "folder": ENV_UE_FOLDER,
        "slots": [
            "/Game/SparkVision/Materials/MI_Bark_Tree.MI_Bark_Tree",
            "/Game/SparkVision/Materials/MI_Foliage_Neem_Green.MI_Foliage_Neem_Green"
        ]
    },
    {
        "name": "SM_Tree_Palm_Coconut",
        "file": os.path.join(ENV_MODELS_DIR, "SM_Tree_Palm_Coconut.fbx"),
        "folder": ENV_UE_FOLDER,
        "slots": [
            "/Game/SparkVision/Materials/MI_Bark_Palm.MI_Bark_Palm",
            "/Game/SparkVision/Materials/MI_Foliage_PalmFrond.MI_Foliage_PalmFrond"
        ]
    },
    {
        "name": "SM_Tree_Palm_BetelNut",
        "file": os.path.join(ENV_MODELS_DIR, "SM_Tree_Palm_BetelNut.fbx"),
        "folder": ENV_UE_FOLDER,
        "slots": [
            "/Game/SparkVision/Materials/MI_Bark_Palm.MI_Bark_Palm",
            "/Game/SparkVision/Materials/MI_Foliage_PalmFrond.MI_Foliage_PalmFrond"
        ]
    },
    {
        "name": "SM_Cluster_Bamboo_Thicket",
        "file": os.path.join(ENV_MODELS_DIR, "SM_Cluster_Bamboo_Thicket.fbx"),
        "folder": ENV_UE_FOLDER,
        "slots": [
            "/Game/SparkVision/Materials/MI_Stem_BambooGold.MI_Stem_BambooGold",
            "/Game/SparkVision/Materials/MI_Foliage_BambooLeaf.MI_Foliage_BambooLeaf"
        ]
    },
    {
        "name": "SM_Pond_WaterLily_Cluster",
        "file": os.path.join(ENV_MODELS_DIR, "SM_Pond_WaterLily_Cluster.fbx"),
        "folder": ENV_UE_FOLDER,
        "slots": [
            "/Game/SparkVision/Materials/MI_Foliage_LilyPad.MI_Foliage_LilyPad",
            "/Game/SparkVision/Materials/MI_Flower_Shapla.MI_Flower_Shapla"
        ]
    },
    {
        "name": "SM_Plant_Reeds_Kashful",
        "file": os.path.join(ENV_MODELS_DIR, "SM_Plant_Reeds_Kashful.fbx"),
        "folder": ENV_UE_FOLDER,
        "slots": [
            "/Game/SparkVision/Materials/MI_Stem_ReedGreen.MI_Stem_ReedGreen",
            "/Game/SparkVision/Materials/MI_Foliage_KashfulWhite.MI_Foliage_KashfulWhite"
        ]
    },
    {
        "name": "SM_Curzon_Pond_Ghat",
        "file": os.path.join(ENV_MODELS_DIR, "SM_Curzon_Pond_Ghat.fbx"),
        "folder": ENV_UE_FOLDER,
        "slots": [
            "/Game/SparkVision/Materials/MI_Curzon_Brick.MI_Curzon_Brick",
            "/Game/SparkVision/Materials/MI_Curzon_Sandstone.MI_Curzon_Sandstone"
        ]
    },
    {
        "name": "SM_Decal_Petal_Scatter",
        "file": os.path.join(ENV_MODELS_DIR, "SM_Decal_Petal_Scatter.fbx"),
        "folder": ENV_UE_FOLDER,
        "slots": [
            "/Game/SparkVision/Materials/MI_Decal_KrishnachuraPetals.MI_Decal_KrishnachuraPetals"
        ]
    }
]

def run_mcp(toolset, tool, args):
    res = subprocess.check_output([
        "/Users/atiaoishi/Downloads/sparkvision/Scripts/mcp_client.py",
        "call", toolset, tool, json.dumps(args)
    ])
    return json.loads(res) if res.strip() else {}

def import_assets(asset_list):
    for item in asset_list:
        name = item["name"]
        src_file = item["file"]
        folder = item["folder"]
        mesh_ref = f"{folder}/{name}.{name}"

        # Create folder
        try:
            run_mcp("editor_toolset.toolsets.asset.AssetTools", "create_folder", {"path": folder})
        except Exception:
            pass

        # Delete old asset if exists
        try:
            run_mcp("editor_toolset.toolsets.asset.AssetTools", "delete", {"path": mesh_ref})
        except Exception:
            pass

        print(f"Importing {name} from {src_file}...")
        try:
            run_mcp("editor_toolset.toolsets.static_mesh.StaticMeshTools", "import_file", {
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

        # Set material slots
        for idx, mat_ref in enumerate(item["slots"]):
            try:
                run_mcp("editor_toolset.toolsets.static_mesh.StaticMeshTools", "set_material", {
                    "mesh": {"refPath": mesh_ref},
                    "material_index": idx,
                    "material": {"refPath": mat_ref}
                })
                print(f"    Slot {idx} -> {mat_ref}")
            except Exception as e:
                print(f"    Slot {idx} assign failed: {e}")

if __name__ == "__main__":
    print("=== Importing Reconstructed Curzon Modular Assets ===")
    import_assets(CURZON_ASSETS)
    print("\n=== Importing Living Environment Botanical Assets ===")
    import_assets(ENV_ASSETS)
    print("\n=== All Assets Imported and Textured Successfully! ===")
