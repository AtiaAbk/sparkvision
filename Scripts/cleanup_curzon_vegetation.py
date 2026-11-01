#!/usr/bin/env python3
"""
Curzon Hall Vegetation Cleanup & Authentic Landscape Alignment Script
1. Identifies and removes all trees, banyans, and shrubs clipping into Curzon Hall's walls or blocking the direct front view.
2. Spawns authentic minimal vegetation matching the user's reference photographs:
   - Two iconic tall Royal Palm trees flanking the central entrance
   - Low trimmed hedge line running in front of the plinth and walkway
   - Clear unobstructed lawn ensuring the entire 128m facade is visible
"""

import json
import subprocess
import os

ENV_PATH = "/Game/SparkVision/Campus/Environment"

def run_mcp(toolset, tool, args):
    res = subprocess.check_output([
        "/Users/atiaoishi/Downloads/sparkvision/Scripts/mcp_client.py",
        "call", toolset, tool, json.dumps(args)
    ])
    return json.loads(res) if res.strip() else {}

def cleanup_clipping_and_blocking_trees():
    print("=" * 70)
    print("AUDITING & REMOVING CLIPPING / OBSTRUCTIVE TREES AROUND CURZON HALL...")
    print("=" * 70)

    # Search for all vegetation actors in scene
    res = run_mcp("editor_toolset.toolsets.scene.SceneTools", "find_actors", {
        "name": "", "tag": "", "collision_channels": []
    })
    actors = res.get("returnValue", res) if isinstance(res, dict) else []
    print(f"Total scene actors found: {len(actors)}")

    # Target actors in Curzon botanical folder or with Curzon vegetation prefixes
    removed_count = 0
    
    # Specific known clipping trees from populate script
    clipping_keywords = [
        "Curzon_Krishnachura_",
        "Curzon_PetalScatter_",
        "Curzon_Radhachura_",
        "Curzon_Banyan_Corner_",
        "Tree_Banyan_Mature",
        "Tree_Raintree_Huge",
        "Tree_Krishnachura_Bloom",
        "Tree_Radhachura_Yellow"
    ]

    for a in actors:
        ref = a.get("refPath", "")
        # Check if this actor is vegetation BEFORE making transform calls
        is_veg = any(k in ref for k in ["Tree", "Foliage", "Krishnachura", "Radhachura", "Banyan", "Raintree", "PetalScatter"])
        if not is_veg:
            continue

        # Get actor location
        try:
            xf_res = run_mcp("editor_toolset.toolsets.actor.ActorTools", "get_actor_transform", {"actor": a})
            xf = xf_res.get("returnValue", xf_res) if isinstance(xf_res, dict) else {}
            loc = xf.get("translation", {})
            x = loc.get("x", 0.0)
            y = loc.get("y", 0.0)
            z = loc.get("z", 0.0)

            # 1. Any tree inside or clipping through building walls (X between -2800 and 800, Y between -6800 and 6800)
            is_clipping = (-2800 <= x <= 800 and -6800 <= y <= 6800)
            
            # 2. Any large tree right in front of the central facade promenade blocking the view (X between -5500 and -2800, |Y| <= 2500)
            is_blocking_front = (-5500 <= x <= -2800 and abs(y) <= 2200)

            if is_clipping or is_blocking_front:
                print(f"  [-] Removing obstructive tree: {ref.split('.')[-1]} at ({x:.1f}, {y:.1f}, {z:.1f}) [clipping={is_clipping}, blocking={is_blocking_front}]")
                run_mcp("editor_toolset.toolsets.scene.SceneTools", "remove_from_scene", {"actor": a})
                removed_count += 1
        except Exception as e:
            pass

    print(f"Removed {removed_count} clipping / blocking vegetation actors.")
    return removed_count

def spawn_authentic_front_landscape():
    print("\n" + "=" * 70)
    print("SPAWNING AUTHENTIC CURZON FRONT LANDSCAPE (MATCHING USER PHOTOS)...")
    print("=" * 70)

    # 1. The Two Iconic Royal Palms Flanking the Central Entrance
    # In user photos: Media 1 & 3 clearly show two tall palms directly flanking the portal
    # Left Palm: X = -3300, Y = -850, Height ~19m
    # Right Palm: X = -3300, Y = +850, Height ~19m (with climbing vine/foliage)
    palm_asset = f"{ENV_PATH}/SM_Tree_Coconut_Palm.SM_Tree_Coconut_Palm"
    
    palms = [
        {"name": "Curzon_Authentic_Palm_Left", "x": -3300.0, "y": -900.0, "z": 20.0, "scale": 1.6, "yaw": 25.0},
        {"name": "Curzon_Authentic_Palm_Right", "x": -3300.0, "y": 900.0, "z": 20.0, "scale": 1.65, "yaw": -35.0},
    ]

    for p in palms:
        try:
            res = run_mcp("editor_toolset.toolsets.scene.SceneTools", "add_to_scene_from_asset", {
                "asset_path": palm_asset,
                "name": p["name"],
                "xform": {
                    "location": {"x": p["x"], "y": p["y"], "z": p["z"]},
                    "rotation": {"pitch": 0.0, "yaw": p["yaw"], "roll": 0.0},
                    "scale": {"x": p["scale"], "y": p["scale"], "z": p["scale"] * 1.2}
                }
            })
            ref = res.get("returnValue", {}).get("refPath", "")
            run_mcp("editor_toolset.toolsets.scene.SceneTools", "set_actor_folder", {
                "actor": {"refPath": ref},
                "folder_path": "Environment/Curzon_Authentic_Landscape"
            })
            print(f"  [+] Spawned iconic Royal Palm: {p['name']} at ({p['x']}, {p['y']})")
        except Exception as e:
            print(f"  Warning spawning palm {p['name']}: {e}")

    # 2. Low Manicured Hedge Line in front of Plinth Pathway
    # In user photos: A neat, low trimmed green bush/hedge runs horizontally across the front lawn
    hedge_asset = f"{ENV_PATH}/SM_Hedge_Manicured_4m.SM_Hedge_Manicured_4m"
    # Front hedge positions spanning from Y = -1600 to +1600 at X = -3500
    hedge_ys = [-1400.0, -1000.0, -600.0, 600.0, 1000.0, 1400.0]
    for idx, hy in enumerate(hedge_ys):
        try:
            res = run_mcp("editor_toolset.toolsets.scene.SceneTools", "add_to_scene_from_asset", {
                "asset_path": hedge_asset,
                "name": f"Curzon_Front_Hedge_{idx+1}",
                "xform": {
                    "location": {"x": -3550.0, "y": hy, "z": 20.0},
                    "rotation": {"pitch": 0.0, "yaw": 0.0, "roll": 0.0},
                    "scale": {"x": 1.0, "y": 1.0, "z": 0.8}
                }
            })
            ref = res.get("returnValue", {}).get("refPath", "")
            run_mcp("editor_toolset.toolsets.scene.SceneTools", "set_actor_folder", {
                "actor": {"refPath": ref},
                "folder_path": "Environment/Curzon_Authentic_Landscape"
            })
            print(f"  [+] Spawned manicured hedge: Curzon_Front_Hedge_{idx+1}")
        except Exception as e:
            print(f"  Warning spawning hedge: {e}")

    print("Authentic front landscape setup complete.")

if __name__ == "__main__":
    cleanup_clipping_and_blocking_trees()
    spawn_authentic_front_landscape()
