import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

KRISHNACHURA_MESH = "/Game/SparkVision/Campus/Environment/SM_Tree_Krishnachura_WWM.SM_Tree_Krishnachura_WWM"
RAINTREE_MESH = "/Game/SparkVision/Campus/Environment/SM_Tree_Raintree_Avenue.SM_Tree_Raintree_Avenue"
BANYAN_MESH = "/Game/SparkVision/Campus/Environment/SM_Tree_Banyan_Natural.SM_Tree_Banyan_Natural"
DEBDARU_MESH = "/Game/SparkVision/Campus/Environment/SM_Tree_Debdaru_Natural.SM_Tree_Debdaru_Natural"
RANGAN_BUSH = "/Game/SparkVision/Campus/Environment/SM_Bush_Rangan_Scarlet.SM_Bush_Rangan_Scarlet"
KAMINI_BUSH = "/Game/SparkVision/Campus/Environment/SM_Bush_Kamini_Hedge.SM_Bush_Kamini_Hedge"
GRASS_TUFT = "/Game/SparkVision/Campus/Environment/SM_Grass_Tuft_Lawn.SM_Grass_Tuft_Lawn"

foliage_spawns = [
    # Curzon Front Promenade Flanks (eliminating empty lawn patches)
    # Left Lawn (Y: -700 to -1400)
    (KRISHNACHURA_MESH, "Garden_Krishnachura_01", -3900, -750, 10, 30, 1.2),
    (RAINTREE_MESH, "Garden_Raintree_01", -3500, -1100, 10, 60, 1.3),
    (DEBDARU_MESH, "Garden_Debdaru_01", -3100, -650, 10, 10, 1.4),
    (KRISHNACHURA_MESH, "Garden_Krishnachura_02", -2800, -950, 10, -45, 1.1),
    (BANYAN_MESH, "Garden_Banyan_01", -3400, -1500, 10, 90, 1.5),

    # Right Lawn (Y: 700 to 1400)
    (KRISHNACHURA_MESH, "Garden_Krishnachura_03", -3900, 750, 10, -30, 1.2),
    (RAINTREE_MESH, "Garden_Raintree_02", -3500, 1100, 10, -60, 1.3),
    (DEBDARU_MESH, "Garden_Debdaru_02", -3100, 650, 10, -10, 1.4),
    (KRISHNACHURA_MESH, "Garden_Krishnachura_04", -2800, 950, 10, 45, 1.1),
    (BANYAN_MESH, "Garden_Banyan_02", -3400, 1500, 10, -90, 1.5),

    # Promenade Flowerbed Clusters (Rangan Scarlet + Kamini White)
    (RANGAN_BUSH, "Flowerbed_Rangan_01", -3900, -340, 10, 0, 1.5),
    (KAMINI_BUSH, "Flowerbed_Kamini_01", -3700, -340, 10, 20, 1.3),
    (RANGAN_BUSH, "Flowerbed_Rangan_02", -3300, -340, 10, 40, 1.5),
    (KAMINI_BUSH, "Flowerbed_Kamini_02", -2900, -340, 10, 10, 1.4),

    (RANGAN_BUSH, "Flowerbed_Rangan_03", -3900, 340, 10, 0, 1.5),
    (KAMINI_BUSH, "Flowerbed_Kamini_03", -3700, 340, 10, -20, 1.3),
    (RANGAN_BUSH, "Flowerbed_Rangan_04", -3300, 340, 10, -40, 1.5),
    (KAMINI_BUSH, "Flowerbed_Kamini_04", -2900, 340, 10, -10, 1.4),

    # Lawn Grass Tuft accents
    (GRASS_TUFT, "Lawn_Grass_01", -3800, -480, 8, 15, 2.0),
    (GRASS_TUFT, "Lawn_Grass_02", -3400, -480, 8, 45, 2.2),
    (GRASS_TUFT, "Lawn_Grass_03", -3000, -480, 8, -30, 2.1),
    (GRASS_TUFT, "Lawn_Grass_04", -3800, 480, 8, -15, 2.0),
    (GRASS_TUFT, "Lawn_Grass_05", -3400, 480, 8, -45, 2.2),
    (GRASS_TUFT, "Lawn_Grass_06", -3000, 480, 8, 30, 2.1),
]

print("=== POPULATING LUSH GARDENS & AVENUE TREES ===")
for mesh_path, name, x, y, z, yaw, scale in foliage_spawns:
    try:
        invoke_tool("add_to_scene_from_asset", "editor_toolset.toolsets.scene.SceneTools", {
            "asset_path": mesh_path,
            "name": name,
            "xform": {
                "location": {"x": float(x), "y": float(y), "z": float(z)},
                "rotation": {"pitch": 0.0, "yaw": float(yaw), "roll": 0.0},
                "scale": {"x": float(scale), "y": float(scale), "z": float(scale)}
            }
        })
        print(f"  ✓ Spawned {name} at ({x}, {y})")
    except Exception as e:
        print(f"Notice {name}:", e)

