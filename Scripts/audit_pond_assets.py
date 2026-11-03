#!/usr/bin/env python3
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

def main():
    print("=== AUDITING POND ACTORS IN LEVEL ===")
    
    # 1. Check current level / world
    try:
        current_level = invoke_tool("get_current_level", "editor_toolset.toolsets.scene.SceneTools", {})
        print("Current Level:", json.dumps(current_level, indent=2))
    except Exception as e:
        print("Error getting current level:", e)

    # 2. Find actors with Pond
    pond_actors = invoke_tool("find_actors", "editor_toolset.toolsets.scene.SceneTools", {
        "name": "*Pond*", "tag": "", "collision_channels": []
    }).get("returnValue", [])
    print(f"\nFound {len(pond_actors)} actors matching '*Pond*':")
    for a in pond_actors:
        lbl = invoke_tool("get_label", "editor_toolset.toolsets.actor.ActorTools", {"actor": a}).get("returnValue", "")
        xform = invoke_tool("get_actor_transform", "editor_toolset.toolsets.actor.ActorTools", {"actor": a, "worldspace": True}).get("returnValue", {})
        comps = invoke_tool("get_components", "editor_toolset.toolsets.actor.ActorTools", {"actor": a}).get("returnValue", [])
        print(f" - Ref: {a.get('refPath')} | Label: {lbl}")
        print(f"   Transform: {xform}")
        for c in comps:
            c_props = invoke_tool("get_properties", "editor_toolset.toolsets.object.ObjectTools", {
                "instance": c, "property_names": ["StaticMesh", "OverrideMaterials", "Materials"]
            }).get("returnValue", {})
            print(f"   Comp: {c.get('refPath')} -> Props: {c_props}")

    # 3. Find actors with Water
    water_actors = invoke_tool("find_actors", "editor_toolset.toolsets.scene.SceneTools", {
        "name": "*Water*", "tag": "", "collision_channels": []
    }).get("returnValue", [])
    print(f"\nFound {len(water_actors)} actors matching '*Water*':")
    for a in water_actors:
        lbl = invoke_tool("get_label", "editor_toolset.toolsets.actor.ActorTools", {"actor": a}).get("returnValue", "")
        xform = invoke_tool("get_actor_transform", "editor_toolset.toolsets.actor.ActorTools", {"actor": a, "worldspace": True}).get("returnValue", {})
        comps = invoke_tool("get_components", "editor_toolset.toolsets.actor.ActorTools", {"actor": a}).get("returnValue", [])
        print(f" - Ref: {a.get('refPath')} | Label: {lbl}")
        print(f"   Transform: {xform}")
        for c in comps:
            c_props = invoke_tool("get_properties", "editor_toolset.toolsets.object.ObjectTools", {
                "instance": c, "property_names": ["StaticMesh", "OverrideMaterials", "Materials"]
            }).get("returnValue", {})
            print(f"   Comp: {c.get('refPath')} -> Props: {c_props}")

    # 4. Find actors with Ghat
    ghat_actors = invoke_tool("find_actors", "editor_toolset.toolsets.scene.SceneTools", {
        "name": "*Ghat*", "tag": "", "collision_channels": []
    }).get("returnValue", [])
    print(f"\nFound {len(ghat_actors)} actors matching '*Ghat*':")
    for a in ghat_actors:
        lbl = invoke_tool("get_label", "editor_toolset.toolsets.actor.ActorTools", {"actor": a}).get("returnValue", "")
        xform = invoke_tool("get_actor_transform", "editor_toolset.toolsets.actor.ActorTools", {"actor": a, "worldspace": True}).get("returnValue", {})
        comps = invoke_tool("get_components", "editor_toolset.toolsets.actor.ActorTools", {"actor": a}).get("returnValue", [])
        print(f" - Ref: {a.get('refPath')} | Label: {lbl}")
        print(f"   Transform: {xform}")
        for c in comps:
            c_props = invoke_tool("get_properties", "editor_toolset.toolsets.object.ObjectTools", {
                "instance": c, "property_names": ["StaticMesh", "OverrideMaterials", "Materials"]
            }).get("returnValue", {})
            print(f"   Comp: {c.get('refPath')} -> Props: {c_props}")

if __name__ == "__main__":
    main()
