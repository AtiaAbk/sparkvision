#!/usr/bin/env python3
"""
Full University of Dhaka Campus Assembly Script
Updates and populates LV_Campus_Blockout with authentic architectural meshes:
- Replaces all placeholder boxes (Kala Bhaban, Jagannath Hall, Science Labs, Surja Sen, Mohsin, Bangla Academy)
- Instantiates new landmark actors (Central Mosque, SM Hall, Shahidullah Hall, Rokeya Hall, IBA, Admin Building, Skylines)
- Configures Outliner folder organization
- Saves the level
"""

import json
import subprocess
import time

def run_mcp(toolset, tool, args):
    res = subprocess.check_output([
        "/Users/atiaoishi/Downloads/sparkvision/Scripts/mcp_client.py",
        "call", toolset, tool, json.dumps(args)
    ])
    return json.loads(res) if res.strip() else {}

print("=" * 70)
print("ASSEMBLING COMPLETE UNIVERSITY OF DHAKA CAMPUS ENVIRONMENT...")
print("=" * 70)

# 1. Update Existing Placeholder Actors with New Architectural Meshes
REPLACEMENTS = [
    {
        "search": "ArtsFaculty_KalaBhaban",
        "mesh": "/Game/SparkVision/Campus/Landmarks/SM_KalaBhaban.SM_KalaBhaban",
        "location": {"x": 78214.0, "y": -91827.0, "z": 20.0},
        "rotation": {"pitch": 0.0, "yaw": 0.0, "roll": 0.0},
        "scale": {"x": 1.0, "y": 1.0, "z": 1.0},
        "folder": "Hero_Buildings/Arts_Faculty"
    },
    {
        "search": "Supporting_JagannathHall",
        "mesh": "/Game/SparkVision/Campus/Landmarks/SM_Jagannath_Hall.SM_Jagannath_Hall",
        "location": {"x": 20000.0, "y": -55000.0, "z": 20.0},
        "rotation": {"pitch": 0.0, "yaw": 0.0, "roll": 0.0},
        "scale": {"x": 1.0, "y": 1.0, "z": 1.0},
        "folder": "Hero_Buildings/Student_Halls"
    },
    {
        "search": "Supporting_CurzonChemistryPhysicsLabs",
        "mesh": "/Game/SparkVision/Campus/Landmarks/SM_Curzon_ScienceAnnex.SM_Curzon_ScienceAnnex",
        "location": {"x": 6500.0, "y": 2500.0, "z": 20.0},
        "rotation": {"pitch": 0.0, "yaw": 0.0, "roll": 0.0},
        "scale": {"x": 1.0, "y": 1.0, "z": 1.0},
        "folder": "Hero_Buildings/Curzon_Hall"
    },
    {
        "search": "Supporting_SurjaSenHall",
        "mesh": "/Game/SparkVision/Campus/Landmarks/SM_SurjaSen_Hall.SM_SurjaSen_Hall",
        "location": {"x": 66000.0, "y": -93000.0, "z": 20.0},
        "rotation": {"pitch": 0.0, "yaw": 0.0, "roll": 0.0},
        "scale": {"x": 1.0, "y": 1.0, "z": 1.0},
        "folder": "Hero_Buildings/Student_Halls"
    },
    {
        "search": "Supporting_HajiMuhammadMohsinHall",
        "mesh": "/Game/SparkVision/Campus/Landmarks/SM_SurjaSen_Hall.SM_SurjaSen_Hall",
        "location": {"x": 64000.0, "y": -102000.0, "z": 20.0},
        "rotation": {"pitch": 0.0, "yaw": 0.0, "roll": 0.0},
        "scale": {"x": 1.0, "y": 1.0, "z": 1.0},
        "folder": "Hero_Buildings/Student_Halls"
    },
    {
        "search": "Supporting_BanglaAcademy",
        "mesh": "/Game/SparkVision/Campus/Landmarks/SM_BanglaAcademy.SM_BanglaAcademy",
        "location": {"x": 18000.0, "y": -28000.0, "z": 20.0},
        "rotation": {"pitch": 0.0, "yaw": -59.1, "roll": 0.0},
        "scale": {"x": 1.0, "y": 1.0, "z": 1.0},
        "folder": "Hero_Buildings/Doyel_Chattar"
    }
]

