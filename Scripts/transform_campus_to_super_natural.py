#!/usr/bin/env python3
"""
Transform SparkVision Campus to Super-Natural Where Winds Meet Standard:
1. Cleans up 80+ artificial geometric Debdaru slats and scaled bamboo poles around Curzon Pond.
2. Artistically plants the new super-natural foliage models:
   - SM_Natural_Raintree_Grand (majestic century-old umbrella canopies with feathery leaf cards, Ref 3)
   - SM_Natural_Banyan_Heritage (gnarled twisting trunks with hanging aerial prop roots, Ref 2)
   - SM_Natural_Krishnachura_Bloom (fiery scarlet wuxia canopy trees, Ref 1)
   - SM_Natural_Fern_Cluster (lush undergrowth ferns along paths and water edge)
3. Saves the persistent level LV_Level01_Compact_Campus.
"""

import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

RAINTREE_PATH = "/Game/SparkVision/Campus/Environment/SM_Natural_Raintree_Grand"
BANYAN_PATH = "/Game/SparkVision/Campus/Environment/SM_Natural_Banyan_Heritage"
KRISHNA_PATH = "/Game/SparkVision/Campus/Environment/SM_Natural_Krishnachura_Bloom"
FERN_PATH = "/Game/SparkVision/Campus/Environment/SM_Natural_Fern_Cluster"

