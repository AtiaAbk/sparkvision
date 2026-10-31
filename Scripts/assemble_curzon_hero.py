#!/usr/bin/env python3
"""
Assembles the detailed Curzon Hall Hero Architecture in Unreal Engine 5.8
using Unreal MCP tools.
Places modular architectural elements over the verified Curzon Hall footprint
and assigns all actors to 'Hero_Buildings/Curzon_Detail'.
"""

import json
import subprocess

MODULAR_PATH = "/Game/SparkVision/Campus/CurzonModular"

def run_mcp(toolset, tool, args):
    res = subprocess.check_output([
        "/Users/atiaoishi/Downloads/sparkvision/Scripts/mcp_client.py",
        "call", toolset, tool, json.dumps(args)
    ])
    return json.loads(res) if res.strip() else {}

def spawn_modular_piece(asset_name, actor_name, loc, rot={"pitch": 0.0, "yaw": 90.0, "roll": 0.0}, scale={"x": 1.0, "y": 1.0, "z": 1.0}):
    asset_ref = f"{MODULAR_PATH}/{asset_name}.{asset_name}"
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
    # Put into folder
    run_mcp("editor_toolset.toolsets.scene.SceneTools", "set_actor_folder", {
        "actor": {"refPath": ref},
        "folder_path": "Hero_Buildings/Curzon_Detail"
    })
    return ref

print("Assembling Curzon Hall Hero Architecture...")

# 1. Monumental Central Entrance Portal
portal_ref = spawn_modular_piece(
    "SM_Curzon_Entrance_Portal",
    "Curzon_Hero_EntrancePortal",
    loc={"x": -2500.0, "y": 0.0, "z": 0.0},
    rot={"pitch": 0.0, "yaw": 90.0, "roll": 0.0}
)
print("Spawned Entrance Portal:", portal_ref)

# 2. Symmetrical Rooftop Chhatris atop the Central Entrance Portal
c1_ref = spawn_modular_piece(
    "SM_Curzon_Chattri_Dome",
    "Curzon_Hero_PorticoChattri_West",
    loc={"x": -2500.0, "y": -750.0, "z": 2000.0},
    rot={"pitch": 0.0, "yaw": 0.0, "roll": 0.0},
    scale={"x": 0.8, "y": 0.8, "z": 0.8}
)
c2_ref = spawn_modular_piece(
    "SM_Curzon_Chattri_Dome",
    "Curzon_Hero_PorticoChattri_East",
    loc={"x": -2500.0, "y": 750.0, "z": 2000.0},
    rot={"pitch": 0.0, "yaw": 0.0, "roll": 0.0},
    scale={"x": 0.8, "y": 0.8, "z": 0.8}
)
print("Spawned Portico Rooftop Chhatris")

# 3. Two-Tiered Southern Verandas
# West Wing: Y = -1200 to -5200 (6 bays of 8m = 800cm)
west_bays = [-1200.0, -2000.0, -2800.0, -3600.0, -4400.0, -5200.0]
for idx, y_pos in enumerate(west_bays):
    # Lower Veranda (Rusticated Arches)
    spawn_modular_piece(
        "SM_Curzon_Veranda_Arch_Lower",
        f"Curzon_Hero_VerandaLower_W{idx+1}",
        loc={"x": -2500.0, "y": y_pos, "z": 0.0},
        rot={"pitch": 0.0, "yaw": 90.0, "roll": 0.0}
    )
    # Upper Veranda (Cusped Multi-foil Arches + Jali Railing)
    spawn_modular_piece(
        "SM_Curzon_Veranda_Arch_Upper",
        f"Curzon_Hero_VerandaUpper_W{idx+1}",
        loc={"x": -2500.0, "y": y_pos, "z": 700.0},
        rot={"pitch": 0.0, "yaw": 90.0, "roll": 0.0}
    )
    # Roof Parapet Merlons
    spawn_modular_piece(
        "SM_Curzon_Parapet_Merlons",
        f"Curzon_Hero_Parapet_W{idx+1}",
        loc={"x": -2500.0, "y": y_pos, "z": 1400.0},
        rot={"pitch": 0.0, "yaw": 90.0, "roll": 0.0}
    )
print(f"Spawned {len(west_bays)} bays on West Wing Veranda (Ground, Upper, Parapet)")

