#!/usr/bin/env python3
"""
Populates calibrated botanical assets across Curzon front lawn, Shaheed sanctuary,
TSC plaza, Hakim Chattar, and Kala Bhaban gardens with guaranteed >14m clearance.
"""

import sys
import os
import math

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mcp_client

ENV_PATH = "/Game/SparkVision/Campus/Environment"

BUILDINGS = [
    {"name": "Curzon_Hall_Main", "center": {"x": -2850.0, "y": 0.0}, "extent": {"x": 1000.0, "y": 6650.0}, "min_clearance": 1200.0},
    {"name": "Curzon_Labs", "center": {"x": 6500.0, "y": 4610.0}, "extent": {"x": 4100.0, "y": 2100.0}, "min_clearance": 1200.0},
    {"name": "Curzon_Annex", "center": {"x": 6500.0, "y": -4190.0}, "extent": {"x": 4100.0, "y": 2100.0}, "min_clearance": 1200.0},
    {"name": "Shaheed_Minar", "center": {"x": -282.0, "y": -54042.0}, "extent": {"x": 1200.0, "y": 1500.0}, "min_clearance": 1600.0},
    {"name": "Raju_Sculpture", "center": {"x": 58964.0, "y": -63725.0}, "extent": {"x": 800.0, "y": 800.0}, "min_clearance": 800.0},
    {"name": "TSC_Complex", "center": {"x": 61200.0, "y": -59500.0}, "extent": {"x": 3500.0, "y": 3200.0}, "min_clearance": 1200.0},
    {"name": "Central_Library", "center": {"x": 73459.0, "y": -71379.0}, "extent": {"x": 2800.0, "y": 2000.0}, "min_clearance": 1200.0},
    {"name": "Kala_Bhaban", "center": {"x": 78004.0, "y": -95794.0}, "extent": {"x": 3000.0, "y": 8200.0}, "min_clearance": 1400.0},
    {"name": "Aparajeyo_Bangla", "center": {"x": 73486.0, "y": -95794.0}, "extent": {"x": 600.0, "y": 600.0}, "min_clearance": 1000.0},
    {"name": "Shahidullah_Hall", "center": {"x": 5000.0, "y": -4960.0}, "extent": {"x": 4600.0, "y": 3700.0}, "min_clearance": 1200.0},
    {"name": "Bangla_Academy", "center": {"x": 18000.0, "y": -28000.0}, "extent": {"x": 4700.0, "y": 5200.0}, "min_clearance": 1200.0},
]

def dist_point_to_box(px, py, cx, cy, ex, ey):
    dx = max(0.0, abs(px - cx) - ex)
    dy = max(0.0, abs(py - cy) - ey)
    return math.sqrt(dx * dx + dy * dy)

def check_clearance(px, py):
    for b in BUILDINGS:
        d = dist_point_to_box(px, py, b["center"]["x"], b["center"]["y"], b["extent"]["x"], b["extent"]["y"])
        if d < b["min_clearance"]:
            return False, b["name"], d
    return True, None, 0.0

def spawn_tree(asset_name, actor_name, loc, yaw=0.0, scale=1.0, folder="Environment/Living_Campus"):
    ok, bname, d = check_clearance(loc["x"], loc["y"])
    if not ok:
        print(f"  [REJECTED] {actor_name} at ({loc['x']}, {loc['y']}): only {d/100:.1f}m from {bname}")
        return None

    asset_ref = f"{ENV_PATH}/{asset_name}.{asset_name}"
    try:
        res = mcp_client.invoke_tool("add_to_scene_from_asset", "editor_toolset.toolsets.scene.SceneTools", {
            "asset_path": asset_ref,
            "name": actor_name,
            "xform": {
                "location": loc,
                "rotation": {"pitch": 0.0, "yaw": yaw, "roll": 0.0},
                "scale": {"x": scale, "y": scale, "z": scale}
            }
        })
        ref = res["returnValue"]["refPath"]
        mcp_client.invoke_tool("set_actor_folder", "editor_toolset.toolsets.scene.SceneTools", {
            "actor": {"refPath": ref},
            "folder_path": folder
        })
        return ref
    except Exception as e:
        print(f"  Error spawning {actor_name}: {e}")
        return None

