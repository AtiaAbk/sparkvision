import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

mesh_path = "/Game/SparkVision/Campus/Environment/SM_Pond_KoiFish.SM_Pond_KoiFish"

fish_spawns = [
    # School swimming near the Ghat pier
    (2480, -80, -3, 30, 1.4),
    (2520, -140, -4, 45, 1.2),
    (2550, -30, -2, 15, 1.5),
    (2580, 100, -3, -40, 1.3),
    (2620, 160, -4, -25, 1.1),
    (2680, 50, -3, -60, 1.4),
    # Cruising among water lilies
    (2800, -320, -4, 80, 1.6),
    (2870, -380, -3, 85, 1.2),
    (2750, 280, -4, -80, 1.3),
    (2900, 340, -5, -105, 1.5),
    # Open water swimmers
    (3100, -90, -5, 135, 1.7),
    (3250, 130, -5, -140, 1.5),
    (3020, 30, -4, 10, 1.2),
    (3380, -60, -6, -165, 1.4),
]

print("Spawning school of swimming fish in Curzon Pond...")
for idx, (x, y, z, yaw, scale) in enumerate(fish_spawns):
    name = f"CurzonPond_KoiFish_{idx+1:02d}"
    try:
        res = invoke_tool("add_to_scene_from_asset", "editor_toolset.toolsets.scene.SceneTools", {
            "asset_path": mesh_path,
            "name": name,
            "xform": {
                "location": {"x": float(x), "y": float(y), "z": float(z)},
                "rotation": {"pitch": 0.0, "yaw": float(yaw), "roll": 0.0},
                "scale": {"x": float(scale), "y": float(scale), "z": float(scale)}
            }
        })
        print(f"  ✓ Spawned {name} at ({x}, {y}, {z})")
    except Exception as e:
        print(f"  Notice spawning {name}: {e}")
