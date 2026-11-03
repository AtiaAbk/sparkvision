import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

actors = invoke_tool("find_actors", "editor_toolset.toolsets.scene.SceneTools", {"name": "Police", "tag": "", "collision_channels": []}).get("returnValue", [])
for a in actors:
    lbl = invoke_tool("get_label", "editor_toolset.toolsets.actor.ActorTools", {"actor": a}).get("returnValue", "")
    xform = invoke_tool("get_actor_transform", "editor_toolset.toolsets.actor.ActorTools", {"actor": a}).get("returnValue", {})
    comps = invoke_tool("get_components", "editor_toolset.toolsets.actor.ActorTools", {"actor": a}).get("returnValue", [])
    print(f"Actor: {lbl}")
    print(f"  Transform: {xform}")
    print(f"  Components: {comps}")
