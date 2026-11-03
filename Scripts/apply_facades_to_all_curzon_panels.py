#!/usr/bin/env python3
"""
Applies authentic architectural facade materials (with doors, windows, arches, and louvers)
to all facade panels and walls across Curzon Hall, Kala Bhaban, and TSC.
"""

import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

MAT_CURZON = "/Game/SparkVision/Materials/MI_Curzon_Facade_ArchedDoorsWindows.MI_Curzon_Facade_ArchedDoorsWindows"
MAT_KALA = "/Game/SparkVision/Materials/MI_KalaBhaban_ModernistFacade.MI_KalaBhaban_ModernistFacade"
MAT_TSC = "/Game/SparkVision/Materials/MI_TSC_ModernistFacade.MI_TSC_ModernistFacade"

def main():
    print("=" * 70)
    print("APPLYING AUTHENTIC ARCHITECTURAL FACADES TO ALL CAMPUS WALL PANELS")
    print("=" * 70)

    actors = invoke_tool("find_actors", "editor_toolset.toolsets.scene.SceneTools", {
        "name": "", "tag": "", "collision_channels": []
    }).get("returnValue", [])

    print(f"Total scene actors: {len(actors)}")

    applied_count = 0
    for a in actors:
        ref = a.get("refPath", "")
        if "StaticMeshActor" not in ref:
            continue

        xform = invoke_tool("get_actor_transform", "editor_toolset.toolsets.actor.ActorTools", {
            "actor": {"refPath": ref}
        }).get("returnValue", {})

        loc = xform.get("location", {})
        x, y, z = loc.get("x", 0), loc.get("y", 0), loc.get("z", 0)

        target_mat = None
        target_name = ""

        # Curzon Hall Facade Panels & Veranda Walls
        if -3600 <= x <= -2300 and -2500 <= y <= 2500 and z >= 50:
            target_mat = MAT_CURZON
            target_name = "Curzon Hall Panel"

        # Kala Bhaban Faculty of Arts
        elif 65000 <= x <= 75000 and -100000 <= y <= -90000 and z >= 50:
            target_mat = MAT_KALA
            target_name = "Kala Bhaban Panel"

        # TSC Complex
        elif 52000 <= x <= 62000 and -68000 <= y <= -58000 and z >= 50:
            target_mat = MAT_TSC
            target_name = "TSC Panel"

        if target_mat:
            comps = invoke_tool("get_components", "editor_toolset.toolsets.actor.ActorTools", {
                "actor": {"refPath": ref}
            }).get("returnValue", [])

            sm_comp = None
            for c in comps:
                if "StaticMeshComponent" in c.get("refPath", ""):
                    sm_comp = c.get("refPath", "")
                    break

            if sm_comp:
                try:
                    invoke_tool("set_properties", "editor_toolset.toolsets.object.ObjectTools", {
                        "instance": {"refPath": sm_comp},
                        "values": json.dumps({
                            "overrideMaterials": [{"refPath": target_mat}]
                        })
                    })
                    applied_count += 1
                    print(f"  ✓ {target_name} at ({x:.0f}, {y:.0f}, {z:.0f}) -> {target_mat.split('.')[-1]}")
                except Exception as e:
                    print(f"  ✗ Error on {ref.split('.')[-1]}: {e}")

    print(f"\nApplied authentic facade material to {applied_count} architectural wall panels!")

    # Save all assets
    try:
        invoke_tool("save_assets", "editor_toolset.toolsets.asset.AssetTools", {
            "asset_paths": []
        })
        print("✅ Successfully saved level assets to disk!")
    except Exception as e:
        print(f"Save notice: {e}")

if __name__ == "__main__":
    main()