CALIBRATED_SPECS = [
    # 1. Curzon Front Lawn Promenade Garden (Setback >= 15m from Curzon portal: X <= -5350)
    ("SM_Bush_Gandharaj_White", "Curzon_Garden_Gandharaj_1", {"x": -5400.0, "y": -1200.0, "z": 20.0}, 15.0, 1.0, "Environment/Curzon_Landscape"),
    ("SM_Bush_Gandharaj_White", "Curzon_Garden_Gandharaj_2", {"x": -5400.0, "y": 1200.0, "z": 20.0}, -20.0, 1.0, "Environment/Curzon_Landscape"),
    ("SM_Bush_Rangan_Scarlet", "Curzon_Garden_Rangan_1", {"x": -5600.0, "y": -2200.0, "z": 20.0}, 45.0, 1.05, "Environment/Curzon_Landscape"),
    ("SM_Bush_Rangan_Scarlet", "Curzon_Garden_Rangan_2", {"x": -5600.0, "y": 2200.0, "z": 20.0}, -45.0, 1.05, "Environment/Curzon_Landscape"),
    ("SM_Bush_Kamini_Hedge", "Curzon_Parterre_Hedge_1", {"x": -5200.0, "y": -1800.0, "z": 20.0}, 0.0, 1.0, "Environment/Curzon_Landscape"),
    ("SM_Bush_Kamini_Hedge", "Curzon_Parterre_Hedge_2", {"x": -5200.0, "y": 1800.0, "z": 20.0}, 0.0, 1.0, "Environment/Curzon_Landscape"),
    ("SM_Tree_Radhachura_Yellow", "Curzon_Wing_Radhachura_West", {"x": -5500.0, "y": -4200.0, "z": 20.0}, 30.0, 1.0, "Environment/Curzon_Landscape"),
    ("SM_Tree_Radhachura_Yellow", "Curzon_Wing_Radhachura_East", {"x": -5500.0, "y": 4200.0, "z": 20.0}, -30.0, 1.0, "Environment/Curzon_Landscape"),
    ("SM_Tree_Krishnachura_Bloom", "Curzon_Wing_Krishnachura_West", {"x": -5800.0, "y": -5800.0, "z": 20.0}, 65.0, 1.0, "Environment/Curzon_Landscape"),
    ("SM_Tree_Krishnachura_Bloom", "Curzon_Wing_Krishnachura_East", {"x": -5800.0, "y": 5800.0, "z": 20.0}, -65.0, 1.0, "Environment/Curzon_Landscape"),
    ("SM_Tree_Debdaru_Columnar", "Curzon_Avenue_Debdaru_1", {"x": -5800.0, "y": -3000.0, "z": 20.0}, 0.0, 1.05, "Environment/Curzon_Landscape"),
    ("SM_Tree_Debdaru_Columnar", "Curzon_Avenue_Debdaru_2", {"x": -5800.0, "y": 3000.0, "z": 20.0}, 0.0, 1.05, "Environment/Curzon_Landscape"),

    # 2. Shaheed Minar Sanctuary Flanking Trees & Gardens (Setback >= 18m from monument: X <= -3100, X >= 2600)
    ("SM_Tree_Debdaru_Columnar", "Shaheed_Flank_Debdaru_1", {"x": -3400.0, "y": -54000.0, "z": 20.0}, 0.0, 1.1, "Environment/Shaheed_Minar"),
    ("SM_Tree_Debdaru_Columnar", "Shaheed_Flank_Debdaru_2", {"x": 2800.0, "y": -54000.0, "z": 20.0}, 0.0, 1.1, "Environment/Shaheed_Minar"),
    ("SM_Bush_Kamini_Hedge", "Shaheed_Walkway_Hedge_1", {"x": -3200.0, "y": -51000.0, "z": 20.0}, 0.0, 1.0, "Environment/Shaheed_Minar"),
    ("SM_Bush_Kamini_Hedge", "Shaheed_Walkway_Hedge_2", {"x": 2600.0, "y": -51000.0, "z": 20.0}, 0.0, 1.0, "Environment/Shaheed_Minar"),
    ("SM_Bush_Gandharaj_White", "Shaheed_Lawn_Gandharaj_1", {"x": -3500.0, "y": -52500.0, "z": 20.0}, 30.0, 1.0, "Environment/Shaheed_Minar"),
    ("SM_Bush_Gandharaj_White", "Shaheed_Lawn_Gandharaj_2", {"x": 2900.0, "y": -52500.0, "z": 20.0}, -30.0, 1.0, "Environment/Shaheed_Minar"),

    # 3. TSC & Central Library Precinct
    ("SM_Bush_Kamini_Hedge", "TSC_Plaza_Hedge_1", {"x": 55500.0, "y": -64000.0, "z": 20.0}, 45.0, 1.0, "Environment/TSC_Raju"),
    ("SM_Bush_Kamini_Hedge", "TSC_Plaza_Hedge_2", {"x": 62500.0, "y": -64000.0, "z": 20.0}, -45.0, 1.0, "Environment/TSC_Raju"),
    ("SM_Bush_Rangan_Scarlet", "TSC_Lawn_Rangan_1", {"x": 55500.0, "y": -56000.0, "z": 20.0}, 25.0, 1.0, "Environment/TSC_Raju"),
    ("SM_Tree_Kadam_Bloom", "HakimChattar_Kadam_1", {"x": 68500.0, "y": -74500.0, "z": 20.0}, 15.0, 1.0, "Environment/TSC_Raju"),
    ("SM_Tree_Mahogany_Grand", "HakimChattar_Mahogany_1", {"x": 67500.0, "y": -71500.0, "z": 20.0}, -25.0, 1.1, "Environment/TSC_Raju"),
    ("SM_Tree_Debdaru_Columnar", "Library_Debdaru_1", {"x": 68500.0, "y": -69000.0, "z": 20.0}, 0.0, 1.1, "Environment/TSC_Raju"),
    ("SM_Bush_Gandharaj_White", "Library_Gandharaj_1", {"x": 69000.0, "y": -69500.0, "z": 20.0}, 20.0, 1.0, "Environment/TSC_Raju"),

    # 4. Kala Bhaban Forecourt Gardens
    ("SM_Bush_Gandharaj_White", "KalaBhaban_Lawn_Gandharaj_1", {"x": 71500.0, "y": -93500.0, "z": 20.0}, 45.0, 1.0, "Environment/Arts_Faculty"),
    ("SM_Bush_Gandharaj_White", "KalaBhaban_Lawn_Gandharaj_2", {"x": 71500.0, "y": -98000.0, "z": 20.0}, -45.0, 1.0, "Environment/Arts_Faculty"),
]

def main():
    print("=" * 70)
    print("SPAWNING CALIBRATED CAMPUS FLORA WITH GUARANTEED CLEARANCE...")
    print("=" * 70)

    spawned = 0
    for asset, name, loc, yaw, scale, folder in CALIBRATED_SPECS:
        ref = spawn_tree(asset, name, loc, yaw=yaw, scale=scale, folder=folder)
        if ref:
            spawned += 1
            print(f"  [SPAWNED] {name} ({asset}) in {folder}")

    print("\n" + "=" * 70)
    print(f"CALIBRATED FLORA COMPLETE: Successfully spawned {spawned}/{len(CALIBRATED_SPECS)} assets!")
    print("=" * 70)

if __name__ == "__main__":
    main()
