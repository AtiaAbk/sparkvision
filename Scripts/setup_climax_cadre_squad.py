#!/usr/bin/env python3
"""
Spawns and configures the Climax Cadre Squad at Curzon North Courtyard:
1. Cadre_Leader_NoukaCap: Leader with Bengali Nouka cap badge, high stats
2. Cadre_Lathiyal_01: Motorcycle cadre with black helmet & bamboo lathi
3. Cadre_Lathiyal_02: Motorcycle cadre with black helmet & bamboo lathi
4. Cadre_Lathiyal_03: Motorcycle cadre with black helmet & bamboo lathi
5. Bamboo Lathi weapons placed with the cadres
"""

import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

CADRE_MEMBERS = [
    {
        "name": "Cadre_Leader_NoukaCap",
        "loc": {"x": -1850.0, "y": 1750.0, "z": 150.0},
        "rot": {"pitch": 0.0, "yaw": -90.0, "roll": 0.0},
        "scale": {"x": 1.05, "y": 1.05, "z": 1.05},
        "health": 500.0,
        "damage": 35.0,
        "range": 220.0,
        "mat0": "/Game/SparkVision/Materials/MI_Cadre_NoukaCap.MI_Cadre_NoukaCap",
        "mat1": "/Game/SparkVision/Materials/MI_Student_DenimLegs.MI_Student_DenimLegs"
    },
    {
        "name": "Cadre_Lathiyal_01",
        "loc": {"x": -1650.0, "y": 1850.0, "z": 150.0},
        "rot": {"pitch": 0.0, "yaw": -105.0, "roll": 0.0},
        "scale": {"x": 1.0, "y": 1.0, "z": 1.0},
        "health": 350.0,
        "damage": 25.0,
        "range": 190.0,
        "mat0": "/Game/SparkVision/Materials/MI_Cadre_Helmet.MI_Cadre_Helmet",
        "mat1": "/Game/SparkVision/Materials/MI_Student_DenimLegs.MI_Student_DenimLegs"
    },
    {
        "name": "Cadre_Lathiyal_02",
        "loc": {"x": -2050.0, "y": 1850.0, "z": 150.0},
        "rot": {"pitch": 0.0, "yaw": -75.0, "roll": 0.0},
        "scale": {"x": 1.0, "y": 1.0, "z": 1.0},
        "health": 350.0,
        "damage": 25.0,
        "range": 190.0,
        "mat0": "/Game/SparkVision/Materials/MI_Cadre_Helmet.MI_Cadre_Helmet",
        "mat1": "/Game/SparkVision/Materials/MI_Student_DenimLegs.MI_Student_DenimLegs"
    },
    {
        "name": "Cadre_Lathiyal_03",
        "loc": {"x": -1850.0, "y": 2050.0, "z": 150.0},
        "rot": {"pitch": 0.0, "yaw": -90.0, "roll": 0.0},
        "scale": {"x": 1.0, "y": 1.0, "z": 1.0},
        "health": 350.0,
        "damage": 25.0,
        "range": 190.0,
        "mat0": "/Game/SparkVision/Materials/MI_Cadre_Helmet.MI_Cadre_Helmet",
        "mat1": "/Game/SparkVision/Materials/MI_Student_DenimLegs.MI_Student_DenimLegs"
    }
]

