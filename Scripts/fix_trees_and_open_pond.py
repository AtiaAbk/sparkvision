#!/usr/bin/env python3
"""
Fix Trees & Open Curzon Pond:
1. Removes all artificial barrier/screen Debdaru trees that created the dark wooden palisade wall.
2. Replaces all pond trees with authentic SM_Tree_Krishnachura_Natural and SM_Tree_Debdaru_Natural.
3. Plants natural organic Krishnachura trees framing Curzon Hall promenade.
4. Places properly spaced Debdaru and Banyan trees around the pond perimeter to create an open,
   picturesque botanical pond reflecting the sky and architecture.
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

script = '''
import json

def run():
    KRISHNA_NATURAL = "/Game/SparkVision/Campus/Environment/SM_Tree_Krishnachura_Natural.SM_Tree_Krishnachura_Natural"
    DEBDARU_NATURAL = "/Game/SparkVision/Campus/Environment/SM_Tree_Debdaru_Natural.SM_Tree_Debdaru_Natural"
    BANYAN_NATURAL = "/Game/SparkVision/Campus/Environment/SM_Tree_Banyan_Natural.SM_Tree_Banyan_Natural"
    FLOWERBED_CIRCULAR = "/Game/SparkVision/Campus/Environment/SM_Garden_Flowerbed_Circular.SM_Garden_Flowerbed_Circular"

    deleted_count = 0

    # 1. Find and delete artificial barrier Debdaru trees around the pond
    barrier_patterns = [
        "CurzonPond_EastBank_Debdaru",
        "CurzonPond_SouthBank_Debdaru",
        "CurzonPond_NorthBank_Debdaru",
        "CurzonPond_WestBank_Debdaru",
        "CurzonPond_GapScreen_Debdaru",
        "CurzonPond_Dense_Debdaru",
        "CurzonPond_Lower_Debdaru",
        "CurzonPond_Tier_Debdaru",
        "WWM_Enclosure_Debdaru",
        "WWM_Screen_Debdaru",
        "Pond_Bamboo_Screen",
        "Pond_LowerTrunk_Cover"
    ]

    for pat in barrier_patterns:
        acts = execute_tool("editor_toolset.toolsets.scene.SceneTools.find_actors", json.dumps({
            "name": pat, "tag": "", "collision_channels": []
        }))["returnValue"]
        for a in acts:
            execute_tool("editor_toolset.toolsets.scene.SceneTools.remove_from_scene", json.dumps({
                "actor": {"refPath": a["refPath"]}
            }))
            deleted_count += 1

    # 2. Update CurzonPond_Jarul_* and CurzonPond trees with natural meshes and proper scale
    jarul_acts = execute_tool("editor_toolset.toolsets.scene.SceneTools.find_actors", json.dumps({
        "name": "CurzonPond_Jarul", "tag": "", "collision_channels": []
    }))["returnValue"]

    updated_jarul = 0
    for i, a in enumerate(jarul_acts):
        ref = a["refPath"]
        mesh_to_use = KRISHNA_NATURAL if (i % 2 == 0) else BANYAN_NATURAL
        comps = execute_tool("editor_toolset.toolsets.actor.ActorTools.get_components", json.dumps({
            "actor": {"refPath": ref}
        }))["returnValue"]
        for c in comps:
            if "StaticMeshComponent" in c["refPath"]:
                execute_tool("editor_toolset.toolsets.object.ObjectTools.set_properties", json.dumps({
                    "instance": {"refPath": c["refPath"]},
                    "values": json.dumps({
                        "StaticMesh": {"refPath": mesh_to_use},
                        "overrideMaterials": []
                    })
                }))
                break
        # Reset scale to natural (1.0, 1.0, 1.0)
        execute_tool("editor_toolset.toolsets.actor.ActorTools.set_actor_transform", json.dumps({
            "actor": {"refPath": ref},
            "xform": {"scale": {"x": 1.0, "y": 1.0, "z": 1.0}}
        }))
        updated_jarul += 1

    # 3. Plant 12 naturally spaced Debdaru mast trees along the pond perimeter
    # Pond center is at X=4800, Y=0. Bank perimeter is at X: 2400 to 7200, Y: -1600 to +1600
    natural_debdaru_pond = [
        # North bank (Y = 1600)
        ("Natural_Pond_Debdaru_N1", 3000.0, 1600.0, 20.0, 1.0),
        ("Natural_Pond_Debdaru_N2", 4200.0, 1700.0, 20.0, 1.1),
        ("Natural_Pond_Debdaru_N3", 5400.0, 1650.0, 20.0, 0.95),
        ("Natural_Pond_Debdaru_N4", 6600.0, 1600.0, 20.0, 1.05),
        # South bank (Y = -1600)
        ("Natural_Pond_Debdaru_S1", 3000.0, -1600.0, 20.0, 1.0),
        ("Natural_Pond_Debdaru_S2", 4200.0, -1700.0, 20.0, 1.05),
        ("Natural_Pond_Debdaru_S3", 5400.0, -1650.0, 20.0, 0.95),
        ("Natural_Pond_Debdaru_S4", 6600.0, -1600.0, 20.0, 1.1),
        # East bank (X = 7200)
        ("Natural_Pond_Debdaru_E1", 7200.0, -800.0, 20.0, 1.0),
        ("Natural_Pond_Debdaru_E2", 7200.0, 800.0, 20.0, 1.05),
        # West bank near promenade (X = 2600)
        ("Natural_Pond_Debdaru_W1", 2600.0, -800.0, 20.0, 1.0),
        ("Natural_Pond_Debdaru_W2", 2600.0, 800.0, 20.0, 1.0),
    ]

    for name, x, y, z, sc in natural_debdaru_pond:
        xform = {
            "location": {"x": x, "y": y, "z": z},
            "rotation": {"pitch": 0.0, "yaw": 0.0, "roll": 0.0},
            "scale": {"x": sc, "y": sc, "z": sc}
        }
        execute_tool("editor_toolset.toolsets.scene.SceneTools.add_to_scene_from_asset", json.dumps({
            "asset_path": DEBDARU_NATURAL,
            "name": name,
            "xform": xform
        }))

    # 4. Plant majestic organic Krishnachura bloom trees framing Curzon Hall promenade
    promenade_trees = [
        ("Curzon_Promenade_Krishnachura_North", -2400.0, 800.0, 20.0, 1.1),
        ("Curzon_Promenade_Krishnachura_South", -2400.0, -800.0, 20.0, 1.1),
        ("Curzon_Forecourt_Banyan_North", -2000.0, 1600.0, 20.0, 1.0),
        ("Curzon_Forecourt_Banyan_South", -2000.0, -1600.0, 20.0, 1.0),
        ("Curzon_CentralLawn_Krishnachura_1", -1200.0, 600.0, 20.0, 1.0),
        ("Curzon_CentralLawn_Krishnachura_2", -1200.0, -600.0, 20.0, 1.0),
    ]

    for name, x, y, z, sc in promenade_trees:
        mesh = KRISHNA_NATURAL if "Krishnachura" in name else BANYAN_NATURAL
        xform = {
            "location": {"x": x, "y": y, "z": z},
            "rotation": {"pitch": 0.0, "yaw": 30.0, "roll": 0.0},
            "scale": {"x": sc, "y": sc, "z": sc}
        }
        execute_tool("editor_toolset.toolsets.scene.SceneTools.add_to_scene_from_asset", json.dumps({
            "asset_path": mesh,
            "name": name,
            "xform": xform
        }))

    # 5. Place Circular Flowerbed directly in front of Curzon Promenade Court
    execute_tool("editor_toolset.toolsets.scene.SceneTools.add_to_scene_from_asset", json.dumps({
        "asset_path": FLOWERBED_CIRCULAR,
        "name": "Flowerbed_Curzon_Hero_Promenade",
        "xform": {
            "location": {"x": -2200.0, "y": 0.0, "z": 20.0},
            "rotation": {"pitch": 0.0, "yaw": 0.0, "roll": 0.0},
            "scale": {"x": 1.4, "y": 1.4, "z": 1.2}
        }
    }))

    return {
        "deleted_barrier_trees": deleted_count,
        "updated_jarul": updated_jarul,
        "planted_pond_debdaru": len(natural_debdaru_pond),
        "planted_promenade_trees": len(promenade_trees)
    }
'''

def main():
    print("=" * 70)
    print("FIXING TREES & OPENING CURZON POND")
    print("=" * 70)
    res = invoke_tool("execute_tool_script", "editor_toolset.toolsets.programmatic.ProgrammaticToolset", {
        "script": script
    })
    print("Result:", res.get("returnValue", ""))

if __name__ == "__main__":
    main()
