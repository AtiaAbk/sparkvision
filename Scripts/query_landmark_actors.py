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

keywords = ["raju", "tsc", "library", "aparajeyo", "doyel", "shaheed", "nazrul"]

found = []
for a in all_actors:
    try:
        lbl = call("editor_toolset.toolsets.actor.ActorTools", "get_label", {"actor": a})
        for kw in keywords:
            if kw in lbl.lower():
                xf = call("editor_toolset.toolsets.actor.ActorTools", "get_actor_transform", {"actor": a})
                # Check root or static mesh component
                comps = call("editor_toolset.toolsets.actor.ActorTools", "get_components", {"actor": a})
                mesh_path = None
                for c in comps:
                    try:
                        props = call("editor_toolset.toolsets.object.ObjectTools", "get_properties", {
                            "instance": c,
                            "properties": ["StaticMesh"]
                        })
                        p_json = json.loads(props) if isinstance(props, str) else props
                        if "StaticMesh" in p_json:
                            mesh_path = p_json["StaticMesh"]
                            break
                    except Exception:
                        pass
                found.append((lbl, a["refPath"], xf, mesh_path))
                break
    except Exception as e:
        pass

print("\n--- Matching Landmark Actors ---")
for lbl, ref, xf, mesh in sorted(found, key=lambda x: x[0]):
    loc = xf.get('location', {})
    rot = xf.get('rotation', {})
    print(f"{lbl:<35} | Pos: ({loc.get('x',0):>8.1f}, {loc.get('y',0):>8.1f}, {loc.get('z',0):>6.1f}) | Mesh: {mesh}")
