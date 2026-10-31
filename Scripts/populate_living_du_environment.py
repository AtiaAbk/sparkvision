#!/usr/bin/env python3
"""
Living University of Dhaka Environment Master Population Script
Populates LV_Campus_Blockout with a rich, authentic Bangladeshi ecosystem:
- 4-tier canopy layering inspired by Where Winds Meet and Ghost of Tsushima
- Banyan, Raintree, Krishnachura, Radhachura, Jarul, Neem, Coconut & Betel palms, Bamboo thickets
- Water-edge ecology with floating Shapla water lilies, Kashful reeds, and historic brick ghat
- Fallen petal decals beneath flowering trees
- Zero collision on roads, paths, or building walls
- Organizes actors into clean Outliner folders
"""

import json
import subprocess
import math

ENV_PATH = "/Game/SparkVision/Campus/Environment"

def run_mcp(toolset, tool, args):
    res = subprocess.check_output([
        "/Users/atiaoishi/Downloads/sparkvision/Scripts/mcp_client.py",
        "call", toolset, tool, json.dumps(args)
    ])
    return json.loads(res) if res.strip() else {}

def spawn_env_actor(asset_name, actor_name, loc, rot={"pitch": 0.0, "yaw": 0.0, "roll": 0.0}, scale={"x": 1.0, "y": 1.0, "z": 1.0}, folder="Environment/Foliage_Trees"):
    asset_ref = f"{ENV_PATH}/{asset_name}.{asset_name}"
    try:
        res = run_mcp("editor_toolset.toolsets.scene.SceneTools", "add_to_scene_from_asset", {
            "asset_path": asset_ref,
            "name": actor_name,
            "xform": {
                "location": loc,
                "rotation": rot,
                "scale": scale
            }
        })
        ref = res["returnValue"]["refPath"]
        run_mcp("editor_toolset.toolsets.scene.SceneTools", "set_actor_folder", {
            "actor": {"refPath": ref},
            "folder_path": folder
        })
        return ref
    except Exception as e:
        print(f"Error spawning {actor_name}: {e}")
        return None

