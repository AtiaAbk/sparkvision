#!/usr/bin/env python3
import json
import subprocess

ENV_PATH = "/Game/SparkVision/Campus/Environment"

def run_mcp(toolset, tool, args):
    res = subprocess.check_output([
        "/Users/atiaoishi/Downloads/sparkvision/Scripts/mcp_client.py",
        "call", toolset, tool, json.dumps(args)
    ])
    return json.loads(res) if res.strip() else {}

def spawn_env_actor(asset_name, actor_name, loc, rot={"pitch": 0.0, "yaw": 0.0, "roll": 0.0}, scale={"x": 1.0, "y": 1.0, "z": 1.0}, folder="Environment/Curzon_Pond"):
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
    print("Spawning Zone 2: Curzon Botanical Pond Ecology at X=-5200, Y=-3800...")
    total_spawned = 0

    # Historic Stepped Brick Pukur Ghat
    ref = spawn_env_actor("SM_Curzon_Pond_Ghat", "Curzon_Pond_MainGhat",
                    loc={"x": -4700.0, "y": -3800.0, "z": 20.0},
                    rot={"pitch": 0.0, "yaw": 0.0, "roll": 0.0},
                    scale={"x": 1.0, "y": 1.0, "z": 1.0},
                    folder="Environment/Curzon_Pond/Pond_Architecture")
    if ref: total_spawned += 1

    # 6 Moisture-loving Purple Jarul trees along the pond margin
    jarul_locs = [
        {"x": -4800.0, "y": -4800.0, "z": 20.0, "yaw": 10.0},
        {"x": -5300.0, "y": -4900.0, "z": 20.0, "yaw": 80.0},
        {"x": -5800.0, "y": -4700.0, "z": 20.0, "yaw": 140.0},
        {"x": -5900.0, "y": -3800.0, "z": 20.0, "yaw": 180.0},
        {"x": -5700.0, "y": -3000.0, "z": 20.0, "yaw": -120.0},
        {"x": -5000.0, "y": -2900.0, "z": 20.0, "yaw": -40.0},
    ]
    for idx, j in enumerate(jarul_locs):
        ref = spawn_env_actor("SM_Tree_Jarul_Purple", f"CurzonPond_Jarul_{idx+1}",
                              loc={"x": j["x"], "y": j["y"], "z": j["z"]},
                              rot={"pitch": 0.0, "yaw": j["yaw"], "roll": 0.0},
                              folder="Environment/Curzon_Pond/Riparian_Trees")
        if ref: total_spawned += 1

    # 6 Leaning Coconut Palms overhanging the water
    palm_locs = [
        {"x": -4750.0, "y": -4400.0, "z": 20.0, "yaw": 25.0},
        {"x": -5100.0, "y": -4950.0, "z": 20.0, "yaw": 75.0},
        {"x": -5600.0, "y": -4850.0, "z": 20.0, "yaw": 115.0},
        {"x": -5950.0, "y": -4100.0, "z": 20.0, "yaw": 165.0},
        {"x": -5850.0, "y": -3300.0, "z": 20.0, "yaw": -135.0},
        {"x": -4850.0, "y": -3200.0, "z": 20.0, "yaw": -45.0},
    ]
    for idx, p in enumerate(palm_locs):
        ref = spawn_env_actor("SM_Tree_Palm_Coconut", f"CurzonPond_Palm_{idx+1}",
                              loc={"x": p["x"], "y": p["y"], "z": p["z"]},
                              rot={"pitch": 0.0, "yaw": p["yaw"], "roll": 0.0},
                              folder="Environment/Curzon_Pond/Riparian_Trees")
        if ref: total_spawned += 1

    # 8 Floating Water Lily (Shapla) clusters on the pond surface (Z = 22)
    lily_locs = [
        {"x": -5000.0, "y": -3600.0, "z": 22.0, "yaw": 15.0},
        {"x": -5150.0, "y": -4000.0, "z": 22.0, "yaw": 45.0},
        {"x": -5300.0, "y": -3700.0, "z": 22.0, "yaw": 85.0},
        {"x": -5500.0, "y": -4100.0, "z": 22.0, "yaw": -30.0},
        {"x": -5650.0, "y": -3800.0, "z": 22.0, "yaw": 120.0},
        {"x": -5250.0, "y": -4300.0, "z": 22.0, "yaw": -70.0},
        {"x": -5400.0, "y": -3400.0, "z": 22.0, "yaw": 60.0},
        {"x": -5100.0, "y": -4200.0, "z": 22.0, "yaw": -110.0},
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
        {"x": -4750.0, "y": -4700.0, "z": 20.0, "yaw": 10.0},
        {"x": -4950.0, "y": -4950.0, "z": 20.0, "yaw": 60.0},
        {"x": -5500.0, "y": -4900.0, "z": 20.0, "yaw": 90.0},
        {"x": -5850.0, "y": -4500.0, "z": 20.0, "yaw": 130.0},
        {"x": -5950.0, "y": -3600.0, "z": 20.0, "yaw": 170.0},
        {"x": -5800.0, "y": -3150.0, "z": 20.0, "yaw": -150.0},
        {"x": -5450.0, "y": -2950.0, "z": 20.0, "yaw": -90.0},
        {"x": -4900.0, "y": -3050.0, "z": 20.0, "yaw": -30.0},
    ]
    for idx, rd in enumerate(reed_locs):
        ref = spawn_env_actor("SM_Plant_Reeds_Kashful", f"CurzonPond_Reeds_{idx+1}",
                              loc={"x": rd["x"], "y": rd["y"], "z": rd["z"]},
                              rot={"pitch": 0.0, "yaw": rd["yaw"], "roll": 0.0},
                              scale={"x": 1.2, "y": 1.2, "z": 1.1},
                              folder="Environment/Curzon_Pond/Wetland_Reeds")
        if ref: total_spawned += 1

    print(f"Spawned {total_spawned}/29 Zone 2 actors.")

    print("\nSaving level...")
    run_mcp("editor_toolset.toolsets.scene.SceneTools", "save_level", {
        "level_path": "/Game/SparkVision/Maps/Campus/LV_Campus_Blockout"
    })
    print("Level saved.")

if __name__ == "__main__":
    main()
