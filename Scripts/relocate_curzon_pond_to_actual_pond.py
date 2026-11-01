#!/usr/bin/env python3
"""
Relocate Curzon Pond elements (Ghat, Lilies, Reeds, Riparian Trees)
from the front lawn to the ACTUAL botanical pond:
Pond bounds: X in [2200, 7400], Y in [-1800, 1800]
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mcp_client

def main():
    print("=" * 70)
    print("RELOCATING CURZON POND ELEMENTS TO ACTUAL BOTANICAL POND...")
    print("=" * 70)

    # 1. Relocate Ghat to West bank of actual pond (X=2350, Y=0, Z=20)
    ghat_actors = mcp_client.invoke_tool("get_actors_in_folder", "editor_toolset.toolsets.scene.SceneTools", {"folder_path": "Environment/Curzon_Pond/Pond_Architecture"}).get("returnValue", [])
    for a in ghat_actors:
        mcp_client.invoke_tool("set_actor_transform", "editor_toolset.toolsets.actor.ActorTools", {
            "actor": a,
            "worldspace": True,
            "xform": {
                "location": {"x": 2350.0, "y": 0.0, "z": 20.0},
                "rotation": {"pitch": 0.0, "yaw": 0.0, "roll": 0.0},
                "scale": {"x": 1.0, "y": 1.0, "z": 1.0}
            }
        })
        print("  Relocated Curzon_Pond_MainGhat to West bank of actual pond")

    # 2. Relocate Water Lilies to the water surface inside actual pond (Z=15)
    lily_coords = [
        {"x": 3400.0, "y": -600.0, "z": 14.0, "scale": 1.2},
        {"x": 4200.0, "y": 700.0, "z": 14.0, "scale": 1.0},
        {"x": 5100.0, "y": -500.0, "z": 14.0, "scale": 1.3},
        {"x": 5800.0, "y": 400.0, "z": 14.0, "scale": 1.1},
        {"x": 3800.0, "y": 300.0, "z": 14.0, "scale": 0.9},
        {"x": 4700.0, "y": -800.0, "z": 14.0, "scale": 1.15},
        {"x": 6200.0, "y": -300.0, "z": 14.0, "scale": 1.0},
        {"x": 6600.0, "y": 500.0, "z": 14.0, "scale": 1.25},
    ]
    lily_actors = mcp_client.invoke_tool("get_actors_in_folder", "editor_toolset.toolsets.scene.SceneTools", {"folder_path": "Environment/Curzon_Pond/Aquatic_Flora"}).get("returnValue", [])
    for idx, a in enumerate(lily_actors):
        c = lily_coords[idx % len(lily_coords)]
        mcp_client.invoke_tool("set_actor_transform", "editor_toolset.toolsets.actor.ActorTools", {
            "actor": a,
            "worldspace": True,
            "xform": {
                "location": {"x": c["x"], "y": c["y"], "z": c["z"]},
                "rotation": {"pitch": 0.0, "yaw": float(idx * 45), "roll": 0.0},
                "scale": {"x": c["scale"], "y": c["scale"], "z": c["scale"]}
            }
        })
    print(f"  Relocated {len(lily_actors)} water lily clusters to actual pond water surface")

    # 3. Relocate Reeds along the shallow margins (North/South banks, Z=18)
    reed_coords = [
        {"x": 2800.0, "y": -1650.0, "z": 18.0},
        {"x": 3600.0, "y": -1700.0, "z": 18.0},
        {"x": 4800.0, "y": -1700.0, "z": 18.0},
        {"x": 6000.0, "y": -1650.0, "z": 18.0},
        {"x": 2800.0, "y": 1650.0, "z": 18.0},
        {"x": 3600.0, "y": 1700.0, "z": 18.0},
        {"x": 4800.0, "y": 1700.0, "z": 18.0},
        {"x": 6000.0, "y": 1650.0, "z": 18.0},
    ]
    reed_actors = mcp_client.invoke_tool("get_actors_in_folder", "editor_toolset.toolsets.scene.SceneTools", {"folder_path": "Environment/Curzon_Pond/Wetland_Reeds"}).get("returnValue", [])
    for idx, a in enumerate(reed_actors):
        c = reed_coords[idx % len(reed_coords)]
        mcp_client.invoke_tool("set_actor_transform", "editor_toolset.toolsets.actor.ActorTools", {
            "actor": a,
            "worldspace": True,
            "xform": {
                "location": {"x": c["x"], "y": c["y"], "z": c["z"]},
                "rotation": {"pitch": 0.0, "yaw": float(idx * 30), "roll": 0.0},
                "scale": {"x": 1.0, "y": 1.0, "z": 1.0}
            }
        })
    print(f"  Relocated {len(reed_actors)} reed clusters to actual pond margins")

    # 4. Relocate Riparian Trees (Jarul and Palms) around the perimeter
    # North bank at Y = 2000, South bank at Y = -2000, East bank at X = 7500
    tree_coords = [
        {"x": 3000.0, "y": -2000.0, "z": 20.0, "yaw": 15.0},
        {"x": 4200.0, "y": -2000.0, "z": 20.0, "yaw": 60.0},
        {"x": 5400.0, "y": -2000.0, "z": 20.0, "yaw": -45.0},
        {"x": 6600.0, "y": -2000.0, "z": 20.0, "yaw": 30.0},
        {"x": 3000.0, "y": 2000.0, "z": 20.0, "yaw": -15.0},
        {"x": 4200.0, "y": 2000.0, "z": 20.0, "yaw": 85.0},
        {"x": 5400.0, "y": 2000.0, "z": 20.0, "yaw": -70.0},
        {"x": 6600.0, "y": 2000.0, "z": 20.0, "yaw": 40.0},
        {"x": 7500.0, "y": -800.0, "z": 20.0, "yaw": 110.0},
        {"x": 7500.0, "y": 0.0, "z": 20.0, "yaw": -90.0},
        {"x": 7500.0, "y": 800.0, "z": 20.0, "yaw": 75.0},
        {"x": 7100.0, "y": 1500.0, "z": 20.0, "yaw": -120.0},
    ]
    tree_actors = mcp_client.invoke_tool("get_actors_in_folder", "editor_toolset.toolsets.scene.SceneTools", {"folder_path": "Environment/Curzon_Pond/Riparian_Trees"}).get("returnValue", [])
    for idx, a in enumerate(tree_actors):
        c = tree_coords[idx % len(tree_coords)]
        mcp_client.invoke_tool("set_actor_transform", "editor_toolset.toolsets.actor.ActorTools", {
            "actor": a,
            "worldspace": True,
            "xform": {
                "location": {"x": c["x"], "y": c["y"], "z": c["z"]},
                "rotation": {"pitch": 0.0, "yaw": c["yaw"], "roll": 0.0},
                "scale": {"x": 1.0, "y": 1.0, "z": 1.0}
            }
        })
    print(f"  Relocated {len(tree_actors)} riparian trees to actual pond perimeter")

    print("\n" + "=" * 70)
    print("POND RELOCATION COMPLETE: Front lawn is now 100% CLEAR of pond elements!")
    print("=" * 70)

if __name__ == "__main__":
    main()
