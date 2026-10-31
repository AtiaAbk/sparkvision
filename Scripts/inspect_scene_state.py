import sys
import json
sys.path.insert(0, 'Scripts')
from mcp_client import post_mcp

def call(toolset, tool, args=None):
    res = post_mcp("tools/call", {
        "name": "call_tool",
        "arguments": {
            "toolset_name": toolset,
            "tool_name": tool,
            "arguments": args or {}
        }
    })
    if res.get("isError"):
        msg = res.get("content", [{}])[0].get("text", "Unknown tool error")
        raise RuntimeError(f"Error calling {tool}: {msg}")
    txt = res.get("content", [{}])[0].get("text", "{}")
    try:
        return json.loads(txt).get("returnValue")
    except Exception:
        return txt

all_actors = call("editor_toolset.toolsets.scene.SceneTools", "find_actors", {
    "name": "",
    "tag": "",
    "collision_channels": []
})

print(f"Total Actors: {len(all_actors)}")

targets = ["Hero", "Shaheed", "Doyel", "Raju", "TSC", "Library", "Tree", "Player", "Archive", "Opponent"]

matching = []
for a in all_actors:
    try:
        lbl = call("editor_toolset.toolsets.actor.ActorTools", "get_label", {"actor": a})
        for t in targets:
            if t.lower() in lbl.lower():
                xform = call("editor_toolset.toolsets.actor.ActorTools", "get_actor_transform", {"actor": a})
                matching.append((lbl, a["refPath"], xform))
                break
    except Exception as e:
        pass

for lbl, ref, xf in sorted(matching, key=lambda x: x[0]):
    loc = xf.get('location', {})
    rot = xf.get('rotation', {})
    print(f"Actor: {lbl:<35} | Pos: ({loc.get('x',0):>8.1f}, {loc.get('y',0):>8.1f}, {loc.get('z',0):>6.1f}) | Rot: ({rot.get('pitch',0):>5.1f}, {rot.get('yaw',0):>6.1f}, {rot.get('roll',0):>5.1f})")
