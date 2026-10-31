#!/usr/bin/env python3
"""
Assembles Phase 3 Campus Landmarks and Environment across University of Dhaka.
Places authentic 3D models at verified UTM Zone 46N coordinates and organizes scene hierarchy.
"""

import json
import subprocess

LANDMARKS_PATH = "/Game/SparkVision/Campus/Landmarks"
FOLIAGE_PATH = "/Game/SparkVision/Campus/Foliage"
CURZON_MOD_PATH = "/Game/SparkVision/Campus/CurzonModular"

def run_mcp(toolset, tool, args):
    res = subprocess.check_output([
        "/Users/atiaoishi/Downloads/sparkvision/Scripts/mcp_client.py",
        "call", toolset, tool, json.dumps(args)
    ])
    return json.loads(res) if res.strip() else {}

def spawn_landmark(asset_path, name, folder, loc, rot={"pitch": 0.0, "yaw": 0.0, "roll": 0.0}, scale={"x": 1.0, "y": 1.0, "z": 1.0}):
    res = run_mcp("editor_toolset.toolsets.scene.SceneTools", "add_to_scene_from_asset", {
        "asset_path": asset_path,
        "name": name,
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
    print(f"Spawned {name} -> {folder} at {loc}")
    return ref

print("=== Phase 3 Campus Assembly Starting ===")

# 1. Remove old primitive blockout placeholders and debug orientation actors
old_actors_to_remove = [
    "/Game/SparkVision/Maps/Campus/LV_Campus_Blockout.LV_Campus_Blockout:PersistentLevel.StaticMeshActor_UAID_685EDD40918A671003_1821598901", # ShaheedMinar_CentralMotherPillar
    "/Game/SparkVision/Maps/Campus/LV_Campus_Blockout.LV_Campus_Blockout:PersistentLevel.StaticMeshActor_UAID_685EDD40918A671003_1823229902", # ShaheedMinar_CrimsonSunMonument
    "/Game/SparkVision/Maps/Campus/LV_Campus_Blockout.LV_Campus_Blockout:PersistentLevel.StaticMeshActor_UAID_685EDD40918A671003_1823523903", # ShaheedMinar_LeftFlankingPillar
    "/Game/SparkVision/Maps/Campus/LV_Campus_Blockout.LV_Campus_Blockout:PersistentLevel.StaticMeshActor_UAID_685EDD40918A671003_1823693904", # ShaheedMinar_RightFlankingPillar
    "/Game/SparkVision/Maps/Campus/LV_Campus_Blockout.LV_Campus_Blockout:PersistentLevel.StaticMeshActor_UAID_685EDD40918A671003_1814941896", # KaziNazrulIslam_MausoleumCenotaph
    "/Game/SparkVision/Maps/Campus/LV_Campus_Blockout.LV_Campus_Blockout:PersistentLevel.StaticMeshActor_UAID_685EDD40918A671003_1810939893", # Raju_Pedestal
    "/Game/SparkVision/Maps/Campus/LV_Campus_Blockout.LV_Campus_Blockout:PersistentLevel.StaticMeshActor_UAID_685EDD40918A671003_1812271894", # Raju_FigureMassing
    "/Game/SparkVision/Maps/Campus/LV_Campus_Blockout.LV_Campus_Blockout:PersistentLevel.StaticMeshActor_UAID_685EDD40918A671003_1817601898", # Aparajeyo_Pedestal
    "/Game/SparkVision/Maps/Campus/LV_Campus_Blockout.LV_Campus_Blockout:PersistentLevel.StaticMeshActor_UAID_685EDD40918A671003_1818942899", # Aparajeyo_TrioFigures
    "/Game/SparkVision/Maps/Campus/LV_Campus_Blockout.LV_Campus_Blockout:PersistentLevel.StaticMeshActor_UAID_685EDD40918A671003_1772266864", # North_Direction_Arrow_Needle
    "/Game/SparkVision/Maps/Campus/LV_Campus_Blockout.LV_Campus_Blockout:PersistentLevel.StaticMeshActor_UAID_685EDD40918A671003_1770934863", # North_Direction_Reference_Compass
]
for ref in old_actors_to_remove:
    try:
        run_mcp("editor_toolset.toolsets.scene.SceneTools", "remove_from_scene", {"actor": {"refPath": ref}})
        print(f"Removed legacy blockout placeholder: {ref.split('.')[-1]}")
    except Exception as e:
        pass

# 2. Doyel Chattar Roundabout & Monument
spawn_landmark(
    f"{LANDMARKS_PATH}/SM_DoyelMonument.SM_DoyelMonument",
    "Hero_DoyelChattar_Monument",
    "Hero_Buildings/Doyel_Chattar",
    loc={"x": 7507.0, "y": -16487.0, "z": 20.0},
    scale={"x": 1.2, "y": 1.2, "z": 1.2}
)
# 4 Heritage lamps around Doyel Chattar roundabout
doyel_lamps = [
    {"x": 6700.0, "y": -16487.0, "z": 20.0},
    {"x": 8300.0, "y": -16487.0, "z": 20.0},
    {"x": 7507.0, "y": -15687.0, "z": 20.0},
    {"x": 7507.0, "y": -17287.0, "z": 20.0}
]
for idx, p in enumerate(doyel_lamps):
    spawn_landmark(
        f"{CURZON_MOD_PATH}/SM_Curzon_Lamp_Colonial.SM_Curzon_Lamp_Colonial",
        f"Doyel_Lamp_{idx+1}",
        "Hero_Buildings/Doyel_Chattar",
        loc=p
    )

# 3. Central Shaheed Minar Monument
spawn_landmark(
    f"{LANDMARKS_PATH}/SM_ShaheedMinar_Monument.SM_ShaheedMinar_Monument",
    "Hero_ShaheedMinar_Monument",
    "Hero_Buildings/Shaheed_Minar",
    loc={"x": -282.0, "y": -54042.0, "z": 20.0},
    rot={"pitch": 0.0, "yaw": 0.0, "roll": 0.0}, # Faces South towards gathering square
    scale={"x": 1.0, "y": 1.0, "z": 1.0}
)
# 4 Heritage lamps at Shaheed Minar perimeter
sm_lamps = [
    {"x": -1500.0, "y": -55200.0, "z": 20.0},
    {"x": -1500.0, "y": -52800.0, "z": 20.0},
    {"x": 800.0, "y": -55200.0, "z": 20.0},
    {"x": 800.0, "y": -52800.0, "z": 20.0}
]
for idx, p in enumerate(sm_lamps):
    spawn_landmark(
        f"{CURZON_MOD_PATH}/SM_Curzon_Lamp_Colonial.SM_Curzon_Lamp_Colonial",
        f"ShaheedMinar_Lamp_{idx+1}",
        "Hero_Buildings/Shaheed_Minar",
        loc=p
    )

# 4. Teacher-Student Centre (TSC) & Raju Sculpture
spawn_landmark(
    f"{LANDMARKS_PATH}/SM_RajuSculpture.SM_RajuSculpture",
    "Hero_RajuMemorial_Sculpture",
    "Hero_Buildings/TSC_Raju",
    loc={"x": 60139.0, "y": -62695.0, "z": 100.0},
    scale={"x": 1.2, "y": 1.2, "z": 1.2}
)
spawn_landmark(
    f"{LANDMARKS_PATH}/SM_TSC_Building.SM_TSC_Building",
    "Hero_TSC_AuditoriumComplex",
    "Hero_Buildings/TSC_Raju",
    loc={"x": 50519.0, "y": -59269.0, "z": 800.0},
    scale={"x": 1.0, "y": 1.0, "z": 1.0}
)

# 5. Hakim Chattar & Central Library
spawn_landmark(
    f"{LANDMARKS_PATH}/SM_CentralLibrary.SM_CentralLibrary",
    "Hero_CentralLibrary_Building",
    "Hero_Buildings/Central_Library",
    loc={"x": 73459.0, "y": -71699.0, "z": 1000.0},
    scale={"x": 1.0, "y": 1.0, "z": 1.0}
)
# Benches at Hakim Chattar
spawn_landmark(
    f"{CURZON_MOD_PATH}/SM_Curzon_Bench_Colonial.SM_Curzon_Bench_Colonial",
    "HakimChattar_Bench_1",
    "Hero_Buildings/Central_Library",
    loc={"x": 72500.0, "y": -71200.0, "z": 20.0}
)
spawn_landmark(
    f"{CURZON_MOD_PATH}/SM_Curzon_Bench_Colonial.SM_Curzon_Bench_Colonial",
    "HakimChattar_Bench_2",
    "Hero_Buildings/Central_Library",
    loc={"x": 72500.0, "y": -72200.0, "z": 20.0}
)

# 6. Aparajeyo Bangla & Arts Faculty (Kala Bhaban)
spawn_landmark(
    f"{LANDMARKS_PATH}/SM_AparajeyoBangla.SM_AparajeyoBangla",
    "Hero_AparajeyoBangla_Sculpture",
    "Hero_Buildings/Arts_Faculty",
    loc={"x": 73486.0, "y": -95794.0, "z": 100.0},
    scale={"x": 1.2, "y": 1.2, "z": 1.2}
)

# 7. Kazi Nazrul Islam Mausoleum
spawn_landmark(
    f"{LANDMARKS_PATH}/SM_NazrulMausoleum.SM_NazrulMausoleum",
    "Hero_NazrulIslam_Mausoleum",
    "Hero_Buildings/Nazrul_Mausoleum",
    loc={"x": 87224.0, "y": -71761.0, "z": 120.0},
    scale={"x": 1.0, "y": 1.0, "z": 1.0}
)

# 8. Campus Hero Shade Trees (Mature Banyan & Raintrees)
tree_positions = [
    # Curzon Hall Gardens & Promenade
    {"loc": {"x": -3800.0, "y": -2800.0, "z": 15.0}, "scale": 1.2},
    {"loc": {"x": -3800.0, "y": 2800.0, "z": 15.0}, "scale": 1.2},
    {"loc": {"x": -2700.0, "y": -4200.0, "z": 15.0}, "scale": 1.0},
    {"loc": {"x": -2700.0, "y": 4200.0, "z": 15.0}, "scale": 1.0},
    # Doyel Chattar Approach
    {"loc": {"x": 6200.0, "y": -15000.0, "z": 20.0}, "scale": 1.3},
    {"loc": {"x": 8800.0, "y": -17500.0, "z": 20.0}, "scale": 1.1},
    # University Avenue / Suhrawardy Buffer
    {"loc": {"x": 22000.0, "y": -32000.0, "z": 20.0}, "scale": 1.4},
    {"loc": {"x": 38000.0, "y": -48000.0, "z": 20.0}, "scale": 1.4},
    # Shaheed Minar Park Perimeter
    {"loc": {"x": -1800.0, "y": -56000.0, "z": 20.0}, "scale": 1.3},
    {"loc": {"x": 1200.0, "y": -52000.0, "z": 20.0}, "scale": 1.2},
    # TSC Mor & Gathering Lawn
    {"loc": {"x": 58000.0, "y": -64500.0, "z": 20.0}, "scale": 1.3},
    # Hakim Chattar Shade Canopy
    {"loc": {"x": 71800.0, "y": -70800.0, "z": 20.0}, "scale": 1.4}
]

for idx, t in enumerate(tree_positions):
    s = t["scale"]
    spawn_landmark(
        f"{FOLIAGE_PATH}/SM_Campus_Tree_Hero.SM_Campus_Tree_Hero",
        f"Campus_HeroTree_{idx+1}",
        "Green_Spaces/Hero_Trees",
        loc=t["loc"],
        scale={"x": s, "y": s, "z": s}
    )

print("\n=== Phase 3 Campus Assembly Complete! ===")
