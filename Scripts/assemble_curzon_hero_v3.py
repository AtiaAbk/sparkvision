#!/usr/bin/env python3
"""
Curzon Hall Master Architectural Assembly Script v3
Reconstructs the authentic Curzon Hall (Faculty of Science, University of Dhaka, 1904)
matching the user's photographic ground-truth references:
- Full 128m bilateral facade with 12 modular bays (6 West, 6 East)
- Inner corridor walls featuring real colonial wooden double doors, arched glass fanlights,
  and tall multi-pane windows with louvered shutters
- Central portal with 4-corner chhatris + 3 intermediate domed merlons, 6 lancet niches,
  2 rosettes, bracketed chhajja, 3-light cusped central window with white jali screen,
  flanking shuttered windows, recessed vestibule with double doors, and 6-step staircase
- 25.2m corner octagonal towers with tiered shuttered windows, balconies, and Rajput cupolas
- Continuous white pierced jali parapet balustrade along roofline
- Department of Physics authentic blue signboard
- Authentic front landscape: Two iconic tall Royal Palms flanking the entrance,
  low manicured hedge line, clear open lawn with zero wall-clipping trees.
"""

import json
import subprocess
import time

MODULAR_PATH = "/Game/SparkVision/Campus/CurzonModular"
ENV_PATH = "/Game/SparkVision/Campus/Environment"

def run_mcp(toolset, tool, args):
    res = subprocess.check_output([
        "/Users/atiaoishi/Downloads/sparkvision/Scripts/mcp_client.py",
        "call", toolset, tool, json.dumps(args)
    ])
    return json.loads(res) if res.strip() else {}

def remove_existing_curzon_actors():
    print("\n[1/4] Cleaning up existing Curzon Hero & Landscape actors...")
    found = run_mcp("editor_toolset.toolsets.scene.SceneTools", "find_actors", {
        "name": "Curzon_Hero_",
        "tag": "",
        "collision_channels": []
    })
    actors = found.get("returnValue", [])
    print(f"Found {len(actors)} existing Curzon_Hero_ actors to replace.")
    for a in actors:
        ref = a["refPath"]
        try:
            run_mcp("editor_toolset.toolsets.scene.SceneTools", "remove_from_scene", {
                "actor": {"refPath": ref}
            })
        except Exception:
            pass

    # Also clean up old authentic landscape if any
    found_land = run_mcp("editor_toolset.toolsets.scene.SceneTools", "find_actors", {
        "name": "Curzon_Authentic_",
        "tag": "",
        "collision_channels": []
    }).get("returnValue", [])
    for a in found_land:
        try:
            run_mcp("editor_toolset.toolsets.scene.SceneTools", "remove_from_scene", {
                "actor": {"refPath": a["refPath"]}
            })
        except Exception:
            pass
    print("Cleanup complete.")

def spawn_piece(asset_path, actor_name, loc, rot={"pitch": 0.0, "yaw": 90.0, "roll": 0.0}, scale={"x": 1.0, "y": 1.0, "z": 1.0}, folder="Hero_Buildings/Curzon_Detail"):
    res = run_mcp("editor_toolset.toolsets.scene.SceneTools", "add_to_scene_from_asset", {
        "asset_path": asset_path,
        "name": actor_name,
        "xform": {
            "location": loc,
            "rotation": rot,
            "scale": scale
        }
    })
    ref = res.get("returnValue", {}).get("refPath", "")
    if ref:
        run_mcp("editor_toolset.toolsets.scene.SceneTools", "set_actor_folder", {
            "actor": {"refPath": ref},
            "folder_path": folder
        })
    return ref

