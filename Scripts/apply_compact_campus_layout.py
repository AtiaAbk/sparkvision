#!/usr/bin/env python3
"""
Apply Compact Semi-Open-World University of Dhaka Layout
Moves all landmarks, roads, boundaries, foliage, and gameplay actors
to their mathematically calibrated compact positions in LV_Level01_Compact_Campus.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from mcp_client import invoke_tool

def set_actor_xform(actor_ref, loc, rot=None, scale=None):
    xform = {"location": loc}
    if rot is not None:
        xform["rotation"] = rot
    if scale is not None:
        xform["scale"] = scale
    return invoke_tool("set_actor_transform", "editor_toolset.toolsets.actor.ActorTools", {
        "actor": {"refPath": actor_ref},
        "xform": xform,
        "worldspace": True
    })

def find_actor_by_label(label_or_name):
    # Find all actors in scene
    res = invoke_tool("find_actors", "editor_toolset.toolsets.scene.SceneTools", {
        "name": label_or_name,
        "tag": "",
        "collision_channels": []
    })
    actors = res.get("returnValue", [])
    if actors:
        return actors[0]["refPath"]
    return None

def main():
    print("=" * 70)
    print("APPLYING COMPACT CAMPUS GEOGRAPHIC TRANSFORMATION")
    print("Level: /Game/SparkVision/Maps/Level01/LV_Level01_Compact_Campus")
    print("=" * 70)

    # Verify current level
    cur_lvl = invoke_tool("get_current_level", "editor_toolset.toolsets.scene.SceneTools").get("returnValue", "")
    print(f"Active Level: {cur_lvl}")
    if "LV_Level01_Compact_Campus" not in cur_lvl:
        print("Loading LV_Level01_Compact_Campus first...")
        invoke_tool("load_level", "editor_toolset.toolsets.scene.SceneTools", {
            "level_path": "/Game/SparkVision/Maps/Level01/LV_Level01_Compact_Campus"
        })

    # Load original actors dump to map refPaths
    with open("/Users/atiaoishi/Downloads/sparkvision/Documentation/WorldCorrection/original_campus_actors.json") as f:
        inv = json.load(f)

    # Flatten inventory by label and refPath
    ref_by_label = {}
    for fld, actors in inv.items():
        for a in actors:
            lbl = a["label"]
            ref_by_label[lbl] = a["refPath"]
            # Also store short name
            short = a["refPath"].split(".")[-1]
            ref_by_label[short] = a["refPath"]

    print(f"Total indexed scene actors: {len(ref_by_label)}")

    # 1. LANDMARKS TRANSFORMATION
    LANDMARK_TARGETS = [
        # Doyel Chattar & Bangla Academy
        {"label": "Hero_DoyelChattar_Monument", "loc": {"x": 5500.0, "y": -8500.0, "z": 20.0}},
        {"label": "Supporting_BanglaAcademyComplex", "loc": {"x": 11000.0, "y": -12000.0, "z": 20.0}},
        {"label": "Doyel_Lamp_1", "loc": {"x": 4700.0, "y": -8500.0, "z": 20.0}},
        {"label": "Doyel_Lamp_2", "loc": {"x": 6300.0, "y": -8500.0, "z": 20.0}},
        {"label": "Doyel_Lamp_3", "loc": {"x": 5500.0, "y": -7700.0, "z": 20.0}},
        {"label": "Doyel_Lamp_4", "loc": {"x": 5500.0, "y": -9300.0, "z": 20.0}},

        # Shaheed Minar
        {"label": "Hero_ShaheedMinar_Monument", "loc": {"x": 0.0, "y": -19000.0, "z": 20.0}},
        {"label": "ShaheedMinar_Lamp_1", "loc": {"x": -1200.0, "y": -19800.0, "z": 20.0}},
        {"label": "ShaheedMinar_Lamp_2", "loc": {"x": -1200.0, "y": -18200.0, "z": 20.0}},
        {"label": "ShaheedMinar_Lamp_3", "loc": {"x": 1200.0, "y": -19800.0, "z": 20.0}},
        {"label": "ShaheedMinar_Lamp_4", "loc": {"x": 1200.0, "y": -18200.0, "z": 20.0}},

        # Student Halls
        {"label": "Hero_DrShahidullah_Hall", "loc": {"x": 4000.0, "y": -5500.0, "z": 20.0}},
        {"label": "Supporting_JagannathHallComplex", "loc": {"x": 8000.0, "y": -22000.0, "z": 20.0}},
        {"label": "Hero_SalimullahMuslim_Hall", "loc": {"x": 3000.0, "y": -26000.0, "z": 20.0}},
        {"label": "Hero_Rokeya_Hall", "loc": {"x": 12000.0, "y": -26000.0, "z": 20.0}},
        {"label": "Supporting_SurjaSenHallBlock", "loc": {"x": 27000.0, "y": -39000.0, "z": 20.0}},
        {"label": "Supporting_HajiMuhammadMohsinHall", "loc": {"x": 25000.0, "y": -42000.0, "z": 20.0}},

        # TSC & Raju Memorial
        {"label": "RajuMemorialSculpture_CustomArtMesh", "loc": {"x": 18000.0, "y": -24000.0, "z": 20.0}},
        {"label": "Hero_TSC_AuditoriumComplex", "loc": {"x": 20500.0, "y": -21500.0, "z": 20.0}},
        {"label": "TSC_Cafeteria_CourtyardRing", "loc": {"x": 21000.0, "y": -19500.0, "z": 20.0}},

        # Central Library & Hakim Chattar
        {"label": "Hero_CentralLibrary_Building", "loc": {"x": 26000.0, "y": -27000.0, "z": 20.0}},
        {"label": "HakimChattar_Bench_1", "loc": {"x": 25000.0, "y": -26000.0, "z": 20.0}},
        {"label": "HakimChattar_Bench_2", "loc": {"x": 25000.0, "y": -26500.0, "z": 20.0}},

        # Central Mosque & Nazrul Mausoleum
        {"label": "Hero_DU_CentralMosque", "loc": {"x": 31000.0, "y": -27500.0, "z": 20.0}},
        {"label": "Hero_NazrulIslam_Mausoleum", "loc": {"x": 33500.0, "y": -27000.0, "z": 20.0}},

        # Arts Faculty / Kala Bhaban & Aparajeyo Bangla
        {"label": "Hero_AparajeyoBangla_Sculpture", "loc": {"x": 28000.0, "y": -35000.0, "z": 20.0}},
        {"label": "ArtsFaculty_KalaBhaban_AcademicBlock", "loc": {"x": 31000.0, "y": -36000.0, "z": 20.0}},

        # Supporting Academic & Administrative
        {"label": "Supporting_AdminBuilding", "loc": {"x": 25000.0, "y": -32000.0, "z": 20.0}},
        {"label": "Supporting_IBABuilding", "loc": {"x": 16000.0, "y": -18000.0, "z": 20.0}},
        {"label": "Supporting_CurzonChemistryPhysicsLabs", "loc": {"x": 5000.0, "y": 4200.0, "z": 20.0}},
        {"label": "Supporting_Curzon_PhysicsAnnex", "loc": {"x": 5000.0, "y": -4200.0, "z": 20.0}},
    ]

    print("\n--- Transforming Landmark Positions ---")
    transformed_count = 0
    for target in LANDMARK_TARGETS:
        lbl = target["label"]
        ref = ref_by_label.get(lbl)
        if not ref:
            # try search
            ref = find_actor_by_label(lbl)
        if ref:
            try:
                set_actor_xform(ref, target["loc"], target.get("rot"), target.get("scale"))
                print(f"  ✓ Transformed {lbl} -> ({target['loc']['x']}, {target['loc']['y']}, {target['loc']['z']})")
                transformed_count += 1
            except Exception as e:
                print(f"  ✗ Error transforming {lbl}: {e}")
        else:
            print(f"  ? Actor '{lbl}' not found in index or scene")
    print(f"Transformed {transformed_count}/{len(LANDMARK_TARGETS)} landmarks.")

    # 2. ROAD NETWORK TRANSFORMATION
    ROAD_TARGETS = [
        {"label": "PrimaryRoad_Curzon_To_DoyelChattar", "loc": {"x": 1500.0, "y": -4250.0, "z": 6.0}, "rot": {"pitch": 0.0, "yaw": -70.0, "roll": 0.0}, "scale": {"x": 1.2, "y": 0.4, "z": 1.0}},
        {"label": "PrimaryRoad_FullerRoad_To_ShaheedMinar", "loc": {"x": 2500.0, "y": -14500.0, "z": 6.0}, "rot": {"pitch": 0.0, "yaw": 0.0, "roll": 0.0}, "scale": {"x": 0.8, "y": 1.2, "z": 1.0}},
        {"label": "PrimaryRoad_TSCMor_RajuPlaza", "loc": {"x": 18000.0, "y": -24000.0, "z": 6.0}, "rot": {"pitch": 0.0, "yaw": 0.0, "roll": 0.0}, "scale": {"x": 1.0, "y": 1.0, "z": 1.0}},
        {"label": "PrimaryRoad_NazrulAve_TSC_To_Library", "loc": {"x": 22000.0, "y": -25500.0, "z": 6.0}, "rot": {"pitch": 0.0, "yaw": -20.0, "roll": 0.0}, "scale": {"x": 0.8, "y": 0.5, "z": 1.0}},
        {"label": "PrimaryRoad_NazrulAve_Library_To_Shahbagh", "loc": {"x": 29500.0, "y": -27250.0, "z": 6.0}, "rot": {"pitch": 0.0, "yaw": 0.0, "roll": 0.0}, "scale": {"x": 0.8, "y": 0.5, "z": 1.0}},
        {"label": "PrimaryRoad_MallRoad_To_ArtsFaculty", "loc": {"x": 27000.0, "y": -31000.0, "z": 6.0}, "rot": {"pitch": 0.0, "yaw": -80.0, "roll": 0.0}, "scale": {"x": 0.8, "y": 0.8, "z": 1.0}},
        {"label": "PrimaryRoad_UniversityAve_Segment1", "loc": {"x": 14000.0, "y": -15000.0, "z": 6.0}, "rot": {"pitch": 0.0, "yaw": -30.0, "roll": 0.0}, "scale": {"x": 0.8, "y": 0.6, "z": 1.0}},
        {"label": "PrimaryRoad_UniversityAve_Segment2", "loc": {"x": 16000.0, "y": -20000.0, "z": 6.0}, "rot": {"pitch": 0.0, "yaw": -15.0, "roll": 0.0}, "scale": {"x": 0.8, "y": 0.6, "z": 1.0}},
    ]
    print("\n--- Transforming Primary Road Network ---")
    for r in ROAD_TARGETS:
        lbl = r["label"]
        ref = ref_by_label.get(lbl) or find_actor_by_label(lbl)
        if ref:
            try:
                set_actor_xform(ref, r["loc"], r["rot"], r["scale"])
                print(f"  ✓ Aligned road {lbl}")
            except Exception as e:
                print(f"  ✗ Road error {lbl}: {e}")

    # 3. PERIMETER BOUNDARIES
    BOUNDARY_TARGETS = [
        {"label": "Boundary_Wall_East_HighCourt", "loc": {"x": 5000.0, "y": 7500.0, "z": 20.0}, "rot": {"pitch": 0.0, "yaw": 90.0, "roll": 0.0}, "scale": {"x": 2.5, "y": 1.0, "z": 1.5}},
        {"label": "Boundary_Wall_South_Nimtoli", "loc": {"x": -6000.0, "y": 0.0, "z": 20.0}, "rot": {"pitch": 0.0, "yaw": 0.0, "roll": 0.0}, "scale": {"x": 1.8, "y": 1.0, "z": 1.5}},
        {"label": "Boundary_Wall_West_Nilkhet", "loc": {"x": 25000.0, "y": -46000.0, "z": 20.0}, "rot": {"pitch": 0.0, "yaw": 90.0, "roll": 0.0}, "scale": {"x": 2.5, "y": 1.0, "z": 1.5}},
        {"label": "Boundary_Wall_North_Shahbagh", "loc": {"x": 36000.0, "y": -30000.0, "z": 20.0}, "rot": {"pitch": 0.0, "yaw": 0.0, "roll": 0.0}, "scale": {"x": 3.0, "y": 1.0, "z": 1.5}},
    ]
    print("\n--- Setting Campus Perimeter Enclosure ---")
    for b in BOUNDARY_TARGETS:
        lbl = b["label"]
        ref = ref_by_label.get(lbl) or find_actor_by_label(lbl)
        if ref:
            try:
                set_actor_xform(ref, b["loc"], b["rot"], b["scale"])
                print(f"  ✓ Set perimeter boundary {lbl}")
            except Exception as e:
                print(f"  ✗ Boundary error {lbl}: {e}")

    # 4. DISTANT SKYLINES (INFINITE-WORLD ILLUSION)
    SKYLINE_TARGETS = [
        {"pattern": "Skyline", "index": 0, "loc": {"x": 48000.0, "y": -28000.0, "z": 20.0}, "scale": {"x": 2.0, "y": 2.0, "z": 2.0}},
        {"pattern": "Skyline", "index": 1, "loc": {"x": 12000.0, "y": 22000.0, "z": 20.0}, "scale": {"x": 2.0, "y": 2.0, "z": 2.0}},
        {"pattern": "Skyline", "index": 2, "loc": {"x": 28000.0, "y": -58000.0, "z": 20.0}, "scale": {"x": 2.0, "y": 2.0, "z": 2.0}},
        {"pattern": "Skyline", "index": 3, "loc": {"x": -18000.0, "y": -12000.0, "z": 20.0}, "scale": {"x": 2.0, "y": 2.0, "z": 2.0}},
    ]
    print("\n--- Setting Distant Backdrop Skylines ---")
    skylines = inv.get("Distant_Skyline", [])
    for idx, sk in enumerate(SKYLINE_TARGETS):
        if idx < len(skylines):
            ref = skylines[idx]["refPath"]
            try:
                set_actor_xform(ref, sk["loc"], scale=sk["scale"])
                print(f"  ✓ Positioned backdrop skyline #{idx+1} at {sk['loc']}")
            except Exception as e:
                print(f"  ✗ Skyline error #{idx+1}: {e}")

    # 5. ENVIRONMENT FLORA CLUSTERS RE-ANCHORING
    # Re-anchor vegetation around Doyel Chattar, Shaheed Minar, TSC, Arts Faculty
    cluster_shifts = {
        "Environment/Doyel_Chattar": {"dx": 5500.0 - 7507.0, "dy": -8500.0 - (-16487.0)},
        "Environment/Shaheed_Minar": {"dx": 0.0 - (-282.0), "dy": -19000.0 - (-54042.0)},
        "Environment/TSC_Raju": {"dx": 18000.0 - 58964.0, "dy": -24000.0 - (-63725.0)},
        "Environment/Arts_Faculty": {"dx": 31000.0 - 78214.0, "dy": -36000.0 - (-95794.0)},
        "Environment/Fuller_Road": {"dx": 2500.0 - 28845.0, "dy": -14500.0 - (-58849.0)},
    }
    print("\n--- Re-anchoring Environmental Flora Clusters ---")
    shifted_flora = 0
    for fld, shift in cluster_shifts.items():
        actors = inv.get(fld, [])
        for a in actors:
            ref = a["refPath"]
            orig_loc = a["location"]
            new_loc = {
                "x": orig_loc["x"] + shift["dx"],
                "y": orig_loc["y"] + shift["dy"],
                "z": 20.0 # ground anchored
            }
            try:
                set_actor_xform(ref, new_loc)
                shifted_flora += 1
            except Exception:
                pass
        print(f"  ✓ Re-anchored {len(actors)} flora actors in {fld}")

    print(f"Total flora shifted: {shifted_flora}")

    # 6. SAVE LEVEL
    print("\n--- Saving Compact Level ---")
    invoke_tool("save_assets", "editor_toolset.toolsets.asset.AssetTools", {
        "asset_paths": ["/Game/SparkVision/Maps/Level01/LV_Level01_Compact_Campus"]
    })
    print("Level saved successfully!")

if __name__ == "__main__":
    main()