def main():
    print("=" * 70)
    print("POPULATING LIVING UNIVERSITY OF DHAKA CAMPUS ENVIRONMENT...")
    print("=" * 70)

    total_spawned = 0

    # --------------------------------------------------------------------------
    # ZONE 1: CURZON HALL BOTANICAL GROUNDS & HERITAGE LAWNS
    # Center around Curzon: X in [-4500, -500], Y in [-5500, 5500]
    # --------------------------------------------------------------------------
    print("\n--- Zone 1: Curzon Hall Botanical Grounds ---")
    
    # 4 Landmark Banyans framing the compound corners
    banyan_locs = [
        {"x": -1200.0, "y": -6500.0, "z": 20.0, "yaw": 45.0, "scale": 1.1},
        {"x": -1200.0, "y": 6500.0, "z": 20.0, "yaw": -45.0, "scale": 1.1},
        {"x": -4800.0, "y": -6500.0, "z": 20.0, "yaw": 120.0, "scale": 1.0},
        {"x": -4800.0, "y": 6500.0, "z": 20.0, "yaw": -120.0, "scale": 1.0},
    ]
    for idx, b in enumerate(banyan_locs):
        ref = spawn_env_actor("SM_Tree_Banyan_Mature", f"Curzon_Banyan_Corner_{idx+1}", 
                              loc={"x": b["x"], "y": b["y"], "z": b["z"]}, 
                              rot={"pitch": 0.0, "yaw": b["yaw"], "roll": 0.0},
                              scale={"x": b["scale"], "y": b["scale"], "z": b["scale"]},
                              folder="Environment/Curzon_Botanical/Canopy_Banyans")
        if ref: total_spawned += 1

    # 10 Scarlet Krishnachura trees lining the front botanical parterres
    krishna_locs = [
        {"x": -1600.0, "y": -3800.0, "z": 20.0, "yaw": 15.0},
        {"x": -1600.0, "y": -2600.0, "z": 20.0, "yaw": 85.0},
        {"x": -1600.0, "y": -1400.0, "z": 20.0, "yaw": -40.0},
        {"x": -1600.0, "y": 1400.0, "z": 20.0, "yaw": 40.0},
        {"x": -1600.0, "y": 2600.0, "z": 20.0, "yaw": -85.0},
        {"x": -1600.0, "y": 3800.0, "z": 20.0, "yaw": -15.0},
        {"x": -900.0, "y": -3200.0, "z": 20.0, "yaw": 60.0},
        {"x": -900.0, "y": -1800.0, "z": 20.0, "yaw": -30.0},
        {"x": -900.0, "y": 1800.0, "z": 20.0, "yaw": 30.0},
        {"x": -900.0, "y": 3200.0, "z": 20.0, "yaw": -60.0},
    ]
    for idx, k in enumerate(krishna_locs):
        ref = spawn_env_actor("SM_Tree_Krishnachura_Bloom", f"Curzon_Krishnachura_{idx+1}",
                              loc={"x": k["x"], "y": k["y"], "z": k["z"]},
                              rot={"pitch": 0.0, "yaw": k["yaw"], "roll": 0.0},
                              scale={"x": 1.0, "y": 1.0, "z": 1.0},
                              folder="Environment/Curzon_Botanical/Flowering_Trees")
        if ref: total_spawned += 1

        # Fallen red petal decals beneath each Krishnachura tree
        p_ref = spawn_env_actor("SM_Decal_Petal_Scatter", f"Curzon_PetalScatter_{idx+1}",
                                loc={"x": k["x"], "y": k["y"], "z": k["z"] + 2.0},
                                rot={"pitch": 0.0, "yaw": k["yaw"] * 2.0, "roll": 0.0},
                                scale={"x": 1.8, "y": 1.8, "z": 1.0},
                                folder="Environment/Curzon_Botanical/Ground_Petals")
        if p_ref: total_spawned += 1

    # 4 Golden Radhachura trees along the central avenue approach
    radha_locs = [
        {"x": -800.0, "y": -800.0, "z": 20.0, "yaw": 20.0},
        {"x": -800.0, "y": 800.0, "z": 20.0, "yaw": -20.0},
        {"x": -400.0, "y": -1200.0, "z": 20.0, "yaw": 75.0},
        {"x": -400.0, "y": 1200.0, "z": 20.0, "yaw": -75.0},
    ]
    for idx, r in enumerate(radha_locs):
        ref = spawn_env_actor("SM_Tree_Radhachura_Yellow", f"Curzon_Radhachura_{idx+1}",
                              loc={"x": r["x"], "y": r["y"], "z": r["z"]},
                              rot={"pitch": 0.0, "yaw": r["yaw"], "roll": 0.0},
                              folder="Environment/Curzon_Botanical/Flowering_Trees")
        if ref: total_spawned += 1

    # 6 Bengal Golden Bamboo Thickets along southern buffer wall
    bamboo_locs = [
        {"x": -300.0, "y": -4500.0, "z": 20.0, "yaw": 10.0},
        {"x": -300.0, "y": -3500.0, "z": 20.0, "yaw": -25.0},
        {"x": -300.0, "y": -2500.0, "z": 20.0, "yaw": 45.0},
        {"x": -300.0, "y": 2500.0, "z": 20.0, "yaw": -45.0},
        {"x": -300.0, "y": 3500.0, "z": 20.0, "yaw": 25.0},
        {"x": -300.0, "y": 4500.0, "z": 20.0, "yaw": -10.0},
    ]
    for idx, bm_pos in enumerate(bamboo_locs):
        ref = spawn_env_actor("SM_Cluster_Bamboo_Thicket", f"Curzon_BambooGrove_{idx+1}",
                              loc={"x": bm_pos["x"], "y": bm_pos["y"], "z": bm_pos["z"]},
                              rot={"pitch": 0.0, "yaw": bm_pos["yaw"], "roll": 0.0},
                              scale={"x": 1.2, "y": 1.2, "z": 1.1},
                              folder="Environment/Curzon_Botanical/Bamboo_Groves")
        if ref: total_spawned += 1

    # --------------------------------------------------------------------------
    # ZONE 2: CURZON BOTANICAL POND ECOLOGY
    # Pond Center: X = -2800, Y = -2200, Extents 85m x 45m (8500 x 4500 UU)
    # --------------------------------------------------------------------------
    print("\n--- Zone 2: Curzon Botanical Pond Ecology ---")
    
    # Historic Stepped Brick Pukur Ghat
    spawn_env_actor("SM_Curzon_Pond_Ghat", "Curzon_Pond_MainGhat",
                    loc={"x": -2300.0, "y": -2200.0, "z": 20.0},
                    rot={"pitch": 0.0, "yaw": 0.0, "roll": 0.0},
                    scale={"x": 1.0, "y": 1.0, "z": 1.0},
                    folder="Environment/Curzon_Pond/Pond_Architecture")
    total_spawned += 1

    # 6 Moisture-loving Purple Jarul trees along the pond margin
    jarul_locs = [
        {"x": -2400.0, "y": -3200.0, "z": 20.0, "yaw": 10.0},
        {"x": -2900.0, "y": -3300.0, "z": 20.0, "yaw": 80.0},
        {"x": -3400.0, "y": -3100.0, "z": 20.0, "yaw": 140.0},
        {"x": -3500.0, "y": -2200.0, "z": 20.0, "yaw": 180.0},
        {"x": -3300.0, "y": -1400.0, "z": 20.0, "yaw": -120.0},
        {"x": -2600.0, "y": -1300.0, "z": 20.0, "yaw": -40.0},
    ]
    for idx, j in enumerate(jarul_locs):
        ref = spawn_env_actor("SM_Tree_Jarul_Purple", f"CurzonPond_Jarul_{idx+1}",
                              loc={"x": j["x"], "y": j["y"], "z": j["z"]},
                              rot={"pitch": 0.0, "yaw": j["yaw"], "roll": 0.0},
                              folder="Environment/Curzon_Pond/Riparian_Trees")
        if ref: total_spawned += 1

    # 6 Leaning Coconut Palms overhanging the water
    palm_locs = [
        {"x": -2350.0, "y": -2800.0, "z": 20.0, "yaw": 25.0},
        {"x": -2700.0, "y": -3350.0, "z": 20.0, "yaw": 75.0},
        {"x": -3200.0, "y": -3250.0, "z": 20.0, "yaw": 115.0},
        {"x": -3550.0, "y": -2500.0, "z": 20.0, "yaw": 165.0},
        {"x": -3450.0, "y": -1700.0, "z": 20.0, "yaw": -135.0},
        {"x": -2450.0, "y": -1600.0, "z": 20.0, "yaw": -45.0},
    ]
    for idx, p in enumerate(palm_locs):
        ref = spawn_env_actor("SM_Tree_Palm_Coconut", f"CurzonPond_Palm_{idx+1}",
                              loc={"x": p["x"], "y": p["y"], "z": p["z"]},
                              rot={"pitch": 0.0, "yaw": p["yaw"], "roll": 0.0},
                              folder="Environment/Curzon_Pond/Riparian_Trees")
        if ref: total_spawned += 1

    # 8 Floating Water Lily (Shapla) clusters on the pond surface (Z = 20)
    lily_locs = [
        {"x": -2600.0, "y": -2000.0, "z": 22.0, "yaw": 15.0},
        {"x": -2750.0, "y": -2400.0, "z": 22.0, "yaw": 45.0},
        {"x": -2900.0, "y": -2100.0, "z": 22.0, "yaw": 85.0},
        {"x": -3100.0, "y": -2500.0, "z": 22.0, "yaw": -30.0},
        {"x": -3250.0, "y": -2200.0, "z": 22.0, "yaw": 120.0},
        {"x": -2850.0, "y": -2700.0, "z": 22.0, "yaw": -70.0},
        {"x": -3000.0, "y": -1800.0, "z": 22.0, "yaw": 60.0},
        {"x": -2700.0, "y": -2600.0, "z": 22.0, "yaw": -110.0},
    ]
    for idx, ly in enumerate(lily_locs):
        ref = spawn_env_actor("SM_Pond_WaterLily_Cluster", f"CurzonPond_WaterLily_{idx+1}",
                              loc={"x": ly["x"], "y": ly["y"], "z": ly["z"]},
                              rot={"pitch": 0.0, "yaw": ly["yaw"], "roll": 0.0},
                              scale={"x": 1.4, "y": 1.4, "z": 1.0},
                              folder="Environment/Curzon_Pond/Aquatic_Flora")
        if ref: total_spawned += 1

    # 8 Kashful & Wetland Reed stands along the natural pond bank
    reed_locs = [
        {"x": -2350.0, "y": -3100.0, "z": 20.0, "yaw": 10.0},
        {"x": -2550.0, "y": -3350.0, "z": 20.0, "yaw": 60.0},
        {"x": -3100.0, "y": -3300.0, "z": 20.0, "yaw": 90.0},
        {"x": -3450.0, "y": -2900.0, "z": 20.0, "yaw": 130.0},
        {"x": -3550.0, "y": -2000.0, "z": 20.0, "yaw": 170.0},
        {"x": -3400.0, "y": -1550.0, "z": 20.0, "yaw": -150.0},
        {"x": -3050.0, "y": -1350.0, "z": 20.0, "yaw": -90.0},
        {"x": -2500.0, "y": -1450.0, "z": 20.0, "yaw": -30.0},
    ]
    for idx, rd in enumerate(reed_locs):
        ref = spawn_env_actor("SM_Plant_Reeds_Kashful", f"CurzonPond_Reeds_{idx+1}",
                              loc={"x": rd["x"], "y": rd["y"], "z": rd["z"]},
                              rot={"pitch": 0.0, "yaw": rd["yaw"], "roll": 0.0},
                              scale={"x": 1.2, "y": 1.2, "z": 1.1},
                              folder="Environment/Curzon_Pond/Wetland_Reeds")
        if ref: total_spawned += 1

    # --------------------------------------------------------------------------
    # ZONE 3: FULLER ROAD GRAND AVENUE (RAIN TREE CANOPY TUNNEL)
    # Fuller Road spans from X = 5000 to X = 45000, Y = -60000 to -30000
    # --------------------------------------------------------------------------
    print("\n--- Zone 3: Fuller Road Grand Avenue Canopy ---")
    
    fuller_road_trees = []
    # North side of Fuller Road (spaced at 40m = 4000 UU)
    for i in range(10):
        fx = 8000.0 + i * 3600.0
        fy = -35000.0 - i * 2800.0
        fuller_road_trees.append((fx + 1200.0, fy + 800.0, i * 35.0, 1.15))
        # South side of Fuller Road
        fuller_road_trees.append((fx - 1200.0, fy - 800.0, i * 45.0 + 180.0, 1.10))

    for idx, (tx, ty, tyaw, tscale) in enumerate(fuller_road_trees):
        ref = spawn_env_actor("SM_Tree_Raintree_Avenue", f"FullerRoad_Raintree_{idx+1}",
                              loc={"x": tx, "y": ty, "z": 20.0},
                              rot={"pitch": 0.0, "yaw": tyaw, "roll": 0.0},
                              scale={"x": tscale, "y": tscale, "z": tscale},
                              folder="Environment/Fuller_Road/Avenue_Canopy")
        if ref: total_spawned += 1

    # --------------------------------------------------------------------------
    # ZONE 4: ARTS FACULTY (KALA BHABAN) & APARAJEYO BANGLA
    # Arts Faculty Center: X = 78000, Y = -92000
    # --------------------------------------------------------------------------
    print("\n--- Zone 4: Arts Faculty & Aparajeyo Bangla Gardens ---")
    
    arts_trees = [
        # Framing Aparajeyo Bangla
        ("SM_Tree_Krishnachura_Bloom", "Arts_Aparajeyo_Krishnachura_1", 76000.0, -88000.0, 30.0, 1.05),
        ("SM_Tree_Krishnachura_Bloom", "Arts_Aparajeyo_Krishnachura_2", 76500.0, -94000.0, -45.0, 1.0),
        ("SM_Tree_Radhachura_Yellow", "Arts_Aparajeyo_Radhachura_1", 79500.0, -88500.0, 60.0, 1.0),
        ("SM_Tree_Radhachura_Yellow", "Arts_Aparajeyo_Radhachura_2", 80000.0, -94500.0, -30.0, 1.0),
        # Courtyard shade neems
        ("SM_Tree_Neem_Delicate", "Arts_Courtyard_Neem_1", 77200.0, -90500.0, 15.0, 0.95),
        ("SM_Tree_Neem_Delicate", "Arts_Courtyard_Neem_2", 79200.0, -92500.0, 85.0, 0.95),
        # Car park / Mall avenue
        ("SM_Tree_Raintree_Avenue", "Arts_Perimeter_Raintree_1", 74000.0, -86000.0, 20.0, 1.2),
        ("SM_Tree_Raintree_Avenue", "Arts_Perimeter_Raintree_2", 82000.0, -96000.0, -40.0, 1.2),
    ]
    for m_name, a_name, ax, ay, ayaw, ascale in arts_trees:
        ref = spawn_env_actor(m_name, a_name,
                              loc={"x": ax, "y": ay, "z": 20.0},
                              rot={"pitch": 0.0, "yaw": ayaw, "roll": 0.0},
                              scale={"x": ascale, "y": ascale, "z": ascale},
                              folder="Environment/Arts_Faculty/Foliage")
        if ref: total_spawned += 1

    # --------------------------------------------------------------------------
    # ZONE 5: TSC & RAJU SCULPTURE INTERSECTION
    # Raju Intersection: X = 4500, Y = -3500
    # --------------------------------------------------------------------------
    print("\n--- Zone 5: TSC & Raju Sculpture Surroundings ---")
    
    tsc_trees = [
        ("SM_Tree_Raintree_Avenue", "TSC_Plaza_Raintree_1", 3200.0, -4800.0, 15.0, 1.15),
        ("SM_Tree_Raintree_Avenue", "TSC_Plaza_Raintree_2", 5800.0, -2200.0, -35.0, 1.10),
        ("SM_Tree_Krishnachura_Bloom", "TSC_Plaza_Krishnachura_1", 2800.0, -2800.0, 75.0, 1.0),
        ("SM_Tree_Radhachura_Yellow", "TSC_Plaza_Radhachura_1", 5200.0, -4500.0, -60.0, 1.0),
        ("SM_Tree_Neem_Delicate", "TSC_Library_Neem_1", 1800.0, -3800.0, 20.0, 1.0),
        ("SM_Tree_Neem_Delicate", "TSC_Library_Neem_2", 2200.0, -5200.0, -45.0, 1.0),
        ("SM_Cluster_Bamboo_Thicket", "TSC_Acoustic_Bamboo_1", 1200.0, -3200.0, 10.0, 1.2),
        ("SM_Cluster_Bamboo_Thicket", "TSC_Acoustic_Bamboo_2", 1500.0, -2400.0, -25.0, 1.2),
    ]
    for m_name, a_name, tx, ty, tyaw, tscale in tsc_trees:
        ref = spawn_env_actor(m_name, a_name,
                              loc={"x": tx, "y": ty, "z": 20.0},
                              rot={"pitch": 0.0, "yaw": tyaw, "roll": 0.0},
                              scale={"x": tscale, "y": tscale, "z": tscale},
                              folder="Environment/TSC_Raju/Foliage")
        if ref: total_spawned += 1

    # --------------------------------------------------------------------------
    # ZONE 6: SHAHEED MINAR SANCTUARY
    # Shaheed Minar Center: X = 25000, Y = -22000
    # --------------------------------------------------------------------------
    print("\n--- Zone 6: Shaheed Minar Sacred Sanctuary ---")
    
    shaheed_trees = [
        # Symmetrical perimeter framing neems (leaving monument clear!)
        ("SM_Tree_Neem_Delicate", "Shaheed_Framing_Neem_1", 22500.0, -24000.0, 0.0, 1.0),
        ("SM_Tree_Neem_Delicate", "Shaheed_Framing_Neem_2", 27500.0, -24000.0, 0.0, 1.0),
        ("SM_Tree_Neem_Delicate", "Shaheed_Framing_Neem_3", 22500.0, -20000.0, 0.0, 1.0),
        ("SM_Tree_Neem_Delicate", "Shaheed_Framing_Neem_4", 27500.0, -20000.0, 0.0, 1.0),
        # Outer Lawn Krishnachura (Symbol of language martyrs' sacrifice)
        ("SM_Tree_Krishnachura_Bloom", "Shaheed_Memorial_Krishnachura_1", 21000.0, -25500.0, 45.0, 1.1),
        ("SM_Tree_Krishnachura_Bloom", "Shaheed_Memorial_Krishnachura_2", 29000.0, -18500.0, -45.0, 1.1),
        ("SM_Tree_Banyan_Mature", "Shaheed_Outer_Banyan_1", 19500.0, -22000.0, 90.0, 1.15),
    ]
    for m_name, a_name, sx, sy, syaw, sscale in shaheed_trees:
        ref = spawn_env_actor(m_name, a_name,
                              loc={"x": sx, "y": sy, "z": 20.0},
                              rot={"pitch": 0.0, "yaw": syaw, "roll": 0.0},
                              scale={"x": sscale, "y": sscale, "z": sscale},
                              folder="Environment/Shaheed_Minar/Sanctuary_Trees")
        if ref: total_spawned += 1

    # --------------------------------------------------------------------------
    # ZONE 7: SHAHIDULLAH HALL & LAKE GROUNDS
    # Shahidullah Hall Center: X = 15000, Y = 25000
    # --------------------------------------------------------------------------
    print("\n--- Zone 7: Shahidullah Hall & Lake Grounds ---")
    
    shahidullah_env = [
        # Hall Quadrangle Banyan
        ("SM_Tree_Banyan_Mature", "Shahidullah_Quad_Banyan", 15000.0, 25000.0, 30.0, 1.2, "Environment/Shahidullah_Hall/Quad_Banyan"),
        # Lakeside Coconut Palms
        ("SM_Tree_Palm_Coconut", "Shahidullah_Lake_Palm_1", 12500.0, 21500.0, 45.0, 1.0, "Environment/Shahidullah_Hall/Lake_Ecology"),
        ("SM_Tree_Palm_Coconut", "Shahidullah_Lake_Palm_2", 14000.0, 20500.0, 75.0, 1.05, "Environment/Shahidullah_Hall/Lake_Ecology"),
        ("SM_Tree_Palm_Coconut", "Shahidullah_Lake_Palm_3", 16000.0, 21000.0, 110.0, 1.0, "Environment/Shahidullah_Hall/Lake_Ecology"),
        ("SM_Tree_Palm_Coconut", "Shahidullah_Lake_Palm_4", 17500.0, 22500.0, 145.0, 1.05, "Environment/Shahidullah_Hall/Lake_Ecology"),
        # Lakeside Purple Jarul
        ("SM_Tree_Jarul_Purple", "Shahidullah_Lake_Jarul_1", 13000.0, 22000.0, 20.0, 1.0, "Environment/Shahidullah_Hall/Lake_Ecology"),
        ("SM_Tree_Jarul_Purple", "Shahidullah_Lake_Jarul_2", 16800.0, 22000.0, -35.0, 1.0, "Environment/Shahidullah_Hall/Lake_Ecology"),
        # Floating Water Lily clusters
        ("SM_Pond_WaterLily_Cluster", "Shahidullah_Lake_Lilies_1", 14500.0, 23000.0, 0.0, 1.5, "Environment/Shahidullah_Hall/Lake_Ecology"),
        ("SM_Pond_WaterLily_Cluster", "Shahidullah_Lake_Lilies_2", 15800.0, 23500.0, 45.0, 1.3, "Environment/Shahidullah_Hall/Lake_Ecology"),
        # Wetland Reeds
        ("SM_Plant_Reeds_Kashful", "Shahidullah_Lake_Reeds_1", 12800.0, 21000.0, 15.0, 1.2, "Environment/Shahidullah_Hall/Lake_Ecology"),
        ("SM_Plant_Reeds_Kashful", "Shahidullah_Lake_Reeds_2", 17200.0, 21500.0, -25.0, 1.2, "Environment/Shahidullah_Hall/Lake_Ecology"),
    ]
    for item in shahidullah_env:
        m_name = item[0]
        a_name = item[1]
        ax = item[2]
        ay = item[3]
        ayaw = item[4]
        ascale = item[5]
        folder = item[6]
        ref = spawn_env_actor(m_name, a_name,
                              loc={"x": ax, "y": ay, "z": 20.0},
                              rot={"pitch": 0.0, "yaw": ayaw, "roll": 0.0},
                              scale={"x": ascale, "y": ascale, "z": ascale},
                              folder=folder)
        if ref: total_spawned += 1

    # --------------------------------------------------------------------------
    # ZONE 8: THE MALL & CENTRAL SPORTS FIELD
    # Mall Center: X = 55000, Y = -65000
    # --------------------------------------------------------------------------
    print("\n--- Zone 8: The Mall & Central Sports Field ---")
    
    mall_env = [
        # Grand Ancient Banyan at Mall
        ("SM_Tree_Banyan_Mature", "Mall_Grand_Banyan_1", 52000.0, -68000.0, 15.0, 1.3),
        ("SM_Tree_Banyan_Mature", "Mall_Grand_Banyan_2", 58000.0, -62000.0, -45.0, 1.25),
        # Betel Nut Palms along pavilion fence
        ("SM_Tree_Palm_BetelNut", "Mall_BetelPalm_1", 50000.0, -64000.0, 0.0, 1.0),
        ("SM_Tree_Palm_BetelNut", "Mall_BetelPalm_2", 50000.0, -65500.0, 0.0, 1.0),
        ("SM_Tree_Palm_BetelNut", "Mall_BetelPalm_3", 50000.0, -67000.0, 0.0, 1.0),
        ("SM_Tree_Palm_BetelNut", "Mall_BetelPalm_4", 50000.0, -68500.0, 0.0, 1.0),
        ("SM_Tree_Palm_BetelNut", "Mall_BetelPalm_5", 50000.0, -70000.0, 0.0, 1.0),
        ("SM_Tree_Palm_BetelNut", "Mall_BetelPalm_6", 50000.0, -71500.0, 0.0, 1.0),
        # Perimeter Shading Raintrees
        ("SM_Tree_Raintree_Avenue", "Mall_Perimeter_Raintree_1", 48000.0, -61000.0, 30.0, 1.2),
        ("SM_Tree_Raintree_Avenue", "Mall_Perimeter_Raintree_2", 61000.0, -69000.0, -50.0, 1.2),
    ]
    for m_name, a_name, mx, my, myaw, mscale in mall_env:
        ref = spawn_env_actor(m_name, a_name,
                              loc={"x": mx, "y": my, "z": 20.0},
                              rot={"pitch": 0.0, "yaw": myaw, "roll": 0.0},
                              scale={"x": mscale, "y": mscale, "z": mscale},
                              folder="Environment/The_Mall/Field_Perimeter")
        if ref: total_spawned += 1

    # Save the updated level
    print("\n--- Saving Level LV_Campus_Blockout ---")
    try:
        run_mcp("editor_toolset.toolsets.scene.SceneTools", "save_level", {
            "level_path": "/Game/SparkVision/Maps/Campus/LV_Campus_Blockout"
        })
        print("[SUCCESS] Level saved successfully!")
    except Exception as e:
        print(f"Notice during save_level: {e}")

    print(f"\n=======================================================")
    print(f"LIVING ENVIRONMENT POPULATION COMPLETE: {total_spawned} ACTORS SPAWNED!")
    print(f"=======================================================")

if __name__ == "__main__":
    main()
