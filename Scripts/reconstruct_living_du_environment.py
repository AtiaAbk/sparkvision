#!/usr/bin/env python3
"""
Living University of Dhaka Open-World Environment Reconstruction Suite
Populates authentic, lush, Where Winds Meet-inspired botanical diversity
across all 5 sectors of the University of Dhaka Level 1 map:
- Strictly enforces architectural setbacks (12m - 18m)
- Ground anchored at Z=20
- Multi-tier vertical canopy layering: canopy trees, sub-canopy bloom,
  flowering shrubs, bamboo groves, wild grasses, ferns, and leaf litter.
- Ambient ecological wildlife: Doel birds, butterflies, and dragonflies.
"""

import sys
import os
import math
import json

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

def spawn_env_actor(asset_name, actor_name, loc, yaw=0.0, scale=1.0, folder="Environment/Living_Campus"):
    # Non-tree decorative elements (wildlife, decals, lilypads) have lighter clearance rules
    is_flora = "Tree" in asset_name or "Bamboo" in asset_name or "Bush" in asset_name
    if is_flora:
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

# ==============================================================================
# ENVIRONMENT RECONSTRUCTION SPECIFICATION
# ==============================================================================
PLANTING_SPECS = [
    # --------------------------------------------------------------------------
    # SECTOR 1: CURZON HALL HERITAGE PRECINCT & BOTANICAL POND
    # --------------------------------------------------------------------------
    # Curzon Front Elevation Parterre Garden
    ("SM_Bush_Gandharaj_White", "Curzon_Garden_Gandharaj_1", {"x": -4200.0, "y": -1200.0, "z": 20.0}, 15.0, 1.0, "Environment/Curzon_Landscape"),
    ("SM_Bush_Gandharaj_White", "Curzon_Garden_Gandharaj_2", {"x": -4200.0, "y": 1200.0, "z": 20.0}, -20.0, 1.0, "Environment/Curzon_Landscape"),
    ("SM_Bush_Rangan_Scarlet", "Curzon_Garden_Rangan_1", {"x": -4400.0, "y": -2200.0, "z": 20.0}, 45.0, 1.05, "Environment/Curzon_Landscape"),
    ("SM_Bush_Rangan_Scarlet", "Curzon_Garden_Rangan_2", {"x": -4400.0, "y": 2200.0, "z": 20.0}, -45.0, 1.05, "Environment/Curzon_Landscape"),
    ("SM_Bush_Kamini_Hedge", "Curzon_Parterre_Hedge_1", {"x": -4000.0, "y": -1800.0, "z": 20.0}, 0.0, 1.0, "Environment/Curzon_Landscape"),
    ("SM_Bush_Kamini_Hedge", "Curzon_Parterre_Hedge_2", {"x": -4000.0, "y": 1800.0, "z": 20.0}, 0.0, 1.0, "Environment/Curzon_Landscape"),
    
    # Curzon Wing Framing Trees
    ("SM_Tree_Radhachura_Yellow", "Curzon_Wing_Radhachura_West", {"x": -4600.0, "y": -4200.0, "z": 20.0}, 30.0, 1.0, "Environment/Curzon_Landscape"),
    ("SM_Tree_Radhachura_Yellow", "Curzon_Wing_Radhachura_East", {"x": -4600.0, "y": 4200.0, "z": 20.0}, -30.0, 1.0, "Environment/Curzon_Landscape"),
    ("SM_Tree_Krishnachura_Bloom", "Curzon_Wing_Krishnachura_West", {"x": -4800.0, "y": -5800.0, "z": 20.0}, 65.0, 1.0, "Environment/Curzon_Landscape"),
    ("SM_Tree_Krishnachura_Bloom", "Curzon_Wing_Krishnachura_East", {"x": -4800.0, "y": 5800.0, "z": 20.0}, -65.0, 1.0, "Environment/Curzon_Landscape"),
    ("SM_Tree_Debdaru_Columnar", "Curzon_Avenue_Debdaru_1", {"x": -4800.0, "y": -3000.0, "z": 20.0}, 0.0, 1.05, "Environment/Curzon_Landscape"),
    ("SM_Tree_Debdaru_Columnar", "Curzon_Avenue_Debdaru_2", {"x": -4800.0, "y": 3000.0, "z": 20.0}, 0.0, 1.05, "Environment/Curzon_Landscape"),

    # Curzon Botanical Pond Enhancements
    ("SM_Tree_Kadam_Bloom", "Curzon_Pond_Kadam_1", {"x": 1600.0, "y": -1200.0, "z": 20.0}, 20.0, 1.0, "Environment/Curzon_Pond"),
    ("SM_Tree_Kadam_Bloom", "Curzon_Pond_Kadam_2", {"x": 3800.0, "y": 1400.0, "z": 20.0}, -40.0, 1.05, "Environment/Curzon_Pond"),
    ("SM_Grass_Tall_Savanna", "Curzon_Pond_Savanna_1", {"x": 1400.0, "y": -600.0, "z": 20.0}, 15.0, 1.0, "Environment/Curzon_Pond"),
    ("SM_Grass_Tall_Savanna", "Curzon_Pond_Savanna_2", {"x": 4200.0, "y": -800.0, "z": 20.0}, -25.0, 1.0, "Environment/Curzon_Pond"),
    ("SM_Grass_Tall_Savanna", "Curzon_Pond_Savanna_3", {"x": 4000.0, "y": 800.0, "z": 20.0}, 45.0, 1.05, "Environment/Curzon_Pond"),
    ("SM_Fern_Undergrowth_Cluster", "Curzon_Pond_Fern_1", {"x": 1500.0, "y": -1000.0, "z": 20.0}, 0.0, 1.0, "Environment/Curzon_Pond"),
    ("SM_Fern_Undergrowth_Cluster", "Curzon_Pond_Fern_2", {"x": 3600.0, "y": 1200.0, "z": 20.0}, 30.0, 1.0, "Environment/Curzon_Pond"),

    # Curzon Rear Science Botanical Pocket & Bamboo Windbreak
    ("SM_Cluster_Bamboo_Grove", "Curzon_Rear_Bamboo_Grove_1", {"x": 7800.0, "y": 2000.0, "z": 20.0}, 45.0, 1.1, "Environment/Curzon_Landscape"),
    ("SM_Tree_Mahogany_Grand", "Curzon_Rear_Mahogany_1", {"x": 7600.0, "y": -1800.0, "z": 20.0}, 15.0, 1.05, "Environment/Curzon_Landscape"),
    ("SM_Ground_LeafLitter_Patch", "Curzon_Litter_Patch_1", {"x": 7600.0, "y": -1800.0, "z": 20.0}, 0.0, 1.0, "Environment/Curzon_Landscape"),

    # Curzon Wildlife & Ambient Life
    ("SM_Wildlife_Bird_Doel", "Curzon_Balustrade_Doel_1", {"x": -2850.0, "y": -450.0, "z": 240.0}, 30.0, 1.0, "Environment/Wildlife"),
    ("SM_Wildlife_Bird_Doel", "Curzon_Garden_Doel_2", {"x": -4200.0, "y": 1200.0, "z": 160.0}, -60.0, 1.0, "Environment/Wildlife"),
    ("SM_Wildlife_Butterfly_Cluster", "Curzon_Garden_Butterflies_1", {"x": -4200.0, "y": -1200.0, "z": 80.0}, 0.0, 1.0, "Environment/Wildlife"),
    ("SM_Wildlife_Dragonfly_Pair", "Curzon_Pond_Dragonflies_1", {"x": 2600.0, "y": -200.0, "z": 65.0}, 25.0, 1.0, "Environment/Wildlife"),
    ("SM_Wildlife_Dragonfly_Pair", "Curzon_Pond_Dragonflies_2", {"x": 3200.0, "y": 300.0, "z": 65.0}, -45.0, 1.0, "Environment/Wildlife"),

    # --------------------------------------------------------------------------
    # SECTOR 2: DOYEL CHATTAR & UNIVERSITY AVENUE
    # --------------------------------------------------------------------------
    # Doyel Monument Roundabout Flower Garden
    ("SM_Bush_Rangan_Scarlet", "Doyel_Roundabout_Rangan_1", {"x": 6900.0, "y": -16500.0, "z": 20.0}, 30.0, 1.0, "Environment/Doyel_Chattar"),
    ("SM_Bush_Rangan_Scarlet", "Doyel_Roundabout_Rangan_2", {"x": 8100.0, "y": -16500.0, "z": 20.0}, -30.0, 1.0, "Environment/Doyel_Chattar"),
    ("SM_Bush_Gandharaj_White", "Doyel_Roundabout_Gandharaj_1", {"x": 7500.0, "y": -15900.0, "z": 20.0}, 90.0, 1.0, "Environment/Doyel_Chattar"),
    ("SM_Bush_Gandharaj_White", "Doyel_Roundabout_Gandharaj_2", {"x": 7500.0, "y": -17100.0, "z": 20.0}, -90.0, 1.0, "Environment/Doyel_Chattar"),
    ("SM_Wildlife_Bird_Doel", "Doyel_Monument_Doel", {"x": 7500.0, "y": -16300.0, "z": 180.0}, 45.0, 1.0, "Environment/Wildlife"),
    ("SM_Wildlife_Butterfly_Cluster", "Doyel_Garden_Butterflies", {"x": 7500.0, "y": -16800.0, "z": 70.0}, 0.0, 1.0, "Environment/Wildlife"),

    # University Avenue Shaded Tree Tunnel (Debdaru & Rain Tree alternating)
    ("SM_Tree_Debdaru_Columnar", "Avenue_Debdaru_West_1", {"x": 4600.0, "y": -13500.0, "z": 20.0}, 0.0, 1.1, "Environment/Doyel_Chattar"),
    ("SM_Tree_Debdaru_Columnar", "Avenue_Debdaru_East_1", {"x": 10400.0, "y": -13500.0, "z": 20.0}, 0.0, 1.1, "Environment/Doyel_Chattar"),
    ("SM_Tree_Debdaru_Columnar", "Avenue_Debdaru_West_2", {"x": 4800.0, "y": -18500.0, "z": 20.0}, 0.0, 1.05, "Environment/Doyel_Chattar"),
    ("SM_Tree_Debdaru_Columnar", "Avenue_Debdaru_East_2", {"x": 10200.0, "y": -18500.0, "z": 20.0}, 0.0, 1.05, "Environment/Doyel_Chattar"),
    ("SM_Tree_Mahogany_Grand", "Avenue_Mahogany_1", {"x": 4800.0, "y": -22000.0, "z": 20.0}, 20.0, 1.1, "Environment/Doyel_Chattar"),
    ("SM_Tree_Mahogany_Grand", "Avenue_Mahogany_2", {"x": 10200.0, "y": -22000.0, "z": 20.0}, -20.0, 1.1, "Environment/Doyel_Chattar"),
    ("SM_Grass_Tall_Savanna", "Avenue_Verge_Savanna_1", {"x": 4500.0, "y": -16000.0, "z": 20.0}, 0.0, 1.0, "Environment/Doyel_Chattar"),
    ("SM_Grass_Tall_Savanna", "Avenue_Verge_Savanna_2", {"x": 10500.0, "y": -16000.0, "z": 20.0}, 0.0, 1.0, "Environment/Doyel_Chattar"),

    # --------------------------------------------------------------------------
    # SECTOR 3: FULLER ROAD & SHAHEED MINAR SANCTUARY
    # --------------------------------------------------------------------------
    # Shaheed Minar Flanking Evergreen & Floral Framing
    ("SM_Tree_Debdaru_Columnar", "Shaheed_Flank_Debdaru_1", {"x": -2600.0, "y": -54000.0, "z": 20.0}, 0.0, 1.1, "Environment/Shaheed_Minar"),
    ("SM_Tree_Debdaru_Columnar", "Shaheed_Flank_Debdaru_2", {"x": 2000.0, "y": -54000.0, "z": 20.0}, 0.0, 1.1, "Environment/Shaheed_Minar"),
    ("SM_Bush_Kamini_Hedge", "Shaheed_Walkway_Hedge_1", {"x": -1800.0, "y": -51000.0, "z": 20.0}, 0.0, 1.0, "Environment/Shaheed_Minar"),
    ("SM_Bush_Kamini_Hedge", "Shaheed_Walkway_Hedge_2", {"x": 1200.0, "y": -51000.0, "z": 20.0}, 0.0, 1.0, "Environment/Shaheed_Minar"),
    ("SM_Bush_Gandharaj_White", "Shaheed_Lawn_Gandharaj_1", {"x": -2400.0, "y": -53000.0, "z": 20.0}, 30.0, 1.0, "Environment/Shaheed_Minar"),
    ("SM_Bush_Gandharaj_White", "Shaheed_Lawn_Gandharaj_2", {"x": 1800.0, "y": -53000.0, "z": 20.0}, -30.0, 1.0, "Environment/Shaheed_Minar"),
    ("SM_Fern_Undergrowth_Cluster", "Shaheed_Banyan_Fern_1", {"x": -2200.0, "y": -52000.0, "z": 20.0}, 15.0, 1.0, "Environment/Shaheed_Minar"),
    ("SM_Fern_Undergrowth_Cluster", "Shaheed_Banyan_Fern_2", {"x": 1600.0, "y": -52000.0, "z": 20.0}, -15.0, 1.0, "Environment/Shaheed_Minar"),
    ("SM_Wildlife_Bird_Doel", "Shaheed_Banyan_Doel", {"x": -2200.0, "y": -52000.0, "z": 220.0}, 60.0, 1.0, "Environment/Wildlife"),

    # Fuller Road Grand Tree Tunnel
    ("SM_Tree_Mahogany_Grand", "Fuller_Mahogany_North_1", {"x": 18000.0, "y": -57000.0, "z": 20.0}, 10.0, 1.1, "Environment/Fuller_Road"),
    ("SM_Tree_Mahogany_Grand", "Fuller_Mahogany_South_1", {"x": 18000.0, "y": -61500.0, "z": 20.0}, -15.0, 1.1, "Environment/Fuller_Road"),
    ("SM_Tree_Debdaru_Columnar", "Fuller_Debdaru_1", {"x": 12000.0, "y": -57000.0, "z": 20.0}, 0.0, 1.05, "Environment/Fuller_Road"),
    ("SM_Tree_Debdaru_Columnar", "Fuller_Debdaru_2", {"x": 22000.0, "y": -57000.0, "z": 20.0}, 0.0, 1.05, "Environment/Fuller_Road"),
    ("SM_Tree_Debdaru_Columnar", "Fuller_Debdaru_3", {"x": 12000.0, "y": -61500.0, "z": 20.0}, 0.0, 1.05, "Environment/Fuller_Road"),
    ("SM_Tree_Debdaru_Columnar", "Fuller_Debdaru_4", {"x": 22000.0, "y": -61500.0, "z": 20.0}, 0.0, 1.05, "Environment/Fuller_Road"),
    ("SM_Ground_LeafLitter_Patch", "Fuller_Litter_Patch_1", {"x": 10000.0, "y": -57000.0, "z": 20.0}, 0.0, 1.0, "Environment/Fuller_Road"),
    ("SM_Ground_LeafLitter_Patch", "Fuller_Litter_Patch_2", {"x": 27000.0, "y": -61500.0, "z": 20.0}, 0.0, 1.0, "Environment/Fuller_Road"),
    ("SM_Grass_Tall_Savanna", "Fuller_Savanna_1", {"x": 15000.0, "y": -56800.0, "z": 20.0}, 20.0, 1.0, "Environment/Fuller_Road"),
    ("SM_Grass_Tall_Savanna", "Fuller_Savanna_2", {"x": 30000.0, "y": -61700.0, "z": 20.0}, -30.0, 1.0, "Environment/Fuller_Road"),

    # --------------------------------------------------------------------------
    # SECTOR 4: TSC & CENTRAL LIBRARY PRECINCT
    # --------------------------------------------------------------------------
    # Raju Memorial & TSC Perimeter Framing
    ("SM_Bush_Kamini_Hedge", "TSC_Plaza_Hedge_1", {"x": 57000.0, "y": -62500.0, "z": 20.0}, 45.0, 1.0, "Environment/TSC_Raju"),
    ("SM_Bush_Kamini_Hedge", "TSC_Plaza_Hedge_2", {"x": 60500.0, "y": -62500.0, "z": 20.0}, -45.0, 1.0, "Environment/TSC_Raju"),
    ("SM_Bush_Rangan_Scarlet", "TSC_Lawn_Rangan_1", {"x": 57500.0, "y": -58000.0, "z": 20.0}, 25.0, 1.0, "Environment/TSC_Raju"),
    ("SM_Bush_Rangan_Scarlet", "TSC_Lawn_Rangan_2", {"x": 65000.0, "y": -61500.0, "z": 20.0}, -35.0, 1.0, "Environment/TSC_Raju"),
    ("SM_Cluster_Bamboo_Grove", "TSC_Corner_Bamboo_1", {"x": 55000.0, "y": -62000.0, "z": 20.0}, 20.0, 1.0, "Environment/TSC_Raju"),
    ("SM_Wildlife_Butterfly_Cluster", "TSC_Flower_Butterflies", {"x": 57500.0, "y": -58000.0, "z": 70.0}, 0.0, 1.0, "Environment/Wildlife"),

    # Hakim Chattar Student Grove
    ("SM_Tree_Kadam_Bloom", "HakimChattar_Kadam_1", {"x": 70000.0, "y": -73000.0, "z": 20.0}, 15.0, 1.0, "Environment/TSC_Raju"),
    ("SM_Tree_Mahogany_Grand", "HakimChattar_Mahogany_1", {"x": 73000.0, "y": -74500.0, "z": 20.0}, -25.0, 1.1, "Environment/TSC_Raju"),
    ("SM_Fern_Undergrowth_Cluster", "HakimChattar_Fern_1", {"x": 71000.0, "y": -73800.0, "z": 20.0}, 45.0, 1.0, "Environment/TSC_Raju"),
    ("SM_Fern_Undergrowth_Cluster", "HakimChattar_Fern_2", {"x": 74500.0, "y": -73800.0, "z": 20.0}, -45.0, 1.0, "Environment/TSC_Raju"),
    ("SM_Ground_LeafLitter_Patch", "HakimChattar_Litter_1", {"x": 71000.0, "y": -73800.0, "z": 20.0}, 0.0, 1.0, "Environment/TSC_Raju"),
    ("SM_Wildlife_Bird_Doel", "HakimChattar_Doel", {"x": 71000.0, "y": -73800.0, "z": 200.0}, 80.0, 1.0, "Environment/Wildlife"),

    # Central Library Forecourt Gardens
    ("SM_Tree_Debdaru_Columnar", "Library_Debdaru_1", {"x": 71000.0, "y": -69000.0, "z": 20.0}, 0.0, 1.1, "Environment/TSC_Raju"),
    ("SM_Tree_Debdaru_Columnar", "Library_Debdaru_2", {"x": 76000.0, "y": -69000.0, "z": 20.0}, 0.0, 1.1, "Environment/TSC_Raju"),
    ("SM_Bush_Gandharaj_White", "Library_Gandharaj_1", {"x": 72500.0, "y": -69500.0, "z": 20.0}, 20.0, 1.0, "Environment/TSC_Raju"),
    ("SM_Bush_Gandharaj_White", "Library_Gandharaj_2", {"x": 74500.0, "y": -69500.0, "z": 20.0}, -20.0, 1.0, "Environment/TSC_Raju"),

    # --------------------------------------------------------------------------
    # SECTOR 5: ARTS FACULTY (KALA BHABAN) & THE MALL
    # --------------------------------------------------------------------------
    # The Mall Open Grassland & Grand Heritage Groves
    ("SM_Cluster_Bamboo_Grove", "TheMall_West_Bamboo_1", {"x": 61000.0, "y": -83000.0, "z": 20.0}, 15.0, 1.15, "Environment/Arts_Faculty"),
    ("SM_Cluster_Bamboo_Grove", "TheMall_West_Bamboo_2", {"x": 61000.0, "y": -90000.0, "z": 20.0}, -20.0, 1.15, "Environment/Arts_Faculty"),
    ("SM_Tree_Kadam_Bloom", "TheMall_Kadam_Bloom_1", {"x": 67000.0, "y": -82000.0, "z": 20.0}, 40.0, 1.05, "Environment/Arts_Faculty"),
    ("SM_Tree_Kadam_Bloom", "TheMall_Kadam_Bloom_2", {"x": 67000.0, "y": -91000.0, "z": 20.0}, -30.0, 1.05, "Environment/Arts_Faculty"),
    ("SM_Grass_Tall_Savanna", "TheMall_WildGrass_1", {"x": 63000.0, "y": -82500.0, "z": 20.0}, 10.0, 1.1, "Environment/Arts_Faculty"),
    ("SM_Grass_Tall_Savanna", "TheMall_WildGrass_2", {"x": 65500.0, "y": -85500.0, "z": 20.0}, -45.0, 1.1, "Environment/Arts_Faculty"),
    ("SM_Grass_Tall_Savanna", "TheMall_WildGrass_3", {"x": 63000.0, "y": -88500.0, "z": 20.0}, 60.0, 1.1, "Environment/Arts_Faculty"),
    ("SM_Grass_Tall_Savanna", "TheMall_WildGrass_4", {"x": 66000.0, "y": -90500.0, "z": 20.0}, -15.0, 1.1, "Environment/Arts_Faculty"),
    ("SM_Grass_Tuft_Lawn", "TheMall_LawnTuft_1", {"x": 64000.0, "y": -86000.0, "z": 20.0}, 0.0, 1.0, "Environment/Arts_Faculty"),
    ("SM_Grass_Tuft_Lawn", "TheMall_LawnTuft_2", {"x": 66000.0, "y": -87000.0, "z": 20.0}, 30.0, 1.0, "Environment/Arts_Faculty"),
    ("SM_Fern_Undergrowth_Cluster", "TheMall_Banyan1_Fern", {"x": 64000.0, "y": -84000.0, "z": 20.0}, 35.0, 1.1, "Environment/Arts_Faculty"),
    ("SM_Fern_Undergrowth_Cluster", "TheMall_Banyan2_Fern", {"x": 64000.0, "y": -89000.0, "z": 20.0}, -35.0, 1.1, "Environment/Arts_Faculty"),
    ("SM_Ground_LeafLitter_Patch", "TheMall_Banyan1_Litter", {"x": 64000.0, "y": -84000.0, "z": 20.0}, 0.0, 1.0, "Environment/Arts_Faculty"),
    ("SM_Ground_LeafLitter_Patch", "TheMall_Banyan2_Litter", {"x": 64000.0, "y": -89000.0, "z": 20.0}, 0.0, 1.0, "Environment/Arts_Faculty"),

    # Aparajeyo Bangla & Kala Bhaban Gardens
    ("SM_Bush_Kamini_Hedge", "KalaBhaban_Walkway_Hedge_1", {"x": 72500.0, "y": -94000.0, "z": 20.0}, 0.0, 1.0, "Environment/Arts_Faculty"),
    ("SM_Bush_Kamini_Hedge", "KalaBhaban_Walkway_Hedge_2", {"x": 72500.0, "y": -97500.0, "z": 20.0}, 0.0, 1.0, "Environment/Arts_Faculty"),
    ("SM_Bush_Rangan_Scarlet", "KalaBhaban_Lawn_Rangan_1", {"x": 73500.0, "y": -93000.0, "z": 20.0}, 15.0, 1.0, "Environment/Arts_Faculty"),
    ("SM_Bush_Rangan_Scarlet", "KalaBhaban_Lawn_Rangan_2", {"x": 73500.0, "y": -98500.0, "z": 20.0}, -15.0, 1.0, "Environment/Arts_Faculty"),
    ("SM_Bush_Gandharaj_White", "KalaBhaban_Lawn_Gandharaj_1", {"x": 75500.0, "y": -93500.0, "z": 20.0}, 45.0, 1.0, "Environment/Arts_Faculty"),
    ("SM_Bush_Gandharaj_White", "KalaBhaban_Lawn_Gandharaj_2", {"x": 75500.0, "y": -98000.0, "z": 20.0}, -45.0, 1.0, "Environment/Arts_Faculty"),
    ("SM_Tree_Debdaru_Columnar", "KalaBhaban_Forecourt_Debdaru_1", {"x": 70500.0, "y": -92000.0, "z": 20.0}, 0.0, 1.1, "Environment/Arts_Faculty"),
    ("SM_Tree_Debdaru_Columnar", "KalaBhaban_Forecourt_Debdaru_2", {"x": 70500.0, "y": -99500.0, "z": 20.0}, 0.0, 1.1, "Environment/Arts_Faculty"),
    ("SM_Wildlife_Bird_Doel", "Aparajeyo_Framing_Doel", {"x": 71500.0, "y": -93000.0, "z": 220.0}, -30.0, 1.0, "Environment/Wildlife"),
    ("SM_Wildlife_Butterfly_Cluster", "KalaBhaban_Butterflies", {"x": 73500.0, "y": -93000.0, "z": 70.0}, 0.0, 1.0, "Environment/Wildlife"),
]

def main():
    print("=" * 70)
    print("EXECUTING LIVING UNIVERSITY OF DHAKA ENVIRONMENT RECONSTRUCTION...")
    print("=" * 70)

    spawned_count = 0
    rejected_count = 0

    for asset_name, actor_name, loc, yaw, scale, folder in PLANTING_SPECS:
        ref = spawn_env_actor(asset_name, actor_name, loc, yaw=yaw, scale=scale, folder=folder)
        if ref:
            spawned_count += 1
            print(f"  [SPAWNED] {actor_name} ({asset_name}) in {folder}")
        else:
            rejected_count += 1

    print("\n" + "=" * 70)
    print(f"RECONSTRUCTION COMPLETE: Successfully spawned {spawned_count} living assets! (Rejected: {rejected_count})")
    print("=" * 70)

if __name__ == "__main__":
    main()
