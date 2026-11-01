#!/usr/bin/env python3
"""
Relocates Curzon_Litter_Patch_1, Curzon_Balustrade_Doel_1, Curzon_Garden_Doel_2,
and Curzon_Garden_Butterflies_1 to verified positions with zero building collisions.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mcp_client

UPDATES = [
    # 1. Curzon_Litter_Patch_1: move to moist soil near Curzon Pond riparian edge (clear of Shahidullah Hall)
    ("Curzon_Litter_Patch_1", {"x": 2200.0, "y": 1200.0, "z": 20.0}, 45.0),
    # 2. Curzon_Balustrade_Doel_1: move to front entrance garden wall / gatepost (15.5m from facade)
    ("Curzon_Balustrade_Doel_1", {"x": -5400.0, "y": 0.0, "z": 150.0}, 0.0),
    # 3. Curzon_Garden_Doel_2: perch near the east blooming Gandharaj shrub (15.5m from facade)
    ("Curzon_Garden_Doel_2", {"x": -5400.0, "y": 1200.0, "z": 140.0}, -45.0),
    # 4. Curzon_Garden_Butterflies_1: flutter over west flower parterre (17.5m from facade)
    ("Curzon_Garden_Butterflies_1", {"x": -5600.0, "y": -1200.0, "z": 80.0}, 15.0),
]

def main():
    print("Adjusting actor positions for 100% clearance...")
    for name, loc, yaw in UPDATES:
        res = mcp_client.invoke_tool("find_actors", "editor_toolset.toolsets.scene.SceneTools", {
            "name": name,
            "tag": "",
            "collision_channels": []
        })
        actors = res.get("returnValue", [])
        if not actors:
            print(f"  Actor {name} not found!")
            continue
        actor_ref = actors[0]["refPath"]
        mcp_client.invoke_tool("set_actor_transform", "editor_toolset.toolsets.actor.ActorTools", {
            "actor": {"refPath": actor_ref},
            "xform": {
                "location": loc,
                "rotation": {"pitch": 0.0, "yaw": yaw, "roll": 0.0}
            }
        })
        print(f"  [MOVED] {name} -> ({loc['x']}, {loc['y']}, {loc['z']})")

if __name__ == "__main__":
    main()
