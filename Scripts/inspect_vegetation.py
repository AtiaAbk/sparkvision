#!/usr/bin/env python3
import sys, json
sys.path.insert(0, "Scripts")
from mcp_client import invoke_tool

for kw in ["Tree", "Fern", "WWM"]:
    actors = invoke_tool("find_actors", "editor_toolset.toolsets.scene.SceneTools", {
        "name": kw,
        "tag": "",
        "collision_channels": []
    }).get("returnValue", [])
    print(f"\n--- {kw} ({len(actors)}) ---")
    for a in actors:
        ref = a["refPath"]
        props = invoke_tool("get_properties", "editor_toolset.toolsets.object.ObjectTools", {
            "instance": {"refPath": ref},
            "properties": ["RootComponent"]
        })
        root = json.loads(props.get("returnValue", "{}")).get("RootComponent", {}).get("refPath")
        if not root:
            continue
        xp = invoke_tool("get_properties", "editor_toolset.toolsets.object.ObjectTools", {
            "instance": {"refPath": root},
            "properties": ["RelativeLocation", "RelativeScale3D", "StaticMesh"]
        })
        d = json.loads(xp.get("returnValue", "{}"))
        loc = d.get("RelativeLocation", {})
        mesh = d.get("StaticMesh", {}).get("refPath", "").split(".")[-1]
        scale = d.get("RelativeScale3D", {})
        lx, ly, lz = loc.get("x", 99999), loc.get("y", 99999), loc.get("z", 99999)
        if -4500 <= lx <= 3500 and -2500 <= ly <= 2500:
            name = ref.split(":")[-1]
            sx = scale.get("x")
            print(f"{name}: Mesh={mesh} Loc=({lx:.0f}, {ly:.0f}, {lz:.0f}) Scale={sx}")
