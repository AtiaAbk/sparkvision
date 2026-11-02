#!/usr/bin/env python3
"""
Purge all remaining legacy low-poly foliage, floating walkway tiles,
stone lanterns, and hedges from Curzon Hall & Promenade area.
Only pristine Where Winds Meet assets will remain.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

PURGE_LABELS = [
    # 16 Stone lanterns on walkway/grass
    "WWM_StoneLantern_01", "WWM_StoneLantern_02", "WWM_StoneLantern_03", "WWM_StoneLantern_04",
    "WWM_StoneLantern_05", "WWM_StoneLantern_06", "WWM_StoneLantern_07", "WWM_StoneLantern_08",
    "WWM_StoneLantern_09", "WWM_StoneLantern_10", "WWM_StoneLantern_11", "WWM_StoneLantern_12",
    "WWM_StoneLantern_13", "WWM_StoneLantern_14", "WWM_StoneLantern_15", "WWM_StoneLantern_16",
    
    # Floating walkway tiles
    "Paved_Walkway_Curzon_To_Gate_1", "Paved_Walkway_Curzon_To_Gate_2",
    "Paved_Walkway_Curzon_To_Gate_3", "Paved_Walkway_Curzon_To_Gate_4",
    "Paved_Walkway_Curzon_To_Gate_5",

    # Legacy low-poly trees in Curzon / Pond area
    "Curzon_Forecourt_Banyan_South", "Curzon_Forecourt_Banyan_North",
    "CurzonPond_South_Banyan_01", "CurzonPond_South_Banyan_02",
    "CurzonPond_South_Banyan_03", "CurzonPond_South_Banyan_04",
    "Curzon_Wing_Krishnachura_East", "Curzon_Wing_Krishnachura_West",
    "Curzon_CentralLawn_Krishnachura_1", "Curzon_CentralLawn_Krishnachura_2",
    "Curzon_Promenade_Krishnachura_South", "Curzon_Promenade_Krishnachura_North",
    "CurzonPond_Palm_1", "CurzonPond_Palm_2", "CurzonPond_Palm_3",
    "CurzonPond_Palm_4", "CurzonPond_Palm_5", "CurzonPond_Palm_6",
    "Curzon_Authentic_Palm_Left", "Curzon_Authentic_Palm_Right",
    "Curzon_Wing_Radhachura_East", "Curzon_Wing_Radhachura_West",

    # Legacy hedges & parterres
    "Curzon_Authentic_Hedge_1", "Curzon_Authentic_Hedge_2",
    "Curzon_Authentic_Hedge_3", "Curzon_Authentic_Hedge_4",
    "Curzon_Parterre_Hedge_1", "Curzon_Parterre_Hedge_2",
    "Curzon_Promenade_Hedge_North_01", "Curzon_Promenade_Hedge_North_02",
    "Curzon_Promenade_Hedge_South_01", "Curzon_Promenade_Hedge_South_02",
]

def main():
    print("=" * 70)
    print("PURGING REMAINING LEGACY CLUTTER IN CURZON PROMENADE & POND")
    print("=" * 70)

    all_actors = invoke_tool("find_actors", "editor_toolset.toolsets.scene.SceneTools", {
        "name": "", "tag": "", "collision_channels": []
    }).get("returnValue", [])

    print(f"Scanning {len(all_actors)} actors in level...")
    
    purged = 0
    for a in all_actors:
        ref = a.get("refPath", "")
        try:
            lbl = invoke_tool("get_label", "editor_toolset.toolsets.actor.ActorTools", {
                "actor": {"refPath": ref}
            }).get("returnValue", "")
            
            if lbl in PURGE_LABELS:
                print(f"  Purging: {lbl:35} ({ref.split('.')[-1]})")
                invoke_tool("remove_from_scene", "editor_toolset.toolsets.scene.SceneTools", {
                    "actor": {"refPath": ref}
                })
                purged += 1
        except Exception:
            pass

    print(f"\n✓ Successfully purged {purged} legacy actors!")

    # Fix Lumen surface cache warning
    try:
        invoke_tool("ExecuteConsoleCommand", "EditorToolset.EditorAppToolset", {
            "command": "r.LumenScene.SurfaceCache.AtlasSize 8192"
        })
        print("✓ Scaled Lumen surface cache atlas size to 8192.")
    except Exception as e:
        print(f"Notice: {e}")

    # Save dirty assets
    invoke_tool("save_assets", "editor_toolset.toolsets.asset.AssetTools", {"asset_paths": []})
    print("✓ Level saved to disk!")

if __name__ == "__main__":
    main()
