#!/usr/bin/env python3
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

def main():
    print("=== SCANNING ALL ACTORS IN POND REGION (X: 1500..8000, Y: -2500..2500) ===")
    res = invoke_tool("find_actors", "editor_toolset.toolsets.scene.SceneTools", {
        "name": "", "tag": "", "collision_channels": [],
        "actor_type": {"refPath": "/Script/Engine.StaticMeshActor"}
    })
    actors = res.get("returnValue", [])
    print(f"Total StaticMeshActors: {len(actors)}")

    pond_candidates = []
    for a in actors:
        xform = invoke_tool("get_actor_transform", "editor_toolset.toolsets.actor.ActorTools", {
            "actor": a, "worldspace": True
        }).get("returnValue", {})
        loc = xform.get("location", {})
        lx, ly, lz = loc.get("x", 0), loc.get("y", 0), loc.get("z", 0)

        # Check if in pond area
        if 1500 <= lx <= 8000 and -2500 <= ly <= 2500 and -100 <= lz <= 300:
            lbl = invoke_tool("get_label", "editor_toolset.toolsets.actor.ActorTools", {"actor": a}).get("returnValue", "")
            comps = invoke_tool("get_components", "editor_toolset.toolsets.actor.ActorTools", {"actor": a}).get("returnValue", [])
            mesh_path = ""
            mat_paths = []
            for c in comps:
                c_res = invoke_tool("get_properties", "editor_toolset.toolsets.object.ObjectTools", {
                    "instance": c, "properties": ["StaticMesh", "OverrideMaterials"]
                }).get("returnValue", {})
                if isinstance(c_res, str):
                    try:
                        c_res = json.loads(c_res)
                    except Exception:
                        pass
                if isinstance(c_res, dict):
                    sm = c_res.get("StaticMesh", {})
                    if sm:
                        mesh_path = sm.get("refPath", "")
                    om = c_res.get("OverrideMaterials", [])
                    if om:
                        mat_paths = [m.get("refPath") if isinstance(m, dict) else m for m in om]

            scale = xform.get("scale", {})
            pond_candidates.append({
                "ref": a.get("refPath"),
                "label": lbl,
                "loc": (lx, ly, lz),
                "scale": (scale.get("x"), scale.get("y"), scale.get("z")),
                "mesh": mesh_path,
                "mats": mat_paths
            })

    print(f"\nFound {len(pond_candidates)} actors in pond horizontal/vertical volume:")
    for c in pond_candidates:
        print(f"Label: '{c['label']}' | Loc: ({c['loc'][0]:.1f}, {c['loc'][1]:.1f}, {c['loc'][2]:.1f}) | Scale: ({c['scale'][0]:.2f}, {c['scale'][1]:.2f}, {c['scale'][2]:.2f})")
        print(f"  Mesh: {c['mesh']}")
        print(f"  OverrideMaterials: {c['mats']}")

if __name__ == "__main__":
    main()
