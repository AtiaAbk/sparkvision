#!/usr/bin/env python3
"""
Spawn full Where Winds Meet environment & combatants in LV_Level01_Compact_Campus:
1. Water Lily & Lotus colonies across Curzon Pond
2. Kashful reeds along pond banks
3. Bamboo groves and thickets along promenades
4. Heritage stone lanterns lining avenues
5. Dragonfly & butterfly wildlife
6. Hostile martial opponents
7. Level save
"""

import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

LILY_MESH = "/Game/SparkVision/Campus/Environment/SM_Pond_WaterLily_Cluster.SM_Pond_WaterLily_Cluster"
REED_MESH = "/Game/SparkVision/Campus/Environment/SM_Plant_Reeds_Kashful.SM_Plant_Reeds_Kashful"
BAMBOO_GROVE_MESH = "/Game/SparkVision/Campus/Environment/SM_Cluster_Bamboo_Grove.SM_Cluster_Bamboo_Grove"
BAMBOO_THICKET_MESH = "/Game/SparkVision/Campus/Environment/SM_Cluster_Bamboo_Thicket.SM_Cluster_Bamboo_Thicket"
LANTERN_MESH = "/Game/SparkVision/Campus/Environment/SM_Curzon_Lantern.SM_Curzon_Lantern"
DRAGONFLY_MESH = "/Game/SparkVision/Campus/Environment/SM_Wildlife_Dragonfly_Pair.SM_Wildlife_Dragonfly_Pair"
BUTTERFLY_MESH = "/Game/SparkVision/Campus/Environment/SM_Wildlife_Butterfly_Cluster.SM_Wildlife_Butterfly_Cluster"
OPPONENT_CLASS = "/Script/MyProject.SVHostileOpponent"

def spawn_mesh(asset_path, name, loc, rot_yaw=0.0, scale=1.0):
    sx = scale if isinstance(scale, (int, float)) else scale[0]
    sy = scale if isinstance(scale, (int, float)) else scale[1]
    sz = scale if isinstance(scale, (int, float)) else scale[2]
    return invoke_tool("add_to_scene_from_asset", "editor_toolset.toolsets.scene.SceneTools", {
        "asset_path": asset_path,
        "name": name,
        "xform": {
            "location": {"x": float(loc[0]), "y": float(loc[1]), "z": float(loc[2])},
            "rotation": {"pitch": 0.0, "yaw": float(rot_yaw), "roll": 0.0},
            "scale": {"x": float(sx), "y": float(sy), "z": float(sz)}
        },
        "snap_to_ground": False
    })

def spawn_actor(actor_class, name, loc, rot_yaw=0.0):
    return invoke_tool("add_to_scene_from_class", "editor_toolset.toolsets.scene.SceneTools", {
        "actor_type": {"refPath": actor_class},
        "name": name,
        "xform": {
            "location": {"x": float(loc[0]), "y": float(loc[1]), "z": float(loc[2])},
            "rotation": {"pitch": 0.0, "yaw": float(rot_yaw), "roll": 0.0},
            "scale": {"x": 1.0, "y": 1.0, "z": 1.0}
        },
        "snap_to_ground": False
    })

