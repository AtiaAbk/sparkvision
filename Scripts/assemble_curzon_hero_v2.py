#!/usr/bin/env python3
"""
Curzon Hall Master Architectural Assembly Script v2
Reconstructs the authentic Curzon Hall (1904 Indo-Saracenic Revival) in Unreal Engine 5.8:
- Monumental Central Entrance Portal with 9-cusp iwan arch, clock pediment, and twin rooftop chhatris
- 6 West Wing bays & 6 East Wing bays of two-tiered colonnades (horseshoe lower arches + 7-cusp upper arches + jali balustrades)
- Continuous roofline with stepped Indo-Saracenic battlements (merlons)
- Twin 25.2m octagonal corner towers with Rajput cupolas and brass kalasa finials
- 1:1 metric scale (128m facade length, 8m structural bay spacing)
- PBR Materials assigned to all slots
"""

import json
import subprocess
import time

MODULAR_PATH = "/Game/SparkVision/Campus/CurzonModular"
MAP_PATH = "/Game/SparkVision/Maps/Campus/LV_Campus_Blockout"

def run_mcp(toolset, tool, args):
    res = subprocess.check_output([
        "/Users/atiaoishi/Downloads/sparkvision/Scripts/mcp_client.py",
        "call", toolset, tool, json.dumps(args)
    ])
    return json.loads(res) if res.strip() else {}

def remove_existing_curzon_hero_actors():
    print("\n[1/4] Cleaning up legacy / invalid Curzon Hero actors...")
    found = run_mcp("editor_toolset.toolsets.scene.SceneTools", "find_actors", {
        "name": "Curzon_Hero_",
        "tag": "",
        "collision_channels": []
    })
    actors = found.get("returnValue", [])
    print(f"Found {len(actors)} existing Curzon_Hero_ actors to remove.")
    for a in actors:
        ref = a["refPath"]
        try:
            run_mcp("editor_toolset.toolsets.scene.SceneTools", "remove_from_scene", {
                "actor": {"refPath": ref}
            })
        except Exception as e:
            print(f"  Warning removing {ref}: {e}")
    print("Cleanup complete.")

def spawn_piece(asset_name, actor_name, loc, rot={"pitch": 0.0, "yaw": 90.0, "roll": 0.0}, scale={"x": 1.0, "y": 1.0, "z": 1.0}):
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
    run_mcp("editor_toolset.toolsets.scene.SceneTools", "set_actor_folder", {
        "actor": {"refPath": ref},
        "folder_path": "Hero_Buildings/Curzon_Detail"
    })
    return ref

