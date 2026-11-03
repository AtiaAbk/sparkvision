#!/usr/bin/env python3
"""
Comprehensive Campus Ground Surface Audit for SparkVision
Inspects all ground, terrain, roads, pedestrian paths, plazas, and boundaries
across the active University of Dhaka campus level.
Outputs data formatted for Documentation/Environment/Grass/Campus_Ground_Surface_Audit.md.
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

def get_actor_info(actor_ref):
    label = invoke_tool("get_label", "editor_toolset.toolsets.actor.ActorTools", {
        "actor": actor_ref
    }).get("returnValue", "")
    
    xform = invoke_tool("get_actor_transform", "editor_toolset.toolsets.actor.ActorTools", {
        "actor": actor_ref, "worldspace": True
    }).get("returnValue", {})
    
    bounds = invoke_tool("get_actor_bounds", "editor_toolset.toolsets.actor.ActorTools", {
        "actor": actor_ref
    }).get("returnValue", {})
    
    comps = invoke_tool("get_components", "editor_toolset.toolsets.actor.ActorTools", {
        "actor": actor_ref
    }).get("returnValue", [])
    
    mesh_path = ""
    override_mats = []
    for c in comps:
        try:
            c_res = invoke_tool("get_properties", "editor_toolset.toolsets.object.ObjectTools", {
                "instance": c, "properties": ["StaticMesh", "OverrideMaterials"]
            }).get("returnValue", {})
            if isinstance(c_res, str):
                c_res = json.loads(c_res)
            if isinstance(c_res, dict):
                sm = c_res.get("StaticMesh", {})
                if sm:
                    mesh_path = sm.get("refPath", "")
                om = c_res.get("OverrideMaterials", [])
                if om:
                    override_mats = [m.get("refPath") if isinstance(m, dict) else str(m) for m in om]
        except Exception:
            pass
            
    return {
        "ref": actor_ref.get("refPath", ""),
        "label": label,
        "xform": xform,
        "bounds": bounds,
        "mesh": mesh_path,
        "materials": override_mats
    }

def main():
    print("=" * 70)
    print("AUDITING ALL CAMPUS GROUND AND INFRASTRUCTURE SURFACES")
    print("=" * 70)
    
    lvl = invoke_tool("get_current_level", "editor_toolset.toolsets.scene.SceneTools", {}).get("returnValue", "")
    print(f"Active Level: {lvl}")
    
    # 1. Check Landscape Actors
    landscapes = invoke_tool("find_actors", "editor_toolset.toolsets.scene.SceneTools", {
        "name": "", "tag": "", "collision_channels": [],
        "actor_type": {"refPath": "/Script/Landscape.Landscape"}
    }).get("returnValue", [])
    
    proxies = invoke_tool("find_actors", "editor_toolset.toolsets.scene.SceneTools", {
        "name": "", "tag": "", "collision_channels": [],
        "actor_type": {"refPath": "/Script/Landscape.LandscapeStreamingProxy"}
    }).get("returnValue", [])
    
    print(f"Landscape Actors: {len(landscapes)} | LandscapeStreamingProxies: {len(proxies)}")
    
    # 2. Query all StaticMeshActors
    actors = invoke_tool("find_actors", "editor_toolset.toolsets.scene.SceneTools", {
        "name": "", "tag": "", "collision_channels": [],
        "actor_type": {"refPath": "/Script/Engine.StaticMeshActor"}
    }).get("returnValue", [])
    print(f"Total StaticMeshActors in scene: {len(actors)}")
    
    # Filter keywords of interest
    SURFACE_KEYWORDS = [
        "ground", "terrain", "floor", "lawn", "soil", "grass", "road", "path",
        "walk", "plaza", "patio", "courtyard", "ghat", "pond", "basin", "altar",
        "boundary", "green", "flowerbed", "hedge", "annex", "hall", "library",
        "mosque", "monument", "curzon"
    ]
    
    surface_records = []
    
    for a in actors:
        # Check label
        try:
            lbl = invoke_tool("get_label", "editor_toolset.toolsets.actor.ActorTools", {"actor": a}).get("returnValue", "")
        except Exception:
            continue
            
        lbl_lower = lbl.lower()
        if any(k in lbl_lower for k in SURFACE_KEYWORDS):
            info = get_actor_info(a)
            surface_records.append(info)
            print(f"Found surface actor: {lbl}")
            
    print(f"\nTotal surface-relevant actors audited: {len(surface_records)}")
    
    # Save raw audit json
    audit_json_path = "Documentation/Environment/Grass/raw_surface_audit.json"
    os.makedirs(os.path.dirname(audit_json_path), exist_ok=True)
    with open(audit_json_path, "w") as f:
        json.dump({
            "level": lvl,
            "has_landscape": len(landscapes) > 0,
            "surface_actors_count": len(surface_records),
            "surfaces": surface_records
        }, f, indent=2)
        
    print(f"Saved raw surface audit to {audit_json_path}")

if __name__ == "__main__":
    main()
