import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

actors = invoke_tool("find_actors", "editor_toolset.toolsets.scene.SceneTools", {"name": "SVStudentNPC", "tag": "", "collision_channels": []}).get("returnValue", [])
if not actors:
    actors = invoke_tool("find_actors", "editor_toolset.toolsets.scene.SceneTools", {"name": "NPC", "tag": "", "collision_channels": []}).get("returnValue", [])

print(f"Total NPC actors queried: {len(actors)}")
for i, a in enumerate(actors):
    lbl = invoke_tool("get_label", "editor_toolset.toolsets.actor.ActorTools", {"actor": a}).get("returnValue", "")
    xform = invoke_tool("get_actor_transform", "editor_toolset.toolsets.actor.ActorTools", {"actor": a}).get("returnValue", {})
    loc = xform.get("location", {})
    print(f"[{i+1}/{len(actors)}] {lbl} -> Loc: ({loc.get('x',0):.0f}, {loc.get('y',0):.0f}, {loc.get('z',0):.0f})")
