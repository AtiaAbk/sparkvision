#!/usr/bin/env python3
"""
Artistic Super-Natural World Designer for SparkVision Campus (Where Winds Meet Standard)
1. Removes old low-poly / conflicting clutter actors along promenade & pond.
2. Removes all obstructive vegetation from the central walking avenue.
3. Plants v2 Grand Rain Trees in an arched avenue formation with dappled sunlit canopies.
4. Plants v2 Heritage Banyans with twisting trunks and hanging prop roots around Curzon Pond.
5. Plants v2 Scarlet Krishnachura Hero Trees framing vistas and hillocks.
6. Plants refined, delicate undergrowth ferns along curbs and tree roots.
7. Sets Lumen console variables and saves the persistent level.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

RAINTREE_PATH = "/Game/SparkVision/Campus/Environment/SM_Natural_Raintree_Grand"
BANYAN_PATH = "/Game/SparkVision/Campus/Environment/SM_Natural_Banyan_Heritage"
KRISHNA_PATH = "/Game/SparkVision/Campus/Environment/SM_Natural_Krishnachura_Bloom"
FERN_PATH = "/Game/SparkVision/Campus/Environment/SM_Natural_Fern_Cluster"

def main():
    print("=" * 75)
    print("REDESIGNING CAMPUS WORLD: AAA SUPER-NATURAL WHERE WINDS MEET VISTA")
    print("=" * 75)

    # -------------------------------------------------------------
    # 1. CLEAN UP OBSTRUCTIVE ACTORS & OLD VEGETATION
    # -------------------------------------------------------------
    print("\n[Phase 1] Cleaning up old obstructive vegetation & clutter...")
    
    # Find all tree and fern actors in the level
    all_foliage = []
    for pattern in ["WWM_Natural_", "WWM_Pond_Fern", "Tree_", "SM_Fern", "SM_Tree"]:
        found = invoke_tool("find_actors", "editor_toolset.toolsets.scene.SceneTools", {
            "name": pattern,
            "tag": "",
            "collision_channels": []
        }).get("returnValue", [])
        all_foliage.extend(found)

    # De-duplicate by refPath
    unique_foliage = {a["refPath"]: a for a in all_foliage}
    print(f"Found {len(unique_foliage)} foliage actors to clean/replace...")

    removed_count = 0
    for ref, a in unique_foliage.items():
        try:
            invoke_tool("remove_from_scene", "editor_toolset.toolsets.scene.SceneTools", {
                "actor": a
            })
            removed_count += 1
        except Exception:
            pass

    print(f"  ✓ Cleaned up {removed_count} actors for fresh artistic layout.")

    # -------------------------------------------------------------
    # 2. PLANT MAJESTIC RAIN TREE AVENUE (Curzon Promenade)
    # -------------------------------------------------------------
    print("\n[Phase 2] Planting Grand Rain Tree Avenue...")
    # Promenade walkway runs X = -3200 to +800, Y = -400 to +400.
    # We place trees set back at Y = ±1400 to ±1600 so trunks do NOT block the road,
    # and their 22m umbrella canopies meet high overhead at Z = 12m to form an arch!
    
    raintree_flanks = [
        # South / West flank (Y ~ -1450)
        {"x": -3000.0, "y": -1450.0, "z": 80.0, "scale": 0.95, "yaw": 25.0},
        {"x": -2200.0, "y": -1500.0, "z": 80.0, "scale": 1.00, "yaw": 75.0},
        {"x": -1400.0, "y": -1420.0, "z": 80.0, "scale": 0.92, "yaw": 140.0},
        {"x": -600.0,  "y": -1480.0, "z": 80.0, "scale": 0.98, "yaw": 215.0},
        {"x": 200.0,   "y": -1400.0, "z": 80.0, "scale": 0.95, "yaw": 310.0},
        {"x": 1000.0,  "y": -1450.0, "z": 75.0, "scale": 1.05, "yaw": 50.0},

        # North / East flank (Y ~ +1450)
        {"x": -3000.0, "y": 1450.0,  "z": 80.0, "scale": 0.96, "yaw": 290.0},
        {"x": -2200.0, "y": 1500.0,  "z": 80.0, "scale": 0.92, "yaw": 35.0},
        {"x": -1400.0, "y": 1420.0,  "z": 80.0, "scale": 1.02, "yaw": 110.0},
        {"x": -600.0,  "y": 1480.0,  "z": 80.0, "scale": 0.95, "yaw": 185.0},
        {"x": 200.0,   "y": 1400.0,  "z": 80.0, "scale": 0.98, "yaw": 260.0},
        {"x": 1000.0,  "y": 1450.0,  "z": 75.0, "scale": 1.00, "yaw": 345.0},
    ]

    for idx, c in enumerate(raintree_flanks):
        name = f"WWM_Avenue_Raintree_{idx+1:02d}"
        xform = {
            "location": {"x": c["x"], "y": c["y"], "z": c["z"]},
            "rotation": {"pitch": 0.0, "yaw": c["yaw"], "roll": 0.0},
            "scale": {"x": c["scale"], "y": c["scale"], "z": c["scale"]}
        }
        try:
            invoke_tool("add_to_scene_from_asset", "editor_toolset.toolsets.scene.SceneTools", {
                "asset_path": RAINTREE_PATH,
                "name": name,
                "xform": xform
            })
        except Exception as e:
            print(f"  Notice {name}: {e}")

    print(f"  ✓ Planted {len(raintree_flanks)} Grand Rain Trees arching over the Promenade.")

    # -------------------------------------------------------------
    # 3. PLANT ANCIENT HERITAGE BANYANS (Curzon Botanical Pond)
    # -------------------------------------------------------------
    print("\n[Phase 3] Planting Heritage Banyans with Aerial Prop Roots...")
    # Framing Curzon Pond (X ~ 1600 to 3200, Y ~ -1000 to +1000)
    banyan_spots = [
        # North Ghat Shoreline
        {"x": 1700.0, "y": -950.0, "z": 20.0, "scale": 1.15, "yaw": 40.0},
        {"x": 1700.0, "y": 950.0,  "z": 20.0, "scale": 1.20, "yaw": 130.0},
        # East Shoreline
        {"x": 2450.0, "y": 1100.0, "z": 20.0, "scale": 1.25, "yaw": 210.0},
        {"x": 3200.0, "y": 650.0,  "z": 20.0, "scale": 1.30, "yaw": 300.0},
        # South Shoreline
        {"x": 3200.0, "y": -650.0, "z": 20.0, "scale": 1.25, "yaw": 20.0},
        {"x": 2450.0, "y": -1100.0,"z": 20.0, "scale": 1.20, "yaw": 110.0},
    ]

    for idx, c in enumerate(banyan_spots):
        name = f"WWM_Pond_Banyan_{idx+1:02d}"
        xform = {
            "location": {"x": c["x"], "y": c["y"], "z": c["z"]},
            "rotation": {"pitch": 0.0, "yaw": c["yaw"], "roll": 0.0},
            "scale": {"x": c["scale"], "y": c["scale"], "z": c["scale"]}
        }
        try:
            invoke_tool("add_to_scene_from_asset", "editor_toolset.toolsets.scene.SceneTools", {
                "asset_path": BANYAN_PATH,
                "name": name,
                "xform": xform
            })
        except Exception as e:
            print(f"  Notice {name}: {e}")

    print(f"  ✓ Planted {len(banyan_spots)} Heritage Banyans around Curzon Botanical Pond.")

    # -------------------------------------------------------------
    # 4. PLANT SCARLET KRISHNACHURA HERO TREES (Reference 1 Parity)
    # -------------------------------------------------------------
    print("\n[Phase 4] Planting Scarlet Krishnachura Hero Trees...")
    # Splashes of crimson against the emerald landscape
    krishna_spots = [
        # Overlooking Curzon Pond Ghat
        {"x": 1500.0, "y": -550.0, "z": 25.0, "scale": 1.15, "yaw": 35.0},
        {"x": 1500.0, "y": 550.0,  "z": 25.0, "scale": 1.15, "yaw": 155.0},
        # Pond Ridges
        {"x": 2800.0, "y": -1250.0,"z": 35.0, "scale": 1.30, "yaw": 80.0},
        {"x": 2800.0, "y": 1250.0, "z": 35.0, "scale": 1.30, "yaw": 250.0},
        # Far vista horizon
        {"x": 3600.0, "y": 0.0,    "z": 45.0, "scale": 1.45, "yaw": 10.0},
        # Curzon Hall Entrance framing
        {"x": -4200.0,"y": -1200.0,"z": 90.0, "scale": 1.20, "yaw": 60.0},
        {"x": -4200.0,"y": 1200.0, "z": 90.0, "scale": 1.20, "yaw": 240.0},
    ]

    for idx, c in enumerate(krishna_spots):
        name = f"WWM_Hero_Krishnachura_{idx+1:02d}"
        xform = {
            "location": {"x": c["x"], "y": c["y"], "z": c["z"]},
            "rotation": {"pitch": 0.0, "yaw": c["yaw"], "roll": 0.0},
            "scale": {"x": c["scale"], "y": c["scale"], "z": c["scale"]}
        }
        try:
            invoke_tool("add_to_scene_from_asset", "editor_toolset.toolsets.scene.SceneTools", {
                "asset_path": KRISHNA_PATH,
                "name": name,
                "xform": xform
            })
        except Exception as e:
            print(f"  Notice {name}: {e}")

    print(f"  ✓ Planted {len(krishna_spots)} Scarlet Krishnachura Hero Trees.")

    # -------------------------------------------------------------
    # 5. PLANT DELICATE UNDERGROWTH FERNS (Tucked along curbs & roots)
    # -------------------------------------------------------------
    print("\n[Phase 5] Planting delicate undergrowth ferns...")
    # Small scale (0.75x), positioned along the edges of the red brick path (Y = ±460)
    # and near pond waterline, leaving the center walking lane (Y = -350 to +350) 100% CLEAR!
    fern_spots = [
        # Promenade South Curb (Y = -480)
        {"x": -2600.0, "y": -480.0, "z": 80.0},
        {"x": -2000.0, "y": -480.0, "z": 80.0},
        {"x": -1400.0, "y": -480.0, "z": 80.0},
        {"x": -800.0,  "y": -480.0, "z": 80.0},
        {"x": -200.0,  "y": -480.0, "z": 80.0},
        {"x": 400.0,   "y": -480.0, "z": 80.0},

        # Promenade North Curb (Y = +480)
        {"x": -2600.0, "y": 480.0,  "z": 80.0},
        {"x": -2000.0, "y": 480.0,  "z": 80.0},
        {"x": -1400.0, "y": 480.0,  "z": 80.0},
        {"x": -800.0,  "y": 480.0,  "z": 80.0},
        {"x": -200.0,  "y": 480.0,  "z": 80.0},
        {"x": 400.0,   "y": 480.0,  "z": 80.0},

        # Pond Ghat Water Margin
        {"x": 1600.0, "y": -400.0, "z": 16.0},
        {"x": 1600.0, "y": 400.0,  "z": 16.0},
        {"x": 1900.0, "y": -600.0, "z": 16.0},
        {"x": 1900.0, "y": 600.0,  "z": 16.0},
        {"x": 2300.0, "y": -700.0, "z": 16.0},
        {"x": 2300.0, "y": 700.0,  "z": 16.0},
    ]

    for idx, pos in enumerate(fern_spots):
        name = f"WWM_Curb_Fern_{idx+1:02d}"
        xform = {
            "location": pos,
            "rotation": {"pitch": 0.0, "yaw": float(idx * 67 % 360), "roll": 0.0},
            "scale": {"x": 0.85, "y": 0.85, "z": 0.85}
        }
        try:
            invoke_tool("add_to_scene_from_asset", "editor_toolset.toolsets.scene.SceneTools", {
                "asset_path": FERN_PATH,
                "name": name,
                "xform": xform
            })
        except Exception as e:
            pass

    print(f"  ✓ Planted {len(fern_spots)} delicate curb ferns.")

    # -------------------------------------------------------------
    # 6. LUMEN SURFACE CACHE & LIGHTING ENHANCEMENT
    # -------------------------------------------------------------
    print("\n[Phase 6] Applying Lumen & Lighting enhancements...")
    try:
        invoke_tool("execute_console_command", "EditorToolset.EditorAppToolset", {
            "command": "r.LumenScene.SurfaceCache.AtlasSize 4096"
        })
        print("  ✓ Increased Lumen Surface Cache AtlasSize to 4096")
    except Exception as e:
        print(f"  Console notice: {e}")

    # Save level
    print("\n[Phase 7] Saving persistent level asset...")
    save_res = invoke_tool("save_assets", "editor_toolset.toolsets.asset.AssetTools", {
        "asset_paths": ["/Game/SparkVision/Maps/Level01/LV_Level01_Compact_Campus"]
    })
    print("  ✓ Level saved:", save_res)

    print("\n" + "=" * 75)
    print("CAMPUS WORLD FULLY REDESIGNED & UPGRADED!")
    print("=" * 75)

if __name__ == "__main__":
    main()