def main():
    print("=" * 70)
    print("SPAWNING WHERE WINDS MEET SCENERY & COMBAT IN DU CAMPUS")
    print("=" * 70)

    # 1. Water Lily & Lotus Clusters
    print("\n1. Spawning 14 Water Lily & Lotus colonies across Curzon Pond...")
    lilies = [
        # Near West Shore (close to Ghat)
        (3200, 300, 16.5, 24.0, 1.3),
        (3400, -400, 16.5, 85.0, 1.1),
        (3600, 600, 16.5, 140.0, 1.4),
        # Mid-lake colonies
        (4100, -200, 16.5, 45.0, 1.5),
        (4400, 450, 16.5, 190.0, 1.2),
        (4800, -550, 16.5, 70.0, 1.6),
        (5100, 150, 16.5, 310.0, 1.3),
        (5400, -350, 16.5, 115.0, 1.4),
        # East & Far shore colonies
        (5800, 500, 16.5, 20.0, 1.2),
        (6200, -250, 16.5, 165.0, 1.5),
        (6500, 300, 16.5, 240.0, 1.1),
        # Shallows along banks
        (3800, -1100, 16.5, 55.0, 1.3),
        (4600, 1150, 16.5, 280.0, 1.4),
        (5500, 1100, 16.5, 95.0, 1.2)
    ]
    for i, (x, y, z, yaw, s) in enumerate(lilies, 1):
        spawn_mesh(LILY_MESH, f"WWM_Lily_Colony_{i:02d}", (x, y, z), yaw, s)
    print(f"  ✓ Spawned {len(lilies)} Water Lily colonies.")

    # 2. Reeds & Kashful along shoreline
    print("\n2. Spawning 16 Kashful Reed beds along lake banks...")
    reeds = [
        # South bank
        (3000, -1400, 20.0, 10.0, 1.2),
        (3500, -1450, 20.0, 45.0, 1.4),
        (4000, -1480, 20.0, 80.0, 1.1),
        (4500, -1500, 20.0, 125.0, 1.3),
        (5000, -1480, 20.0, 30.0, 1.5),
        (5500, -1450, 20.0, 95.0, 1.2),
        (6000, -1400, 20.0, 160.0, 1.3),
        (6500, -1350, 20.0, 50.0, 1.1),
        # North bank
        (3000, 1400, 20.0, -20.0, 1.3),
        (3500, 1450, 20.0, 60.0, 1.2),
        (4000, 1480, 20.0, 110.0, 1.5),
        (4500, 1500, 20.0, -75.0, 1.1),
        (5000, 1480, 20.0, 40.0, 1.4),
        (5500, 1450, 20.0, 130.0, 1.3),
        (6000, 1400, 20.0, -45.0, 1.2),
        (6500, 1350, 20.0, 85.0, 1.4)
    ]
    for i, (x, y, z, yaw, s) in enumerate(reeds, 1):
        spawn_mesh(REED_MESH, f"WWM_Reeds_{i:02d}", (x, y, z), yaw, s)
    print(f"  ✓ Spawned {len(reeds)} Kashful Reed beds.")

    # 3. Bamboo Groves & Thickets
    print("\n3. Spawning Bamboo groves along promenades...")
    bamboos = [
        (2200, 700, 25.0, 35.0, 1.3, BAMBOO_GROVE_MESH),
        (2200, -700, 25.0, 110.0, 1.3, BAMBOO_THICKET_MESH),
        (1800, 1100, 25.0, 75.0, 1.4, BAMBOO_GROVE_MESH),
        (1800, -1100, 25.0, -40.0, 1.4, BAMBOO_THICKET_MESH),
        (6800, 800, 25.0, 20.0, 1.3, BAMBOO_THICKET_MESH),
        (6800, -800, 25.0, -60.0, 1.3, BAMBOO_GROVE_MESH)
    ]
    for i, (x, y, z, yaw, s, mesh) in enumerate(bamboos, 1):
        spawn_mesh(mesh, f"WWM_Bamboo_{i:02d}", (x, y, z), yaw, s)
    print(f"  ✓ Spawned {len(bamboos)} Bamboo groves.")

    # 4. Heritage Stone Lanterns
    print("\n4. Spawning Heritage Stone Lanterns along Curzon Avenue...")
    lanterns = [
        (-2800, 200, 25.0), (-2800, -200, 25.0),
        (-2000, 200, 25.0), (-2000, -200, 25.0),
        (-1200, 200, 25.0), (-1200, -200, 25.0),
        (-400, 200, 25.0),  (-400, -200, 25.0),
        (400, 200, 25.0),   (400, -200, 25.0),
        (1200, 200, 25.0),  (1200, -200, 25.0),
        (2000, 200, 25.0),  (2000, -200, 25.0),
        (2650, 280, 25.0),  (2650, -280, 25.0)
    ]
    for i, (x, y, z) in enumerate(lanterns, 1):
        spawn_mesh(LANTERN_MESH, f"WWM_StoneLantern_{i:02d}", (x, y, z), 0.0, 1.0)
    print(f"  ✓ Spawned {len(lanterns)} Heritage Stone Lanterns.")

    # 5. Wildlife
    print("\n5. Spawning Dragonfly & Butterfly clusters...")
    dragonflies = [
        (3500, 200, 38.0, 45.0),
        (4500, -300, 38.0, 120.0),
        (5400, 350, 38.0, 210.0)
    ]
    for i, (x, y, z, yaw) in enumerate(dragonflies, 1):
        spawn_mesh(DRAGONFLY_MESH, f"WWM_Dragonfly_{i:02d}", (x, y, z), yaw, 1.0)

    butterflies = [
        (2100, 600, 55.0, 30.0),
        (2100, -600, 55.0, 150.0)
    ]
    for i, (x, y, z, yaw) in enumerate(butterflies, 1):
        spawn_mesh(BUTTERFLY_MESH, f"WWM_Butterfly_{i:02d}", (x, y, z), yaw, 1.0)
    print(f"  ✓ Spawned wildlife.")

    # 6. Hostile Martial Opponents
    print("\n6. Spawning Hostile Martial Opponents on campus grounds...")
    opponents = [
        ("WWM_Martial_Opponent_Promenade", (800.0, 0.0, 120.0), 180.0),
        ("WWM_Martial_Opponent_Lakeside", (2300.0, -120.0, 120.0), 180.0),
    ]
    for name, loc, yaw in opponents:
        spawn_actor(OPPONENT_CLASS, name, loc, yaw)
    print(f"  ✓ Spawned {len(opponents)} Hostile Martial Opponents.")

    # 7. Save the level asset
    print("\n7. Saving level assets...")
    invoke_tool("save_assets", "editor_toolset.toolsets.asset.AssetTools", {
        "asset_paths": ["/Game/SparkVision/Maps/Level01/LV_Level01_Compact_Campus"]
    })
    print("  ✓ Level saved successfully.")

    print("\n" + "=" * 70)
    print("WWM ENVIRONMENT & COMBATANTS SUCCESSFULLY POPULATED!")
    print("=" * 70)

if __name__ == "__main__":
    main()
