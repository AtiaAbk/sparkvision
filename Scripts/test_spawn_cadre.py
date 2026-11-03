#!/usr/bin/env python3
"""
Test spawning Cadre Leader and inspecting components
"""
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

def main():
    print("Testing add_to_scene_from_class...")
    res = invoke_tool("add_to_scene_from_class", "editor_toolset.toolsets.scene.SceneTools", {
        "actor_type": {"refPath": "/Script/MyProject.SVHostileOpponent"},
        "name": "Cadre_Leader_NoukaCap",
        "xform": {
            "location": {"x": -1850.0, "y": 1750.0, "z": 150.0},
            "rotation": {"pitch": 0.0, "yaw": -90.0, "roll": 0.0},
            "scale": {"x": 1.05, "y": 1.05, "z": 1.05}
        },
        "snap_to_ground": True
    })
    print(f"Spawn result: {res}")
    actor_ref = res.get("returnValue", {}).get("refPath")
    if not actor_ref:
        print("Failed to get actor ref")
        return

    # Get components
    comps = invoke_tool("get_components", "editor_toolset.toolsets.actor.ActorTools", {
        "actor": {"refPath": actor_ref}
    })
    print(f"Components: {json.dumps(comps, indent=2)}")

if __name__ == "__main__":
    main()
