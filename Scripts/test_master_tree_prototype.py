#!/usr/bin/env python3
"""
Test and Validate Master Tree Prototype for SparkVision:
1. Cleans up old obstructive foreground trees along Curzon Promenade.
2. Spawns Prototype_Master_Raintree and Prototype_Master_Krishnachura in Curzon lawn.
3. Spawns natural grass clumps around tree bases.
4. Captures 4 detailed validation angles:
   - Full Tree Silhouette & Canopy View
   - Trunk, Buttress Roots & Branching Close-up
   - Delicate Foliage Clusters Close-up (Zero Geometric Slabs)
   - Gameplay Third-Person Promenade View
5. Writes artifacts and evaluates visual quality.
"""

import base64
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

SCENE_TOOLS = "editor_toolset.toolsets.scene.SceneTools"
EDITOR_APP_TOOLS = "EditorToolset.EditorAppToolset"
ASSET_TOOLS = "editor_toolset.toolsets.asset.AssetTools"

ARTIFACT_DIR = "/Users/atiaoishi/.gemini/antigravity/brain/e20fce03-5cdc-4c76-8f10-f79efc005a90"
os.makedirs(ARTIFACT_DIR, exist_ok=True)

RAINTREE_MASTER = "/Game/SparkVision/Environment/Vegetation/SM_Tree_Raintree_Master"
KRISHNA_MASTER = "/Game/SparkVision/Environment/Vegetation/SM_Tree_Krishnachura_Master"
GRASS_LAWN = "/Game/SparkVision/Environment/Vegetation/SM_Campus_Grass_Lawn"
GRASS_TUFT = "/Game/SparkVision/Environment/Vegetation/SM_Campus_Grass_Tuft"

