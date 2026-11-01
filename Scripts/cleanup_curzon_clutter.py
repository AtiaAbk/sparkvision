#!/usr/bin/env python3
"""
Clean up misplaced trees and foliage actors currently cluttering Curzon Hall
and penetrating its walls.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mcp_client

FOLDERS_TO_CLEAR = [
    "Environment/Arts_Faculty/Foliage",
    "Environment/Fuller_Road/Avenue_Canopy",
    "Environment/Shaheed_Minar/Sanctuary_Trees",
    "Environment/TSC_Raju/Foliage",
    "Environment/The_Mall/Field_Perimeter",
    "Environment/Curzon_Botanical/Bamboo_Groves",
]

def main():
    print("=" * 70)
    print("CLEANING UP MISPLACED TREES & WALL-PENETRATING CLUTTER...")
    print("=" * 70)

    total_removed = 0
    for folder in FOLDERS_TO_CLEAR:
        res = mcp_client.invoke_tool("get_actors_in_folder", "editor_toolset.toolsets.scene.SceneTools", {"folder_path": folder})
        actors = res.get("returnValue", [])
        print(f"Folder {folder}: found {len(actors)} actors to remove")
        for a in actors:
            lbl = mcp_client.invoke_tool("get_label", "editor_toolset.toolsets.actor.ActorTools", {"actor": a}).get("returnValue", "Unknown")
            try:
                mcp_client.invoke_tool("remove_from_scene", "editor_toolset.toolsets.scene.SceneTools", {"actor": a})
                total_removed += 1
                print(f"  Removed: {lbl}")
            except Exception as e:
                print(f"  Failed to remove {lbl}: {e}")

    print("\n" + "=" * 70)
    print(f"CLEANUP COMPLETE: Removed {total_removed} misplaced actors from Curzon Hall area.")
    print("=" * 70)

if __name__ == "__main__":
    main()
