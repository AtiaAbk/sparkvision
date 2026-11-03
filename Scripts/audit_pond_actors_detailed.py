#!/usr/bin/env python3
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

def inspect_actor(a_ref, label_prefix=""):
    lbl = invoke_tool("get_label", "editor_toolset.toolsets.actor.ActorTools", {"actor": a_ref}).get("returnValue", "")
    xform = invoke_tool("get_actor_transform", "editor_toolset.toolsets.actor.ActorTools", {"actor": a_ref, "worldspace": True}).get("returnValue", {})
    comps = invoke_tool("get_components", "editor_toolset.toolsets.actor.ActorTools", {"actor": a_ref}).get("returnValue", [])
    print(f"{label_prefix}[Actor] Label: '{lbl}' | Ref: {a_ref.get('refPath')}")
    loc = xform.get("location", {})
    rot = xform.get("rotation", {})
    scale = xform.get("scale", {})
    print(f"  Transform: Loc=({loc.get('x'):.1f}, {loc.get('y'):.1f}, {loc.get('z'):.1f}), Rot=({rot.get('pitch'):.1f}, {rot.get('yaw'):.1f}, {rot.get('roll'):.1f}), Scale=({scale.get('x'):.2f}, {scale.get('y'):.2f}, {scale.get('z'):.2f})")
    
    for c in comps:
        c_ref = c.get("refPath", "")
        c_name = c_ref.split(".")[-1]
        c_res = invoke_tool("get_properties", "editor_toolset.toolsets.object.ObjectTools", {
            "instance": c, "properties": ["StaticMesh", "OverrideMaterials"]
        }).get("returnValue", {})
        if isinstance(c_res, str):
            try:
                c_props = json.loads(c_res)
            except Exception:
                c_props = {"raw": c_res}
        else:
            c_props = c_res
        print(f"   - Component: {c_name} -> {c_props}")

def main():
    folders = [
        "Environment/Curzon_Pond",
        "Environment/Curzon_Pond/Pond_Architecture",
        "Environment/Curzon_Pond/Aquatic_Flora",
        "Environment/Curzon_Pond/Riparian_Flora",
        "Environment/Curzon_Pond/Fauna"
    ]
    for folder in folders:
        try:
            actors = invoke_tool("get_actors_in_folder", "editor_toolset.toolsets.scene.SceneTools", {"folder_path": folder}).get("returnValue", [])
            print(f"\n================ FOLDER: {folder} ({len(actors)} actors) ================")
            for a in actors:
                inspect_actor(a, " ")
        except Exception as e:
            print(f"\nFolder '{folder}' error: {e}")

if __name__ == "__main__":
    main()