def main():
    print("=" * 70)
    print("ASSEMBLING CURZON HALL MASTER ARCHITECTURAL RECONSTRUCTION (v3)...")
    print("=" * 70)

    remove_existing_curzon_actors()

    print("\n[2/4] Spawning Reconstructed Modular Elements...")
    spawned_count = 0

    # 1. Monumental Central Entrance Portal (18m x 5.6m x 23.4m)
    # Includes 6-step staircase, grand 9-cusp arch, recessed double doors, 3-light jali window,
    # 6 lancet niches, 2 rosettes, 4 corner chhatris + 3 intermediate domed merlons
    portal_asset = f"{MODULAR_PATH}/SM_Curzon_Entrance_Portal.SM_Curzon_Entrance_Portal"
    portal_ref = spawn_piece(
        portal_asset,
        "Curzon_Hero_EntrancePortal",
        loc={"x": -2500.0, "y": 0.0, "z": 0.0},
        rot={"pitch": 0.0, "yaw": -90.0, "roll": 0.0}
    )
    spawned_count += 1
    print(f"  [+] Spawned Monumental Entrance Portal: {portal_ref}")

    # 2. Six West Wing Bays (Y = -1300 to -5300)
    west_bays = [-1300.0, -2100.0, -2900.0, -3700.0, -4500.0, -5300.0]
    for idx, y_pos in enumerate(west_bays):
        # Lower Veranda (Horseshoe arches, sandstone plinth, colonial doors/fanlights/windows inside)
        spawn_piece(
            f"{MODULAR_PATH}/SM_Curzon_Veranda_Arch_Lower.SM_Curzon_Veranda_Arch_Lower",
            f"Curzon_Hero_VerandaLower_W{idx+1}",
            loc={"x": -2500.0, "y": y_pos, "z": 0.0},
            rot={"pitch": 0.0, "yaw": -90.0, "roll": 0.0}
        )
        spawned_count += 1

        # Upper Veranda (7-lobed cusped arches, white jali balustrade, shuttered windows inside)
        spawn_piece(
            f"{MODULAR_PATH}/SM_Curzon_Veranda_Arch_Upper.SM_Curzon_Veranda_Arch_Upper",
            f"Curzon_Hero_VerandaUpper_W{idx+1}",
            loc={"x": -2500.0, "y": y_pos, "z": 640.0},
            rot={"pitch": 0.0, "yaw": -90.0, "roll": 0.0}
        )
        spawned_count += 1

        # Roofline Parapet (Continuous white pierced jali + miniature domed kiosks)
        spawn_piece(
            f"{MODULAR_PATH}/SM_Curzon_Parapet_Merlons.SM_Curzon_Parapet_Merlons",
            f"Curzon_Hero_Parapet_W{idx+1}",
            loc={"x": -2585.0, "y": y_pos, "z": 1260.0},
            rot={"pitch": 0.0, "yaw": -90.0, "roll": 0.0}
        )
        spawned_count += 1

    print(f"  [+] Spawned 6 West Wing Modular Bays (18 components)")

    # 3. Six East Wing Bays (Y = +1300 to +5300)
    east_bays = [1300.0, 2100.0, 2900.0, 3700.0, 4500.0, 5300.0]
    for idx, y_pos in enumerate(east_bays):
        # Lower Veranda
        spawn_piece(
            f"{MODULAR_PATH}/SM_Curzon_Veranda_Arch_Lower.SM_Curzon_Veranda_Arch_Lower",
            f"Curzon_Hero_VerandaLower_E{idx+1}",
            loc={"x": -2500.0, "y": y_pos, "z": 0.0},
            rot={"pitch": 0.0, "yaw": -90.0, "roll": 0.0}
        )
        spawned_count += 1

        # Upper Veranda
        spawn_piece(
            f"{MODULAR_PATH}/SM_Curzon_Veranda_Arch_Upper.SM_Curzon_Veranda_Arch_Upper",
            f"Curzon_Hero_VerandaUpper_E{idx+1}",
            loc={"x": -2500.0, "y": y_pos, "z": 640.0},
            rot={"pitch": 0.0, "yaw": -90.0, "roll": 0.0}
        )
        spawned_count += 1

        # Roofline Parapet
        spawn_piece(
            f"{MODULAR_PATH}/SM_Curzon_Parapet_Merlons.SM_Curzon_Parapet_Merlons",
            f"Curzon_Hero_Parapet_E{idx+1}",
            loc={"x": -2585.0, "y": y_pos, "z": 1260.0},
            rot={"pitch": 0.0, "yaw": -90.0, "roll": 0.0}
        )
        spawned_count += 1

    print(f"  [+] Spawned 6 East Wing Modular Bays (18 components)")

    # 4. Corner 25.2m Octagonal Towers
    west_tower_ref = spawn_piece(
        f"{MODULAR_PATH}/SM_Curzon_Tower_Octagon.SM_Curzon_Tower_Octagon",
        "Curzon_Hero_Tower_West",
        loc={"x": -2500.0, "y": -6000.0, "z": 0.0},
        rot={"pitch": 0.0, "yaw": 22.5, "roll": 0.0}
    )
    spawned_count += 1

    east_tower_ref = spawn_piece(
        f"{MODULAR_PATH}/SM_Curzon_Tower_Octagon.SM_Curzon_Tower_Octagon",
        "Curzon_Hero_Tower_East",
        loc={"x": -2500.0, "y": 6000.0, "z": 0.0},
        rot={"pitch": 0.0, "yaw": -22.5, "roll": 0.0}
    )
    spawned_count += 1
    print(f"  [+] Spawned 25.2m Corner Octagonal Towers (East & West)")

    # 5. Department of Physics Signboard (Matching Media 4)
    sign_ref = spawn_piece(
        f"{MODULAR_PATH}/SM_Curzon_Sign_Physics.SM_Curzon_Sign_Physics",
        "Curzon_Hero_Sign_Physics",
        loc={"x": -2480.0, "y": 2100.0, "z": 620.0},
        rot={"pitch": 0.0, "yaw": -90.0, "roll": 0.0}
    )
    spawned_count += 1
    print(f"  [+] Spawned Department of Physics Signboard")

    # 6. Authentic Front Landscape (Matching Media 1, 2, 3)
    # The Two Iconic Tall Royal Palms Flanking the Portal
    palm_asset = f"{ENV_PATH}/SM_Tree_Palm_Coconut.SM_Tree_Palm_Coconut"
    spawn_piece(
        palm_asset,
        "Curzon_Authentic_Palm_Left",
        loc={"x": -3350.0, "y": -850.0, "z": 15.0},
        rot={"pitch": 0.0, "yaw": 25.0, "roll": 0.0},
        scale={"x": 1.6, "y": 1.6, "z": 2.1},
        folder="Environment/Curzon_Authentic_Landscape"
    )
    spawned_count += 1

    spawn_piece(
        palm_asset,
        "Curzon_Authentic_Palm_Right",
        loc={"x": -3350.0, "y": 850.0, "z": 15.0},
        rot={"pitch": 0.0, "yaw": -35.0, "roll": 0.0},
        scale={"x": 1.65, "y": 1.65, "z": 2.15},
        folder="Environment/Curzon_Authentic_Landscape"
    )
    spawned_count += 1
    print(f"  [+] Spawned Two Iconic Tall Royal Palms flanking entrance")

    # Low Manicured Boxwood Hedges in front of plinth
    hedge_asset = f"{MODULAR_PATH}/SM_Curzon_Hedge_Low.SM_Curzon_Hedge_Low"
    hedge_ys = [-1400.0, -800.0, 800.0, 1400.0]
    for idx, hy in enumerate(hedge_ys):
        spawn_piece(
            hedge_asset,
            f"Curzon_Authentic_Hedge_{idx+1}",
            loc={"x": -3550.0, "y": hy, "z": 15.0},
            rot={"pitch": 0.0, "yaw": 0.0, "roll": 0.0},
            scale={"x": 1.0, "y": 1.0, "z": 1.0},
            folder="Environment/Curzon_Authentic_Landscape"
        )
        spawned_count += 1
    print(f"  [+] Spawned Low Manicured Hedges along front pathway")

    # 7. Colonial Heritage Street Lamps along promenade
    lamp_asset = f"{MODULAR_PATH}/SM_Curzon_Lamp_Colonial.SM_Curzon_Lamp_Colonial"
    lamp_locs = [
        {"x": -3400.0, "y": -1800.0, "z": 15.0},
        {"x": -3800.0, "y": -1800.0, "z": 15.0},
        {"x": -3400.0, "y": 1800.0, "z": 15.0},
        {"x": -3800.0, "y": 1800.0, "z": 15.0},
    ]
    for idx, pos in enumerate(lamp_locs):
        spawn_piece(
            lamp_asset,
            f"Curzon_Hero_StreetLamp_{idx+1}",
            loc=pos,
            rot={"pitch": 0.0, "yaw": 0.0, "roll": 0.0}
        )
        spawned_count += 1
    print(f"  [+] Spawned Colonial Heritage Promenade Street Lamps")

    print(f"\nTotal components spawned: {spawned_count}")
    print("Curzon Hall v3 hero assembly completed successfully!")

if __name__ == "__main__":
    main()