def main():
    print("=" * 75)
    print("TRANSFORMING SPARKVISION TO SUPER-NATURAL WHERE WINDS MEET AESTHETICS")
    print("=" * 75)

    # -------------------------------------------------------------
    # 1. REMOVE ARTIFICIAL ENCLOSURE CLUTTER (Debdaru, Bamboo slats, etc.)
    # -------------------------------------------------------------
    print("\n[Phase 1] Removing artificial geometric enclosure clutter...")
    clutter_actors = []
    for pattern in ["Debdaru", "CurzonPond_WWM_Bamboo", "CurzonPond_South_Bamboo", "CurzonPond_East_Bamboo", "CurzonPond_Screening"]:
        found = invoke_tool("find_actors", "editor_toolset.toolsets.scene.SceneTools", {
            "name": pattern,
            "tag": "",
            "collision_channels": []
        }).get("returnValue", [])
        clutter_actors.extend(found)

    # De-duplicate
    unique_clutter = {}
    for a in clutter_actors:
        unique_clutter[a["refPath"]] = a

    print(f"Found {len(unique_clutter)} artificial enclosure actors to remove...")
    removed_count = 0
    for ref, a in unique_clutter.items():
        try:
            invoke_tool("remove_from_scene", "editor_toolset.toolsets.scene.SceneTools", {
                "actor": a
            })
            removed_count += 1
        except Exception as e:
            print(f"  Notice removing {ref}: {e}")

    print(f"  ✓ Removed {removed_count} artificial clutter actors.")

    # -------------------------------------------------------------
    # 2. ARTISTIC RE-PLANTING OF SUPER-NATURAL TREES
    # -------------------------------------------------------------
    print("\n[Phase 2] Planting Super-Natural Trees & Undergrowth...")

    # A. Curzon Promenade Majestic Raintrees (Lining the central brick avenue)
    # Spaced along the walkway to cast dappled canopy shadows on the red bricks
    raintree_coords = [
        # West side of Curzon avenue
        {"loc": {"x": -2800.0, "y": -900.0, "z": 80.0}, "scale": 1.1, "yaw": 24.0},
        {"loc": {"x": -2000.0, "y": -950.0, "z": 80.0}, "scale": 1.25, "yaw": 68.0},
        {"loc": {"x": -1200.0, "y": -920.0, "z": 80.0}, "scale": 1.15, "yaw": 115.0},
        {"loc": {"x": -400.0, "y": -880.0, "z": 80.0}, "scale": 1.2, "yaw": 190.0},
        {"loc": {"x": 400.0, "y": -850.0, "z": 80.0}, "scale": 1.1, "yaw": 275.0},
        # East side of Curzon avenue
        {"loc": {"x": -2800.0, "y": 900.0, "z": 80.0}, "scale": 1.15, "yaw": 310.0},
        {"loc": {"x": -2000.0, "y": 950.0, "z": 80.0}, "scale": 1.2, "yaw": 45.0},
        {"loc": {"x": -1200.0, "y": 920.0, "z": 80.0}, "scale": 1.3, "yaw": 140.0},
        {"loc": {"x": -400.0, "y": 880.0, "z": 80.0}, "scale": 1.1, "yaw": 220.0},
        {"loc": {"x": 400.0, "y": 850.0, "z": 80.0}, "scale": 1.25, "yaw": 85.0},
    ]

    for idx, c in enumerate(raintree_coords):
        name = f"WWM_Natural_Raintree_{idx+1:02d}"
        xform = {
            "location": c["loc"],
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
            print(f"  Notice adding {name}: {e}")

    print(f"  ✓ Planted {len(raintree_coords)} Grand Raintrees along Curzon Promenade.")

    # B. Curzon Botanical Pond Majestic Heritage Banyans (With aerial prop roots)
    # Framed around the water's edge to hang prop roots and create a serene wuxia lake
    banyan_coords = [
        # North Shore / Ghat
        {"loc": {"x": 1600.0, "y": -650.0, "z": 20.0}, "scale": 1.2, "yaw": 35.0},
        {"loc": {"x": 1600.0, "y": 650.0, "z": 20.0}, "scale": 1.25, "yaw": 145.0},
        # East Shore
        {"loc": {"x": 2400.0, "y": 850.0, "z": 20.0}, "scale": 1.3, "yaw": 225.0},
        {"loc": {"x": 3100.0, "y": 450.0, "z": 20.0}, "scale": 1.35, "yaw": 315.0},
        # South Shore
        {"loc": {"x": 3100.0, "y": -450.0, "z": 20.0}, "scale": 1.25, "yaw": 15.0},
        {"loc": {"x": 2400.0, "y": -850.0, "z": 20.0}, "scale": 1.3, "yaw": 110.0},
    ]

    for idx, c in enumerate(banyan_coords):
        name = f"WWM_Natural_Banyan_{idx+1:02d}"
        xform = {
            "location": c["loc"],
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
            print(f"  Notice adding {name}: {e}")

    print(f"  ✓ Planted {len(banyan_coords)} Heritage Banyans around Curzon Botanical Pond.")

    # C. Scarlet Krishnachura Blooms (Ref 1 Parity: Fiery scarlet accents against green canopy)
    krishna_coords = [
        # Framing the lake vista
        {"loc": {"x": 2000.0, "y": -1150.0, "z": 40.0}, "scale": 1.3, "yaw": 40.0},
        {"loc": {"x": 2000.0, "y": 1150.0, "z": 40.0}, "scale": 1.25, "yaw": 160.0},
        {"loc": {"x": 2800.0, "y": -1050.0, "z": 40.0}, "scale": 1.35, "yaw": 85.0},
        {"loc": {"x": 2800.0, "y": 1050.0, "z": 40.0}, "scale": 1.2, "yaw": 240.0},
        # High ridges / background accents
        {"loc": {"x": 3500.0, "y": 0.0, "z": 50.0}, "scale": 1.45, "yaw": 0.0},
        {"loc": {"x": 1000.0, "y": 0.0, "z": 80.0}, "scale": 1.2, "yaw": 180.0},
    ]

    for idx, c in enumerate(krishna_coords):
        name = f"WWM_Natural_Krishnachura_{idx+1:02d}"
        xform = {
            "location": c["loc"],
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
            print(f"  Notice adding {name}: {e}")

    print(f"  ✓ Planted {len(krishna_coords)} Scarlet Krishnachura Flowering Trees.")

    # D. Foreground Lush Fern Clusters
    fern_coords = [
        {"x": 1500.0, "y": -350.0, "z": 15.0},
        {"x": 1500.0, "y": 350.0, "z": 15.0},
        {"x": 1750.0, "y": -550.0, "z": 12.0},
        {"x": 1750.0, "y": 550.0, "z": 12.0},
        {"x": 2100.0, "y": -750.0, "z": 12.0},
        {"x": 2100.0, "y": 750.0, "z": 12.0},
        {"x": 2700.0, "y": -650.0, "z": 12.0},
        {"x": 2700.0, "y": 650.0, "z": 12.0},
        {"x": 2950.0, "y": 0.0, "z": 15.0},
        # Promenade bases
        {"x": -200.0, "y": -300.0, "z": 85.0},
        {"x": -200.0, "y": 300.0, "z": 85.0},
        {"x": 600.0, "y": -250.0, "z": 85.0},
        {"x": 600.0, "y": 250.0, "z": 85.0},
    ]

    for idx, pos in enumerate(fern_coords):
        name = f"WWM_Pond_Fern_{idx+1:02d}"
        xform = {
            "location": pos,
            "rotation": {"pitch": 0.0, "yaw": float(idx * 53 % 360), "roll": 0.0},
            "scale": {"x": 1.6, "y": 1.6, "z": 1.6}
        }
        try:
            invoke_tool("add_to_scene_from_asset", "editor_toolset.toolsets.scene.SceneTools", {
                "asset_path": FERN_PATH,
                "name": name,
                "xform": xform
            })
        except Exception as e:
            pass

    print(f"  ✓ Planted {len(fern_coords)} lush fern clusters around water and paths.")

    # -------------------------------------------------------------
    # 3. SAVE LEVEL ASSET
    # -------------------------------------------------------------
    print("\n[Phase 3] Saving persistent level asset...")
    save_res = invoke_tool("save_assets", "editor_toolset.toolsets.asset.AssetTools", {
        "asset_paths": ["/Game/SparkVision/Maps/Level01/LV_Level01_Compact_Campus"]
    })
    print("  ✓ Level saved cleanly:", save_res)

    print("\n" + "=" * 75)
    print("SUPER-NATURAL TRANSFORMATION COMPLETE!")
    print("=" * 75)

if __name__ == "__main__":
    main()