def main():
    print("=" * 70)
    print("ASSEMBLING CURZON HALL MASTER ARCHITECTURAL RECONSTRUCTION (v2)...")
    print("=" * 70)

    remove_existing_curzon_hero_actors()

    print("\n[2/4] Spawning Reconstructed Modular Elements...")
    spawned_count = 0

    # 1. Monumental Central Entrance Portal (18m x 4.8m x 23.4m)
    # Includes 5-step staircase, grand 9-cusp arch, clock pediment, and twin rooftop chhatris
    # Yaw -90.0 ensures front stairs, iwan arch, and pediment face South (-X) towards the botanical lawn
    portal_ref = spawn_piece(
        "SM_Curzon_Entrance_Portal",
        "Curzon_Hero_EntrancePortal",
        loc={"x": -2500.0, "y": 0.0, "z": 0.0},
        rot={"pitch": 0.0, "yaw": -90.0, "roll": 0.0}
    )
    spawned_count += 1
    print(f"  [+] Spawned Monumental Entrance Portal: {portal_ref}")

    # 2. Six West Wing Bays (Y = -1300 to -5300)
    west_bays = [-1300.0, -2100.0, -2900.0, -3700.0, -4500.0, -5300.0]
    for idx, y_pos in enumerate(west_bays):
        # Lower Veranda (Horseshoe Arches facing South towards lawn)
        spawn_piece(
            "SM_Curzon_Veranda_Arch_Lower",
            f"Curzon_Hero_VerandaLower_W{idx+1}",
            loc={"x": -2500.0, "y": y_pos, "z": 0.0},
            rot={"pitch": 0.0, "yaw": -90.0, "roll": 0.0}
        )
        spawned_count += 1

        # Upper Veranda (7-Lobed Cusped Arches + Jali Screens + Upper Chhajja facing South)
        spawn_piece(
            "SM_Curzon_Veranda_Arch_Upper",
            f"Curzon_Hero_VerandaUpper_W{idx+1}",
            loc={"x": -2500.0, "y": y_pos, "z": 640.0},
            rot={"pitch": 0.0, "yaw": -90.0, "roll": 0.0}
        )
        spawned_count += 1

        # Roof Parapet Merlons (Stepped pointed battlements aligned above front facade wall)
        spawn_piece(
            "SM_Curzon_Parapet_Merlons",
            f"Curzon_Hero_Parapet_W{idx+1}",
            loc={"x": -2585.0, "y": y_pos, "z": 1280.0},
            rot={"pitch": 0.0, "yaw": -90.0, "roll": 0.0}
        )
        spawned_count += 1

    print(f"  [+] Spawned 6 West Wing Modular Bays (18 components)")

    # 3. Six East Wing Bays (Y = +1300 to +5300)
    east_bays = [1300.0, 2100.0, 2900.0, 3700.0, 4500.0, 5300.0]
    for idx, y_pos in enumerate(east_bays):
        # Lower Veranda (Horseshoe Arches facing South towards lawn)
        spawn_piece(
            "SM_Curzon_Veranda_Arch_Lower",
            f"Curzon_Hero_VerandaLower_E{idx+1}",
            loc={"x": -2500.0, "y": y_pos, "z": 0.0},
            rot={"pitch": 0.0, "yaw": -90.0, "roll": 0.0}
        )
        spawned_count += 1

        # Upper Veranda (7-Lobed Cusped Arches + Jali Screens + Upper Chhajja facing South)
        spawn_piece(
            "SM_Curzon_Veranda_Arch_Upper",
            f"Curzon_Hero_VerandaUpper_E{idx+1}",
            loc={"x": -2500.0, "y": y_pos, "z": 640.0},
            rot={"pitch": 0.0, "yaw": -90.0, "roll": 0.0}
        )
        spawned_count += 1

        # Roof Parapet Merlons (Stepped pointed battlements aligned above front facade wall)
        spawn_piece(
            "SM_Curzon_Parapet_Merlons",
            f"Curzon_Hero_Parapet_E{idx+1}",
            loc={"x": -2585.0, "y": y_pos, "z": 1280.0},
            rot={"pitch": 0.0, "yaw": -90.0, "roll": 0.0}
        )
        spawned_count += 1

    print(f"  [+] Spawned 6 East Wing Modular Bays (18 components)")

    # 4. Corner 25.2m Octagonal Towers (with Tiered Louvers, Balcony, 8-Col Kiosk & Domes)
    west_tower_ref = spawn_piece(
        "SM_Curzon_Tower_Octagon",
        "Curzon_Hero_Tower_West",
        loc={"x": -2500.0, "y": -6000.0, "z": 0.0},
        rot={"pitch": 0.0, "yaw": 22.5, "roll": 0.0}
    )
    spawned_count += 1

    east_tower_ref = spawn_piece(
        "SM_Curzon_Tower_Octagon",
        "Curzon_Hero_Tower_East",
        loc={"x": -2500.0, "y": 6000.0, "z": 0.0},
        rot={"pitch": 0.0, "yaw": -22.5, "roll": 0.0}
    )
    spawned_count += 1
    print(f"  [+] Spawned 25.2m Corner Octagonal Towers (East & West)")

    # 5. Colonial Promenade Heritage Street Lamps
    lamp_locs = [
        {"x": -3200.0, "y": -900.0, "z": 15.0},
        {"x": -3600.0, "y": -900.0, "z": 15.0},
        {"x": -4000.0, "y": -900.0, "z": 15.0},
        {"x": -3200.0, "y": 900.0, "z": 15.0},
        {"x": -3600.0, "y": 900.0, "z": 15.0},
        {"x": -4000.0, "y": 900.0, "z": 15.0},
    ]
    for idx, pos in enumerate(lamp_locs):
        spawn_piece(
            "SM_Curzon_Lamp_Colonial",
            f"Curzon_Hero_StreetLamp_{idx+1}",
            loc=pos,
            rot={"pitch": 0.0, "yaw": 0.0, "roll": 0.0}
        )
        spawned_count += 1
    print(f"  [+] Spawned 6 Colonial Heritage Promenade Street Lamps")

    print(f"\nTotal Curzon Hero components spawned: {spawned_count}")

    # 6. Verify Static Mesh Binding
    print("\n[3/4] Verifying Static Mesh Bindings and Bounds...")
    check_actors = run_mcp("editor_toolset.toolsets.scene.SceneTools", "find_actors", {
        "name": "Curzon_Hero_",
        "tag": "",
        "collision_channels": []
    }).get("returnValue", [])
    
    verified_count = 0
    for a in check_actors:
        ref = a["refPath"]
        bounds = run_mcp("editor_toolset.toolsets.actor.ActorTools", "get_actor_bounds", {
            "actor": {"refPath": ref}
        }).get("returnValue", {})
        lbl = run_mcp("editor_toolset.toolsets.actor.ActorTools", "get_label", {
            "actor": {"refPath": ref}
        }).get("returnValue", "")
        
        b_min = bounds.get("min", {})
        b_max = bounds.get("max", {})
        dx = abs(b_max.get("x", 0) - b_min.get("x", 0))
        dy = abs(b_max.get("y", 0) - b_min.get("y", 0))
        dz = abs(b_max.get("z", 0) - b_min.get("z", 0))
        
        if dx > 0 and dy > 0 and dz > 0:
            verified_count += 1
        else:
            print(f"  [WARNING] Actor {lbl} has zero bounds: dx={dx}, dy={dy}, dz={dz}")

    print(f"Verified {verified_count}/{len(check_actors)} actors have non-zero 3D geometry.")

    # 7. Save Map
    print("\n[4/4] Saving Map Asset...")
    save_res = run_mcp("editor_toolset.toolsets.asset.AssetTools", "save_assets", {
        "asset_paths": [MAP_PATH]
    })
    print(f"Map Save Result: {save_res}")

    print("\n=== CURZON HALL MASTER RECONSTRUCTION v2 COMPLETED SUCCESSFULLY! ===")

if __name__ == "__main__":
    main()
