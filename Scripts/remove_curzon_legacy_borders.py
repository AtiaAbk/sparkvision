#!/usr/bin/env python3
"""
Remove legacy Curzon flowerbed border walls that obstruct views of Curzon Promenade and Pond.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

TARGET_LABELS = [
    "Border_Curzon_Promenade_North",
    "Border_Curzon_Promenade_South",
    "Border_Curzon_Pond_Bank_1",
    "Border_Curzon_Pond_Bank_2",
]

def main():
    print("=" * 70)
    print("REMOVING LEGACY CURZON BORDER WALLS")
    print("=" * 70)

    res = invoke_tool("find_actors", "editor_toolset.toolsets.scene.SceneTools", {
        "name": "Border_Curzon", "tag": "", "collision_channels": []
    })
    actors = res.get("returnValue", [])
    print(f"Found {len(actors)} matching actors.")

    removed = 0
    for a in actors:
        lbl = invoke_tool("get_label", "editor_toolset.toolsets.actor.ActorTools", {
            "actor": a
        }).get("returnValue", "")
        if lbl in TARGET_LABELS:
            print(f"  Removing {lbl} ({a.get('refPath')})...")
            invoke_tool("remove_from_scene", "editor_toolset.toolsets.scene.SceneTools", {
                "actor": a
            })
            removed += 1

    print(f"✓ Removed {removed} legacy border actors.")

    # Save level assets
    print("Saving dirty assets...")
    invoke_tool("save_assets", "editor_toolset.toolsets.asset.AssetTools", {"asset_paths": []})
    print("✓ Level saved.")

if __name__ == "__main__":
    main()