# East Wing: Y = +1200 to +5200 (6 bays of 8m = 800cm)
east_bays = [1200.0, 2000.0, 2800.0, 3600.0, 4400.0, 5200.0]
for idx, y_pos in enumerate(east_bays):
    # Lower Veranda (Rusticated Arches)
    spawn_modular_piece(
        "SM_Curzon_Veranda_Arch_Lower",
        f"Curzon_Hero_VerandaLower_E{idx+1}",
        loc={"x": -2500.0, "y": y_pos, "z": 0.0},
        rot={"pitch": 0.0, "yaw": 90.0, "roll": 0.0}
    )
    # Upper Veranda (Cusped Multi-foil Arches + Jali Railing)
    spawn_modular_piece(
        "SM_Curzon_Veranda_Arch_Upper",
        f"Curzon_Hero_VerandaUpper_E{idx+1}",
        loc={"x": -2500.0, "y": y_pos, "z": 700.0},
        rot={"pitch": 0.0, "yaw": 90.0, "roll": 0.0}
    )
    # Roof Parapet Merlons
    spawn_modular_piece(
        "SM_Curzon_Parapet_Merlons",
        f"Curzon_Hero_Parapet_E{idx+1}",
        loc={"x": -2500.0, "y": y_pos, "z": 1400.0},
        rot={"pitch": 0.0, "yaw": 90.0, "roll": 0.0}
    )
print(f"Spawned {len(east_bays)} bays on East Wing Veranda (Ground, Upper, Parapet)")

# 4. Corner Octagonal Towers and Rooftop Chhatris
# West Corner Tower
spawn_modular_piece(
    "SM_Curzon_Tower_Octagon",
    "Curzon_Hero_Tower_West",
    loc={"x": -2500.0, "y": -6000.0, "z": 0.0},
    rot={"pitch": 0.0, "yaw": 0.0, "roll": 0.0},
    scale={"x": 1.2, "y": 1.2, "z": 1.2} # 19.2m high
)
spawn_modular_piece(
    "SM_Curzon_Chattri_Dome",
    "Curzon_Hero_TowerChattri_West",
    loc={"x": -2500.0, "y": -6000.0, "z": 1920.0},
    rot={"pitch": 0.0, "yaw": 0.0, "roll": 0.0},
    scale={"x": 1.2, "y": 1.2, "z": 1.2}
)

# East Corner Tower
spawn_modular_piece(
    "SM_Curzon_Tower_Octagon",
    "Curzon_Hero_Tower_East",
    loc={"x": -2500.0, "y": 6000.0, "z": 0.0},
    rot={"pitch": 0.0, "yaw": 0.0, "roll": 0.0},
    scale={"x": 1.2, "y": 1.2, "z": 1.2}
)
spawn_modular_piece(
    "SM_Curzon_Chattri_Dome",
    "Curzon_Hero_TowerChattri_East",
    loc={"x": -2500.0, "y": 6000.0, "z": 1920.0},
    rot={"pitch": 0.0, "yaw": 0.0, "roll": 0.0},
    scale={"x": 1.2, "y": 1.2, "z": 1.2}
)
print("Spawned Corner Octagonal Towers and Corner Chhatris")

# 5. Campus Environment Elements (Promenade Benches and Heritage Street Lamps)
# 4 Heritage colonial street lamps lining the promenade
lamp_positions = [
    {"x": -3400.0, "y": -900.0, "z": 15.0},
    {"x": -3000.0, "y": -900.0, "z": 15.0},
    {"x": -3400.0, "y": 900.0, "z": 15.0},
    {"x": -3000.0, "y": 900.0, "z": 15.0},
    {"x": -2650.0, "y": -1000.0, "z": 15.0},
    {"x": -2650.0, "y": 1000.0, "z": 15.0}
]
for idx, pos in enumerate(lamp_positions):
    spawn_modular_piece(
        "SM_Curzon_Lamp_Colonial",
        f"Curzon_Hero_StreetLamp_{idx+1}",
        loc=pos,
        rot={"pitch": 0.0, "yaw": 0.0, "roll": 0.0},
        scale={"x": 1.0, "y": 1.0, "z": 1.0}
    )
print(f"Spawned {len(lamp_positions)} Heritage Colonial Street Lamps")

# 4 Colonial park benches flanking the manicured lawn walkways
bench_positions = [
    {"pos": {"x": -3300.0, "y": -1100.0, "z": 15.0}, "yaw": 0.0},
    {"pos": {"x": -2900.0, "y": -1100.0, "z": 15.0}, "yaw": 0.0},
    {"pos": {"x": -3300.0, "y": 1100.0, "z": 15.0}, "yaw": 180.0},
    {"pos": {"x": -2900.0, "y": 1100.0, "z": 15.0}, "yaw": 180.0},
]
for idx, b in enumerate(bench_positions):
    spawn_modular_piece(
        "SM_Curzon_Bench_Colonial",
        f"Curzon_Hero_Bench_{idx+1}",
        loc=b["pos"],
        rot={"pitch": 0.0, "yaw": b["yaw"], "roll": 0.0},
        scale={"x": 1.0, "y": 1.0, "z": 1.0}
    )
print(f"Spawned {len(bench_positions)} Colonial Campus Benches")

print("\nCurzon Hall Hero Architecture assembly completed successfully!")