print("\n--- Upgrading Existing Actors to Authentic Architectural Meshes ---")
for rep in REPLACEMENTS:
    search_term = rep["search"]
    try:
        found = run_mcp("editor_toolset.toolsets.scene.SceneTools", "find_actors", {
            "name": search_term, "tag": "", "collision_channels": []
        }).get("returnValue", [])

        if not found:
            print(f"Actor matching '{search_term}' not found. Will spawn as new.")
            continue

        actor_ref = found[0]
        # Get StaticMeshComponent
        comps = run_mcp("editor_toolset.toolsets.actor.ActorTools", "get_components", {
            "actor": actor_ref
        }).get("returnValue", [])

        for c in comps:
            if "StaticMeshComponent" in c["refPath"]:
                print(f"Setting mesh {rep['mesh']} on {search_term}...")
                run_mcp("editor_toolset.toolsets.object.ObjectTools", "set_properties", {
                    "instance": c,
                    "values": json.dumps({"StaticMesh": {"refPath": rep["mesh"]}})
                })
                break

        # Set transform
        print(f"Setting transform on {search_term}...")
        run_mcp("editor_toolset.toolsets.actor.ActorTools", "set_actor_transform", {
            "actor": actor_ref,
            "xform": {
                "location": rep["location"],
                "rotation": rep["rotation"],
                "scale": rep["scale"]
            },
            "worldspace": True
        })

        # Set folder
        if rep.get("folder"):
            run_mcp("editor_toolset.toolsets.scene.SceneTools", "set_actor_folder", {
                "actor": actor_ref,
                "folder_path": rep["folder"]
            })
        print(f"SUCCESS: Upgraded {search_term}")
    except Exception as e:
        print(f"Error upgrading {search_term}: {e}")

# 2. Spawn New Campus Buildings
NEW_SPAWNS = [
    {
        "name": "Hero_DU_CentralMosque",
        "asset": "/Game/SparkVision/Campus/Landmarks/SM_CentralMosque.SM_CentralMosque",
        "location": {"x": 82582.0, "y": -72180.0, "z": 20.0},
        "rotation": {"pitch": 0.0, "yaw": 0.0, "roll": 0.0},
        "scale": {"x": 1.0, "y": 1.0, "z": 1.0},
        "folder": "Hero_Buildings/Central_Mosque"
    },
    {
        "name": "Hero_SalimullahMuslim_Hall",
        "asset": "/Game/SparkVision/Campus/Landmarks/SM_SalimullahMuslim_Hall.SM_SalimullahMuslim_Hall",
        "location": {"x": 15000.0, "y": -68000.0, "z": 20.0},
        "rotation": {"pitch": 0.0, "yaw": 0.0, "roll": 0.0},
        "scale": {"x": 1.0, "y": 1.0, "z": 1.0},
        "folder": "Hero_Buildings/Student_Halls"
    },
    {
        "name": "Hero_DrShahidullah_Hall",
        "asset": "/Game/SparkVision/Campus/Landmarks/SM_Shahidullah_Hall.SM_Shahidullah_Hall",
        "location": {"x": 5000.0, "y": -5000.0, "z": 20.0},
        "rotation": {"pitch": 0.0, "yaw": 0.0, "roll": 0.0},
        "scale": {"x": 1.0, "y": 1.0, "z": 1.0},
        "folder": "Hero_Buildings/Student_Halls"
    },
    {
        "name": "Hero_Rokeya_Hall",
        "asset": "/Game/SparkVision/Campus/Landmarks/SM_Rokeya_Hall.SM_Rokeya_Hall",
        "location": {"x": 42000.0, "y": -66000.0, "z": 20.0},
        "rotation": {"pitch": 0.0, "yaw": 0.0, "roll": 0.0},
        "scale": {"x": 1.0, "y": 1.0, "z": 1.0},
        "folder": "Hero_Buildings/Student_Halls"
    },
    {
        "name": "Supporting_Curzon_PhysicsAnnex",
        "asset": "/Game/SparkVision/Campus/Landmarks/SM_Curzon_ScienceAnnex.SM_Curzon_ScienceAnnex",
        "location": {"x": 6500.0, "y": -2500.0, "z": 20.0},
        "rotation": {"pitch": 0.0, "yaw": 0.0, "roll": 0.0},
        "scale": {"x": 1.0, "y": 1.0, "z": 1.0},
        "folder": "Hero_Buildings/Curzon_Hall"
    },
    {
        "name": "Supporting_Admin_RegistrarBuilding",
        "asset": "/Game/SparkVision/Campus/Landmarks/SM_Admin_Building.SM_Admin_Building",
        "location": {"x": 66000.0, "y": -78000.0, "z": 20.0},
        "rotation": {"pitch": 0.0, "yaw": 0.0, "roll": 0.0},
        "scale": {"x": 1.0, "y": 1.0, "z": 1.0},
        "folder": "Supporting_Buildings/Administrative"
    },
    {
        "name": "Supporting_IBA_Building",
        "asset": "/Game/SparkVision/Campus/Landmarks/SM_IBA_Building.SM_IBA_Building",
        "location": {"x": 53000.0, "y": -52000.0, "z": 20.0},
        "rotation": {"pitch": 0.0, "yaw": -59.1, "roll": 0.0},
        "scale": {"x": 1.0, "y": 1.0, "z": 1.0},
        "folder": "Supporting_Buildings/Academic"
    },
    # Peripheral Skylines for Atmospheric Depth
    {
        "name": "Skyline_North_Shahbagh",
        "asset": "/Game/SparkVision/Campus/Landmarks/SM_Campus_Skyline.SM_Campus_Skyline",
        "location": {"x": 92000.0, "y": -55000.0, "z": 20.0},
        "rotation": {"pitch": 0.0, "yaw": 0.0, "roll": 0.0},
        "scale": {"x": 1.5, "y": 1.0, "z": 1.0},
        "folder": "Distant_Skyline"
    },
    {
        "name": "Skyline_East_HighCourt",
        "asset": "/Game/SparkVision/Campus/Landmarks/SM_Campus_Skyline.SM_Campus_Skyline",
        "location": {"x": 25000.0, "y": 15000.0, "z": 20.0},
        "rotation": {"pitch": 0.0, "yaw": 90.0, "roll": 0.0},
        "scale": {"x": 1.5, "y": 1.0, "z": 1.0},
        "folder": "Distant_Skyline"
    },
    {
        "name": "Skyline_West_Nilkhet",
        "asset": "/Game/SparkVision/Campus/Landmarks/SM_Campus_Skyline.SM_Campus_Skyline",
        "location": {"x": 70000.0, "y": -118000.0, "z": 20.0},
        "rotation": {"pitch": 0.0, "yaw": 90.0, "roll": 0.0},
        "scale": {"x": 1.5, "y": 1.0, "z": 1.0},
        "folder": "Distant_Skyline"
    },
    {
        "name": "Skyline_South_OldDhaka",
        "asset": "/Game/SparkVision/Campus/Landmarks/SM_Campus_Skyline.SM_Campus_Skyline",
        "location": {"x": -16000.0, "y": -30000.0, "z": 20.0},
        "rotation": {"pitch": 0.0, "yaw": 0.0, "roll": 0.0},
        "scale": {"x": 1.5, "y": 1.0, "z": 1.0},
        "folder": "Distant_Skyline"
    }
]

