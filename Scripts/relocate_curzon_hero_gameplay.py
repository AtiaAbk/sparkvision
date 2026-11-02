#!/usr/bin/env python3
"""
Relocate Curzon Hall Gameplay Elements & Style Student NPC:
- Positions ArchiveTerminal_archive_01 on the sunny front landing of Curzon Hall
- Positions NPC_Tanvir_Curzon on the veranda facing the player
- Creates and assigns collegiate scholar PBR materials to Tanvir (Navy blazer, khaki trousers)
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

def main():
    print("=" * 60)
    print("POLISHING CURZON HERO GAMEPLAY & NPC AESTHETICS")
    print("=" * 60)

    # 1. Relocate Archive Terminal to front landing
    archives = invoke_tool("find_actors", "editor_toolset.toolsets.scene.SceneTools", {
        "name": "ArchiveTerminal_archive_01",
        "tag": "",
        "collision_channels": []
    }).get("returnValue", [])

    if archives:
        ref = archives[0]["refPath"]
        invoke_tool("set_actor_transform", "editor_toolset.toolsets.actor.ActorTools", {
            "actor": {"refPath": ref},
            "xform": {
                "location": {"x": -3450.0, "y": 240.0, "z": 150.0},
                "rotation": {"pitch": 0.0, "yaw": 180.0, "roll": 0.0},
                "scale": {"x": 1.2, "y": 1.2, "z": 1.2}
            }
        })
        print("  ✓ Relocated ArchiveTerminal_archive_01 to front landing (-3450, 240, 150)")

    # 2. Relocate NPC Tanvir to front veranda
    tanvir_actors = invoke_tool("find_actors", "editor_toolset.toolsets.scene.SceneTools", {
        "name": "NPC_Tanvir_Curzon",
        "tag": "",
        "collision_channels": []
    }).get("returnValue", [])

    if tanvir_actors:
        ref = tanvir_actors[0]["refPath"]
        invoke_tool("set_actor_transform", "editor_toolset.toolsets.actor.ActorTools", {
            "actor": {"refPath": ref},
            "xform": {
                "location": {"x": -3450.0, "y": -240.0, "z": 150.0},
                "rotation": {"pitch": 0.0, "yaw": 180.0, "roll": 0.0},
                "scale": {"x": 1.0, "y": 1.0, "z": 1.0}
            }
        })
        print("  ✓ Relocated NPC_Tanvir_Curzon to front veranda (-3450, -240, 150)")

    # 3. Create Collegiate Student Materials for NPCs
    print("\nCreating Collegiate Student NPC Materials...")
    # Legs (Khaki / Cream trousers)
    try:
        invoke_tool("create", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
            "folder_path": "/Game/Characters/Mannequins/Materials/Manny",
            "asset_name": "MI_Student_KhakiLegs",
            "parent": {"refPath": "/Game/Characters/Mannequins/Materials/Manny/MI_Manny_01_New.MI_Manny_01_New"}
        })
        invoke_tool("set_vector_parameter", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
            "instance": {"refPath": "/Game/Characters/Mannequins/Materials/Manny/MI_Student_KhakiLegs.MI_Student_KhakiLegs"},
            "name": "Paint Tint",
            "value": {"r": 0.65, "g": 0.58, "b": 0.45, "a": 1.0}
        })
        print("  ✓ Created MI_Student_KhakiLegs")
    except Exception as e:
        print(f"  Notice: {e}")

    # Torso (Collegiate Navy Blazer)
    try:
        invoke_tool("create", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
            "folder_path": "/Game/Characters/Mannequins/Materials/Manny",
            "asset_name": "MI_Student_NavyTorso",
            "parent": {"refPath": "/Game/Characters/Mannequins/Materials/Manny/MI_Manny_02_New.MI_Manny_02_New"}
        })
        invoke_tool("set_vector_parameter", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
            "instance": {"refPath": "/Game/Characters/Mannequins/Materials/Manny/MI_Student_NavyTorso.MI_Student_NavyTorso"},
            "name": "Paint Tint",
            "value": {"r": 0.05, "g": 0.08, "b": 0.25, "a": 1.0}
        })
        print("  ✓ Created MI_Student_NavyTorso")
    except Exception as e:
        print(f"  Notice: {e}")

    # Assign to Tanvir SkeletalMeshComponent
    if tanvir_actors:
        ref = tanvir_actors[0]["refPath"]
        comps = invoke_tool("get_components", "editor_toolset.toolsets.actor.ActorTools", {
            "actor": {"refPath": ref}
        }).get("returnValue", [])
        for c in comps:
            c_ref = c["refPath"]
            if "Mesh" in c_ref or "CharacterMesh0" in c_ref:
                try:
                    invoke_tool("set_properties", "editor_toolset.toolsets.object.ObjectTools", {
                        "instance": {"refPath": c_ref},
                        "values": json.dumps({
                            "OverrideMaterials": [
                                {"refPath": "/Game/Characters/Mannequins/Materials/Manny/MI_Student_KhakiLegs.MI_Student_KhakiLegs"},
                                {"refPath": "/Game/Characters/Mannequins/Materials/Manny/MI_Student_NavyTorso.MI_Student_NavyTorso"}
                            ]
                        })
                    })
                    print(f"  ✓ Assigned collegiate materials to {c_ref}")
                except Exception as e:
                    print(f"  Notice setting mesh materials: {e}")

    # Save level & assets
    try:
        invoke_tool("save_assets", "editor_toolset.toolsets.asset.AssetTools", {
            "asset_paths": [
                "/Game/SparkVision/Maps/Level01/LV_Level01_Compact_Campus",
                "/Game/Characters/Mannequins/Materials/Manny/MI_Student_KhakiLegs",
                "/Game/Characters/Mannequins/Materials/Manny/MI_Student_NavyTorso"
            ]
        })
        print("\n✅ Level & Assets saved successfully!")
    except Exception as e:
        print(f"Notice saving: {e}")

if __name__ == "__main__":
    main()
