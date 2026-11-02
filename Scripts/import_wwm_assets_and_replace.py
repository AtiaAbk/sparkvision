#!/usr/bin/env python3
"""
Import WWM Assets and Replace in Compact Campus Map:
- Imports SM_ArchiveTerminal_WWM, SM_Tree_Krishnachura_WWM, SM_Pond_WaterLily_WWM
- Assigns PBR materials
- Swaps the meshes on existing Archive Terminals and pond trees
- Places hanging brass lanterns along Curzon veranda
"""

import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

SOURCE_DIR = "/Users/atiaoishi/Downloads/sparkvision/SourceAssets/Models"

def main():
    print("=" * 60)
    print("IMPORTING WWM UPGRADED ASSETS & UPDATING LEVEL")
    print("=" * 60)

    # 1. Import meshes
    imports = [
        ("/Game/SparkVision/Campus", "SM_ArchiveTerminal_WWM", os.path.join(SOURCE_DIR, "SM_ArchiveTerminal.fbx")),
        ("/Game/SparkVision/Campus/Environment", "SM_Tree_Krishnachura_WWM", os.path.join(SOURCE_DIR, "SM_Tree_Krishnachura_Bloom.fbx")),
        ("/Game/SparkVision/Campus/Environment", "SM_Pond_WaterLily_WWM", os.path.join(SOURCE_DIR, "SM_Pond_WaterLily_Cluster.fbx")),
    ]

    for folder, name, fbx in imports:
        print(f"\nImporting {name}...")
        try:
            res = invoke_tool("import_file", "editor_toolset.toolsets.static_mesh.StaticMeshTools", {
                "folder_path": folder,
                "asset_name": name,
                "source_file": fbx,
                "import_materials": False,
                "import_textures": False,
                "combine_meshes": True
            })
            print(f"  ✓ Imported: {name}")
        except Exception as e:
            print(f"  Notice: {e}")

    # 2. Assign Materials to Static Meshes
    mat_assignments = [
        ("/Game/SparkVision/Campus/SM_ArchiveTerminal_WWM.SM_ArchiveTerminal_WWM", "/Game/SparkVision/Materials/MI_ArchiveTerminal.MI_ArchiveTerminal"),
        ("/Game/SparkVision/Campus/Environment/SM_Tree_Krishnachura_WWM.SM_Tree_Krishnachura_WWM", "/Game/SparkVision/Materials/MI_Foliage_Krishnachura_Red.MI_Foliage_Krishnachura_Red"),
        ("/Game/SparkVision/Campus/Environment/SM_Pond_WaterLily_WWM.SM_Pond_WaterLily_WWM", "/Game/SparkVision/Materials/MI_Ground_Grass.MI_Ground_Grass"),
    ]

    for mesh_ref, mat_ref in mat_assignments:
        try:
            values = {
                "StaticMaterials": [
                    {"materialInterface": {"refPath": mat_ref}}
                ]
            }
            invoke_tool("set_properties", "editor_toolset.toolsets.object.ObjectTools", {
                "instance": {"refPath": mesh_ref},
                "values": json.dumps(values)
            })
            print(f"  ✓ Assigned {mat_ref} to {mesh_ref}")
        except Exception as e:
            print(f"  Notice setting static material: {e}")

    # 3. Swap meshes on Archive Terminal actors
    print("\nUpdating Archive Terminals in Level...")
    new_archive_mesh = "/Game/SparkVision/Campus/SM_ArchiveTerminal_WWM.SM_ArchiveTerminal_WWM"
    archives = invoke_tool("find_actors", "editor_toolset.toolsets.scene.SceneTools", {
        "name": "ArchiveTerminal",
        "tag": "",
        "collision_channels": []
    }).get("returnValue", [])

    print(f"Found {len(archives)} ArchiveTerminal actors in level.")
    for a in archives:
        actor_ref = a["refPath"]
        comps = invoke_tool("get_components", "editor_toolset.toolsets.actor.ActorTools", {
            "actor": {"refPath": actor_ref}
        }).get("returnValue", [])
        for c in comps:
            c_ref = c["refPath"]
            try:
                invoke_tool("set_properties", "editor_toolset.toolsets.object.ObjectTools", {
                    "instance": {"refPath": c_ref},
                    "values": json.dumps({"StaticMesh": {"refPath": new_archive_mesh}})
                })
                print(f"  ✓ Updated mesh on {actor_ref}")
            except Exception as e:
                print(f"  Notice: {e}")

    # 4. Swap meshes on pond cartoon trees (SM_Tree_Jarul_Purple)
    print("\nReplacing cartoon blob trees around Curzon Pond...")
    trees = invoke_tool("find_actors", "editor_toolset.toolsets.scene.SceneTools", {
        "name": "Tree_",
        "tag": "",
        "collision_channels": []
    }).get("returnValue", [])

    new_tree_mesh = "/Game/SparkVision/Campus/Environment/SM_Tree_Krishnachura_WWM.SM_Tree_Krishnachura_WWM"
    swapped = 0
    for t in trees:
        actor_ref = t["refPath"]
        comps = invoke_tool("get_components", "editor_toolset.toolsets.actor.ActorTools", {
            "actor": {"refPath": actor_ref}
        }).get("returnValue", [])
        for c in comps:
            c_ref = c["refPath"]
            props = invoke_tool("get_properties", "editor_toolset.toolsets.object.ObjectTools", {
                "instance": {"refPath": c_ref},
                "properties": ["StaticMesh"]
            }).get("returnValue", "")
            if "SM_Tree_Jarul_Purple" in props:
                invoke_tool("set_properties", "editor_toolset.toolsets.object.ObjectTools", {
                    "instance": {"refPath": c_ref},
                    "values": json.dumps({"StaticMesh": {"refPath": new_tree_mesh}})
                })
                swapped += 1
    print(f"  ✓ Swapped {swapped} cartoon trees with WWM Krishnachura Bloom trees!")

    # 5. Place Hanging Brass Lanterns under Curzon Veranda
    print("\nPlacing hanging brass lanterns under Curzon Veranda arches...")
    lantern_mesh = "/Game/SparkVision/Campus/Environment/SM_Curzon_Lantern.SM_Curzon_Lantern"
    # Curzon portal is at X=-3400, Y=0, Z=0. Veranda arches span Y=-2400 to Y=+2400 at X=-3450, Z=450
    lantern_positions = [
        (-3420, -1800, 480),
        (-3420, -1200, 480),
        (-3420, -600, 480),
        (-3420, 600, 480),
        (-3420, 1200, 480),
        (-3420, 1800, 480),
        # Entrance portal flanking
        (-3440, -150, 450),
        (-3440, 150, 450),
    ]

    for i, (lx, ly, lz) in enumerate(lantern_positions):
        lname = f"Curzon_Veranda_Lantern_{i+1:02d}"
        try:
            res = invoke_tool("add_to_scene_from_asset", "editor_toolset.toolsets.scene.SceneTools", {
                "asset_path": lantern_mesh,
                "name": lname,
                "xform": {
                    "location": {"x": lx, "y": ly, "z": lz},
                    "rotation": {"pitch": 0.0, "yaw": 0.0, "roll": 0.0},
                    "scale": {"x": 1.2, "y": 1.2, "z": 1.2}
                }
            })
            actor_ref = res.get("returnValue", {}).get("refPath", "")
            if actor_ref:
                invoke_tool("set_actor_folder", "editor_toolset.toolsets.scene.SceneTools", {
                    "actor": {"refPath": actor_ref},
                    "folder_path": "Heritage_Lighting/Lanterns"
                })
                print(f"  ✓ Placed {lname} at ({lx}, {ly}, {lz})")
        except Exception as e:
            print(f"  Notice placing lantern: {e}")

    # 6. Save current level & assets
    print("\nSaving level and assets...")
    try:
        invoke_tool("save_current_level", "editor_toolset.toolsets.scene.SceneTools", {})
        invoke_tool("save_assets", "editor_toolset.toolsets.asset.AssetTools", {
            "asset_paths": [
                "/Game/SparkVision/Campus/SM_ArchiveTerminal_WWM",
                "/Game/SparkVision/Campus/Environment/SM_Tree_Krishnachura_WWM",
                "/Game/SparkVision/Campus/Environment/SM_Pond_WaterLily_WWM"
            ]
        })
        print("  ✓ Level and assets saved successfully!")
    except Exception as e:
        print(f"Notice saving: {e}")

    print("\n✅ WWM Upgrade complete!")

if __name__ == "__main__":
    main()