def main():
    print("=" * 70)
    print("SPAWNING AND CONFIGURING CLIMAX CADRE SQUAD")
    print("=" * 70)

    for cadre in CADRE_MEMBERS:
        name = cadre["name"]
        print(f"\nSpawning {name}...")

        # Spawn actor
        res = invoke_tool("add_to_scene_from_class", "editor_toolset.toolsets.scene.SceneTools", {
            "actor_type": {"refPath": "/Script/MyProject.SVHostileOpponent"},
            "name": name,
            "xform": {
                "location": cadre["loc"],
                "rotation": cadre["rot"],
                "scale": cadre["scale"]
            },
            "snap_to_ground": True
        })

        actor_ref = res.get("returnValue", {}).get("refPath")
        if not actor_ref:
            print(f"  Failed to spawn {name}")
            continue

        print(f"  ✓ Spawned at ref: {actor_ref}")

        # Set Actor Label
        try:
            invoke_tool("set_label", "editor_toolset.toolsets.actor.ActorTools", {
                "actor": {"refPath": actor_ref},
                "label": name
            })
        except Exception as e:
            print(f"  Set label notice: {e}")

        # Set Combat Properties (Health, AttackDamage, AttackRange)
        try:
            invoke_tool("set_properties", "editor_toolset.toolsets.object.ObjectTools", {
                "instance": {"refPath": actor_ref},
                "values": json.dumps({
                    "health": cadre["health"],
                    "attackDamage": cadre["damage"],
                    "attackRange": cadre["range"]
                })
            })
            print(f"  ✓ Set stats: Health={cadre['health']}, Damage={cadre['damage']}, Range={cadre['range']}")
        except Exception as e:
            print(f"  Set stats notice: {e}")

        # Set Mesh Materials
        try:
            comps = invoke_tool("get_components", "editor_toolset.toolsets.actor.ActorTools", {
                "actor": {"refPath": actor_ref}
            }).get("returnValue", [])

            mesh_comp = None
            for comp in comps:
                ref = comp.get("refPath", "")
                if "CharacterMesh" in ref or "SkeletalMeshComponent" in ref:
                    mesh_comp = ref
                    break

            if mesh_comp:
                invoke_tool("set_properties", "editor_toolset.toolsets.object.ObjectTools", {
                    "instance": {"refPath": mesh_comp},
                    "values": json.dumps({
                        "overrideMaterials": [
                            {"refPath": cadre["mat0"]},
                            {"refPath": cadre["mat1"]}
                        ]
                    })
                })
                print(f"  ✓ Assigned materials: {cadre['mat0']}, {cadre['mat1']}")
        except Exception as e:
            print(f"  Material assign notice: {e}")

        # Spawn Bamboo Lathi (stick prop) near the cadre member
        try:
            stick_x = cadre["loc"]["x"] + 35.0
            stick_y = cadre["loc"]["y"] - 20.0
            stick_z = cadre["loc"]["z"] + 45.0
            stick_name = f"{name}_BambooLathi"

            stick_res = invoke_tool("add_to_scene_from_class", "editor_toolset.toolsets.scene.SceneTools", {
                "actor_type": {"refPath": "/Script/Engine.StaticMeshActor"},
                "name": stick_name,
                "xform": {
                    "location": {"x": stick_x, "y": stick_y, "z": stick_z},
                    "rotation": {"pitch": 15.0, "yaw": cadre["rot"]["yaw"] + 30.0, "roll": 0.0},
                    "scale": {"x": 0.06, "y": 0.06, "z": 1.45}
                },
                "snap_to_ground": False
            })
            stick_ref = stick_res.get("returnValue", {}).get("refPath")
            if stick_ref:
                invoke_tool("set_label", "editor_toolset.toolsets.actor.ActorTools", {
                    "actor": {"refPath": stick_ref},
                    "label": stick_name
                })
                # Set Cylinder mesh and Bamboo material
                stick_comps = invoke_tool("get_components", "editor_toolset.toolsets.actor.ActorTools", {
                    "actor": {"refPath": stick_ref}
                }).get("returnValue", [])
                sm_comp = None
                for sc in stick_comps:
                    if "StaticMeshComponent" in sc.get("refPath", ""):
                        sm_comp = sc.get("refPath", "")
                        break
                if sm_comp:
                    invoke_tool("set_properties", "editor_toolset.toolsets.object.ObjectTools", {
                        "instance": {"refPath": sm_comp},
                        "values": json.dumps({
                            "staticMesh": {"refPath": "/Engine/BasicShapes/Cylinder.Cylinder"},
                            "overrideMaterials": [{"refPath": "/Game/SparkVision/Materials/MI_Bamboo_Lathi.MI_Bamboo_Lathi"}]
                        })
                    })
                    print(f"  ✓ Spawned and attached Bamboo Lathi weapon: {stick_name}")
        except Exception as e:
            print(f"  Bamboo stick notice: {e}")

    # Save level assets
    try:
        invoke_tool("save_assets", "editor_toolset.toolsets.asset.AssetTools", {
            "asset_paths": []
        })
        print("\n✅ Successfully saved level with Climax Cadre Squad!")
    except Exception as e:
        print(f"Save notice: {e}")

if __name__ == "__main__":
    main()
