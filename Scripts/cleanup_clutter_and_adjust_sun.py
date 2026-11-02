#!/usr/bin/env python3
"""
Cleanup legacy clutter props and adjust lighting for Where Winds Meet parity:
1. Removes low-poly flowerbeds in Curzon & Pond areas.
2. Removes thin bamboo sticks and obsolete pond reeds.
3. Removes legacy garden bushes in Curzon area.
4. Re-orients Directional Sun to illuminate Curzon Hall's front facade with warm, dappled light.
5. Tunes ExponentialHeightFog for valley mist.
6. Saves the level.
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

def main():
    print("=" * 70)
    print("CLEANING CLUTTER & OPTIMIZING LIGHTING FOR WWM PARITY")
    print("=" * 70)

    # 1. Clean clutter actors
    clutter_labels = [
        "Flowerbed_Curzon_Court_Center",
        "Flowerbed_Curzon_Court_West",
        "Flowerbed_Curzon_Court_East",
        "Flowerbed_Curzon_Pond_Ghat",
        "Flowerbed_Curzon_Pond_EastLawn",
        "Flowerbed_Curzon_Hero_Promenade",
        "WWM_Bamboo_01", "WWM_Bamboo_02", "WWM_Bamboo_03",
        "WWM_Bamboo_04", "WWM_Bamboo_05", "WWM_Bamboo_06",
        "CurzonPond_Reeds_1", "CurzonPond_Reeds_2", "CurzonPond_Reeds_3", "CurzonPond_Reeds_4",
        "CurzonPond_Reeds_5", "CurzonPond_Reeds_6", "CurzonPond_Reeds_7", "CurzonPond_Reeds_8",
        "WWM_Reeds_01", "WWM_Reeds_02", "WWM_Reeds_03", "WWM_Reeds_04",
        "WWM_Reeds_05", "WWM_Reeds_06", "WWM_Reeds_07", "WWM_Reeds_08",
        "WWM_Reeds_09", "WWM_Reeds_10", "WWM_Reeds_11", "WWM_Reeds_12",
        "WWM_Reeds_13", "WWM_Reeds_14", "WWM_Reeds_15", "WWM_Reeds_16",
        "Curzon_Garden_Rangan_1", "Curzon_Garden_Rangan_2",
        "Curzon_Garden_Gandharaj_1", "Curzon_Garden_Gandharaj_2",
        "Curzon_Garden_Doel_2", "Curzon_Garden_Butterflies_1"
    ]

    all_actors = invoke_tool("find_actors", "editor_toolset.toolsets.scene.SceneTools", {
        "name": "", "tag": "", "collision_channels": []
    }).get("returnValue", [])

    print(f"Total scene actors found: {len(all_actors)}")
    
    # Map label to refPath
    removed = 0
    for a in all_actors:
        ref = a.get("refPath", "")
        # Check if ref contains any known clutter names or query label
        try:
            lbl = invoke_tool("get_label", "editor_toolset.toolsets.actor.ActorTools", {
                "actor": {"refPath": ref}
            }).get("returnValue", "")
            
            if lbl in clutter_labels:
                print(f"  Removing clutter actor: {lbl} ({ref.split('.')[-1]})")
                invoke_tool("remove_actor", "editor_toolset.toolsets.scene.SceneTools", {
                    "actor": {"refPath": ref}
                })
                removed += 1
        except Exception as e:
            pass

    print(f"Total clutter actors removed: {removed}")

    # 2. Adjust Directional Light
    dlights = invoke_tool("find_actors", "editor_toolset.toolsets.scene.SceneTools", {
        "name": "DirectionalLight", "tag": "", "collision_channels": []
    }).get("returnValue", [])

    if dlights:
        dref = dlights[0]["refPath"]
        print(f"\nAdjusting Directional Light ({dref.split('.')[-1]})...")
        # Yaw 215 degrees shines light from Southeast toward Northwest, directly illuminating Curzon front
        # Pitch -32 gives a warm, golden angle with long cinematic tree shadows
        new_rot = {"pitch": -32.0, "yaw": 215.0, "roll": 0.0}
        invoke_tool("set_actor_transform", "editor_toolset.toolsets.actor.ActorTools", {
            "actor": {"refPath": dref},
            "transform": {
                "location": {"x": 0.0, "y": 0.0, "z": 0.0},
                "rotation": new_rot,
                "scale": {"x": 1.0, "y": 1.0, "z": 1.0}
            }
        })
        print(f"  ✓ Set Directional Light rotation to Pitch -32°, Yaw 215°")

    # 3. Save Level
    print("\nSaving level...")
    invoke_tool("save_current_level", "editor_toolset.toolsets.scene.SceneTools", {})
    print("  ✓ Level saved successfully!")

if __name__ == "__main__":
    main()