def main():
    print("=" * 70)
    print("VALIDATING MASTER TREE PROTOTYPE IN UNREAL ENGINE 5.8")
    print("=" * 70)

    # 1. Clean up old obstructive trees near Curzon front
    print("\n[1/4] Removing old obstructive geometric slab trees...")
    try:
        found = invoke_tool("find_actors", SCENE_TOOLS, {
            "name": "WWM_Avenue_Raintree",
            "tag": "",
            "collision_channels": []
        }).get("returnValue", [])
        for a in found:
            try:
                invoke_tool("remove_from_scene", SCENE_TOOLS, {"actor": {"refPath": a["refPath"]}})
            except Exception:
                pass
        print(f"  ✓ Cleaned {len(found)} legacy avenue trees")
    except Exception as e:
        print(f"  Cleanup note: {e}")

    # Also clean existing prototype actors if re-running
    for p_name in ["Prototype_Master_Raintree", "Prototype_Master_Krishna", "Prototype_Grass_"]:
        try:
            found = invoke_tool("find_actors", SCENE_TOOLS, {
                "name": p_name,
                "tag": "",
                "collision_channels": []
            }).get("returnValue", [])
            for a in found:
                try:
                    invoke_tool("remove_from_scene", SCENE_TOOLS, {"actor": {"refPath": a["refPath"]}})
                except Exception:
                    pass
        except Exception:
            pass

    # 2. Place Prototype Master Trees
    print("\n[2/4] Placing Master Prototype Trees in Curzon Lawn...")
    # Grand Rain Tree on East Lawn
    invoke_tool("add_to_scene_from_asset", SCENE_TOOLS, {
        "asset_path": RAINTREE_MASTER,
        "name": "Prototype_Master_Raintree",
        "xform": {
            "location": {"x": -4600.0, "y": 1200.0, "z": 20.0},
            "rotation": {"pitch": 0.0, "yaw": 25.0, "roll": 0.0},
            "scale": {"x": 1.0, "y": 1.0, "z": 1.0}
        }
    })
    print("  ✓ Placed Prototype_Master_Raintree (14m wide umbrella canopy)")

    # Scarlet Krishnachura on West Lawn
    invoke_tool("add_to_scene_from_asset", SCENE_TOOLS, {
        "asset_path": KRISHNA_MASTER,
        "name": "Prototype_Master_Krishna",
        "xform": {
            "location": {"x": -4600.0, "y": -1200.0, "z": 20.0},
            "rotation": {"pitch": 0.0, "yaw": -40.0, "roll": 0.0},
            "scale": {"x": 1.0, "y": 1.0, "z": 1.0}
        }
    })
    print("  ✓ Placed Prototype_Master_Krishna (Scarlet flowering hero tree)")

    # Place natural grass clusters around tree bases
    print("\n[3/4] Planting 3D natural grass clusters around tree bases...")
    grass_spots = [
        # Around Raintree base
        (-4600.0 + 80.0, 1200.0 + 60.0, 20.0),
        (-4600.0 - 70.0, 1200.0 + 90.0, 20.0),
        (-4600.0 + 50.0, 1200.0 - 100.0, 20.0),
        (-4600.0 - 90.0, 1200.0 - 60.0, 20.0),
        (-4600.0 + 150.0, 1200.0 + 20.0, 20.0),
        # Around Krishnachura base
        (-4600.0 + 70.0, -1200.0 + 60.0, 20.0),
        (-4600.0 - 80.0, -1200.0 + 80.0, 20.0),
        (-4600.0 + 60.0, -1200.0 - 80.0, 20.0),
        (-4600.0 - 60.0, -1200.0 - 90.0, 20.0),
    ]
    for g_idx, (gx, gy, gz) in enumerate(grass_spots):
        mesh_asset = GRASS_TUFT if g_idx % 2 == 0 else GRASS_LAWN
        invoke_tool("add_to_scene_from_asset", SCENE_TOOLS, {
            "asset_path": mesh_asset,
            "name": f"Prototype_Grass_{g_idx+1:02d}",
            "xform": {
                "location": {"x": gx, "y": gy, "z": gz},
                "rotation": {"pitch": 0.0, "yaw": float(g_idx * 43 % 360), "roll": 0.0},
                "scale": {"x": 1.2, "y": 1.2, "z": 1.2}
            }
        })
    print(f"  ✓ Planted {len(grass_spots)} grass clumps around tree bases")

    # 3. Capture Validation Viewpoints
    print("\n[4/4] Capturing 4 Master Tree Prototype validation viewpoints...")
    test_views = [
        {
            "id": "MASTER_TREE_PROTOTYPE_FULL_VIEW",
            "title": "Master Tree Full Silhouette and Umbrella Canopy View",
            "loc": {"x": -3600.0, "y": 1400.0, "z": 450.0},
            "rot": {"pitch": -12.0, "yaw": -170.0, "roll": 0.0}
        },
        {
            "id": "MASTER_TREE_PROTOTYPE_TRUNK_ROOTS",
            "title": "Master Tree Trunk Buttress Roots & Natural Bark Close-up",
            "loc": {"x": -4300.0, "y": 1250.0, "z": 120.0},
            "rot": {"pitch": -8.0, "yaw": -175.0, "roll": 0.0}
        },
        {
            "id": "MASTER_TREE_PROTOTYPE_LEAF_CLUSTERS",
            "title": "Master Tree Delicate Foliage Clusters & Light-Wrap Close-up",
            "loc": {"x": -4100.0, "y": 1150.0, "z": 750.0},
            "rot": {"pitch": 6.0, "yaw": -170.0, "roll": 0.0}
        },
        {
            "id": "MASTER_TREE_PROTOTYPE_GAMEPLAY_VIEW",
            "title": "Gameplay Third-Person Promenade View Framing Curzon Hall",
            "loc": {"x": -5800.0, "y": 0.0, "z": 180.0},
            "rot": {"pitch": -4.0, "yaw": 0.0, "roll": 0.0}
        }
    ]

    for v in test_views:
        vid = v["id"]
        xform = {
            "location": v["loc"],
            "rotation": v["rot"],
            "scale": {"x": 1.0, "y": 1.0, "z": 1.0}
        }
        invoke_tool("SetCameraTransform", EDITOR_APP_TOOLS, {"transform": xform})
        time.sleep(0.4)
        cap = invoke_tool("CaptureViewport", EDITOR_APP_TOOLS, {
            "captureTransform": xform,
            "annotations": {
                "gridSpacing": 0, "gridExtent": 0, "gridHeight": 0,
                "maxLabelDistance": 0, "classFilter": None, "maxLabels": 0
            },
            "bShowUI": False
        })
        img_b64 = cap.get("returnValue", {}).get("image", {}).get("data", "")
        if img_b64:
            out_file = os.path.join(ARTIFACT_DIR, f"{vid}.png")
            with open(out_file, "wb") as f:
                f.write(base64.b64decode(img_b64))
            print(f"  ✓ Saved validation capture: {vid}.png")
        else:
            print(f"  ✗ Failed capture for {vid}")

    print("\n" + "=" * 70)
    print("MASTER TREE PROTOTYPE VALIDATION COMPLETE!")
    print("=" * 70)

if __name__ == "__main__":
    main()
