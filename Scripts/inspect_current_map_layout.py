#!/usr/bin/env python3
"""
Inspect Current Map Layout in LV_Campus_Blockout using invoke_tool
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from mcp_client import invoke_tool

def main():
    print("Inspecting current map layout...")
    folders_data = invoke_tool("get_folders", "editor_toolset.toolsets.scene.SceneTools")
    folders = folders_data.get("returnValue", [])
    print(f"Total Folders: {len(folders)}")

    inventory = {}

    for fld in folders:
        actors_data = invoke_tool("get_actors_in_folder", "editor_toolset.toolsets.scene.SceneTools", {
            "folder_path": fld,
            "recursive": False
        })
        actors = actors_data.get("returnValue", [])
        if not actors:
            continue
            
        inventory[fld] = []
        for a in actors:
            t_data = invoke_tool("get_actor_transform", "editor_toolset.toolsets.actor.ActorTools", {
                "actor": a
            })
            loc = t_data.get("returnValue", {}).get("location", {})
            rot = t_data.get("returnValue", {}).get("rotation", {})
            scale = t_data.get("returnValue", {}).get("scale", {})
            
            l_data = invoke_tool("get_label", "editor_toolset.toolsets.actor.ActorTools", {
                "actor": a
            })
            label = l_data.get("returnValue", a["refPath"].split(".")[-1])
            
            inventory[fld].append({
                "label": label,
                "refPath": a["refPath"],
                "location": loc,
                "rotation": rot,
                "scale": scale
            })
        print(f"  Folder '{fld}': {len(inventory[fld])} actors")
        
    out_path = "/Users/atiaoishi/Downloads/sparkvision/Documentation/WorldCorrection/original_campus_actors.json"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(inventory, f, indent=2)
    print(f"\nSaved {sum(len(v) for v in inventory.values())} actors to {out_path}")

if __name__ == "__main__":
    main()
