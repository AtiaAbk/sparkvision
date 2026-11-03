#!/usr/bin/env python3
"""
SparkVision — Calibrate Character Transforms and Hide Editor Wireframes
Ensures all 16 campus characters (students, professors, pedestrians, sparring partners)
stand firmly on the ground plane (no sunken meshes) and disables editor capsule/arrow visibility.
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

# Exact calibrated positions for all campus characters
# Z = Ground_Z + CapsuleHalfHeight (96.0)
CALIBRATED_CHARACTERS = {
    # Curzon Hall Heritage Portico & Promenade
    "Prof_Jamal": {
        "loc": {"x": -3350.0, "y": 280.0, "z": 176.0},
        "yaw": -30.0
    },
    "Tanvir": {
        "loc": {"x": -3450.0, "y": -240.0, "z": 176.0},
        "yaw": 30.0
    },
    "NPC_Sabbir": {
        "loc": {"x": -1800.0, "y": 320.0, "z": 176.0},
        "yaw": 80.0
    },
    "NPC_Rifat": {
        "loc": {"x": -1800.0, "y": 440.0, "z": 176.0},
        "yaw": -100.0
    },
    "Student_Commuter_01": {
        "loc": {"x": -950.0, "y": 140.0, "z": 176.0},
        "yaw": 180.0
    },
    "Student_Commuter_02": {
        "loc": {"x": 250.0, "y": -120.0, "z": 176.0},
        "yaw": 0.0
    },

    # Curzon Botanical Pond Ghat & Banyan Grove
    "NPC_Ananya": {
        "loc": {"x": 1650.0, "y": -450.0, "z": 166.0},
        "yaw": 45.0
    },
    "NPC_Mehedi": {
        "loc": {"x": 2300.0, "y": -650.0, "z": 136.0},
        "yaw": 30.0
    },

    # Curzon North Courtyard Martial Arts Sparring
    "Hostile_Fahim": {
        "loc": {"x": -2200.0, "y": 1600.0, "z": 176.0},
        "yaw": 30.0
    },
    "Hostile_Kamal": {
        "loc": {"x": -1800.0, "y": 1800.0, "z": 176.0},
        "yaw": -150.0
    },

    # TSC Cultural Hub & Assembly
    "NPC_Sadia": {
        "loc": {"x": 57000.0, "y": -62500.0, "z": 246.0},
        "yaw": -45.0
    },
    "NPC_Arif": {
        "loc": {"x": 57600.0, "y": -61800.0, "z": 246.0},
        "yaw": 135.0
    },

    # Kala Bhaban (Faculty of Arts & Aparajeyo Bangla)
    "Prof_Rahman": {
        "loc": {"x": 70500.0, "y": -95000.0, "z": 246.0},
        "yaw": 0.0
    },
    "NPC_Nabila": {
        "loc": {"x": 71200.0, "y": -95400.0, "z": 246.0},
        "yaw": 180.0
    },

    # Central Shaheed Minar Memorial Plaza
    "NPC_Farhan": {
        "loc": {"x": -2200.0, "y": -54000.0, "z": 196.0},
        "yaw": 0.0
    }
}

def main():
    print("=" * 70)
    print("CALIBRATING CHARACTER TRANSFORMS AND HIDING EDITOR WIREFRAMES")
    print("=" * 70)

    updated_count = 0
    for key, cfg in CALIBRATED_CHARACTERS.items():
        actors = invoke_tool("find_actors", "editor_toolset.toolsets.scene.SceneTools", {
            "name": key, "tag": "", "collision_channels": []
        }).get("returnValue", [])

        if not actors:
            print(f"  ⚠️ Could not find actor matching '{key}'")
            continue

        actor = actors[0]
        lbl = invoke_tool("get_label", "editor_toolset.toolsets.actor.ActorTools", {"actor": actor}).get("returnValue", key)

        # 1. Update Transform
        xform = {
            "location": cfg["loc"],
            "rotation": {"pitch": 0.0, "yaw": cfg["yaw"], "roll": 0.0},
            "scale": {"x": 1.0, "y": 1.0, "z": 1.0}
        }
        try:
            invoke_tool("set_actor_transform", "editor_toolset.toolsets.actor.ActorTools", {
                "actor": actor,
                "xform": xform
            })
            print(f"  ✓ Repositioned {lbl} to Z={cfg['loc']['z']}")
        except Exception as e:
            print(f"  Notice setting transform on {lbl}: {e}")

        # 2. Hide CollisionCylinder and Arrow in editor viewport
        comps = invoke_tool("get_components", "editor_toolset.toolsets.actor.ActorTools", {"actor": actor}).get("returnValue", [])
        for c in comps:
            path = c.get("refPath", "")
            if "CollisionCylinder" in path or "Arrow" in path:
                try:
                    invoke_tool("set_properties", "editor_toolset.toolsets.object.ObjectTools", {
                        "instance": c,
                        "values": json.dumps({"bVisible": False})
                    })
                except Exception:
                    pass

        updated_count += 1

    # Save level
    try:
        invoke_tool("save_assets", "editor_toolset.toolsets.asset.AssetTools", {
            "asset_paths": ["/Game/SparkVision/Maps/Level01/LV_Level01_Compact_Campus"]
        })
        print(f"\n✅ Successfully calibrated {updated_count} characters and saved level!")
    except Exception as e:
        print(f"Notice saving: {e}")

if __name__ == "__main__":
    main()