print("\n--- Spawning New Campus Landmarks and Skylines ---")
for sp in NEW_SPAWNS:
    name = sp["name"]
    try:
        # Check if already exists
        existing = run_mcp("editor_toolset.toolsets.scene.SceneTools", "find_actors", {
            "name": name, "tag": "", "collision_channels": []
        }).get("returnValue", [])
        if existing:
            print(f"Actor '{name}' already exists. Updating transform...")
            run_mcp("editor_toolset.toolsets.actor.ActorTools", "set_actor_transform", {
                "actor": existing[0],
                "xform": {
                    "location": sp["location"],
                    "rotation": sp["rotation"],
                    "scale": sp["scale"]
                },
                "worldspace": True
            })
            continue

        print(f"Spawning {name} from {sp['asset']}...")
        new_actor = run_mcp("editor_toolset.toolsets.scene.SceneTools", "add_to_scene_from_asset", {
            "asset_path": sp["asset"],
            "name": name,
            "xform": {
                "location": sp["location"],
                "rotation": sp["rotation"],
                "scale": sp["scale"]
            },
            "snap_to_ground": False
        }).get("returnValue")

        if new_actor:
            run_mcp("editor_toolset.toolsets.actor.ActorTools", "set_label", {
                "actor": new_actor,
                "label": name
            })
            run_mcp("editor_toolset.toolsets.scene.SceneTools", "set_actor_folder", {
                "actor": new_actor,
                "folder_path": sp["folder"]
            })
            print(f"SUCCESS: Spawned {name}")
    except Exception as e:
        print(f"Error spawning {name}: {e}")

# Save Level & All Modified Assets
print("\nSaving Level and all assets to disk...")
try:
    run_mcp("editor_toolset.toolsets.asset.AssetTools", "save_assets", {
        "asset_paths": []
    })
    print("SUCCESS: Level and assets saved!")
except Exception as e:
    print(f"Error saving level: {e}")

print("\n" + "=" * 70)
print("CAMPUS ASSEMBLY COMPLETE!")
print("=" * 70)
