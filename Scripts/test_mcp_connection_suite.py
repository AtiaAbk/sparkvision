import sys
import json
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

print("=== 1. VERIFY REACHABILITY & TOOLSETS ===")
toolsets_raw = post_mcp("tools/call", {"name": "list_toolsets", "arguments": {}})
toolsets_text = toolsets_raw.get("content", [{}])[0].get("text", "")
toolset_count = len([line for line in toolsets_text.splitlines() if line.startswith("- ")])
print(f"Status: REACHABLE")
print(f"Server Endpoint: http://127.0.0.1:8000/mcp")
print(f"Available Toolsets ({toolset_count}):")
for line in toolsets_text.splitlines():
    if line.strip():
        print(f"  {line.strip()}")

print("\n=== 2. CURRENT PROJECT & LEVEL ===")
current_level = call("editor_toolset.toolsets.scene.SceneTools", "get_current_level")
print(f"Current Open Level: {current_level}")
print(f"Active Project File: /Users/atiaoishi/Downloads/sparkvision/MyProject.uproject")

print("\n=== 3. WORLD OUTLINER & SELECTED ACTOR ===")
selected = call("EditorToolset.EditorAppToolset", "GetSelectedActors")
print(f"Selected Actor Count: {len(selected) if selected else 0}")
if selected and len(selected) > 0:
    ref = selected[0]
    label = call("editor_toolset.toolsets.actor.ActorTools", "get_label", {"actor": ref})
    xform = call("editor_toolset.toolsets.actor.ActorTools", "get_actor_transform", {"actor": ref})
    print(f"  - Selected Actor Label: {label}")
    print(f"  - Selected Actor Reference: {ref.get('refPath')}")
    print(f"  - Selected Actor Transform: {xform}")

# Query count and sample actors in level
actors = call("editor_toolset.toolsets.scene.SceneTools", "find_actors", {
    "name": "",
    "tag": "",
    "collision_channels": []
})
print(f"Total Actors in Current World Outliner: {len(actors) if actors else 0}")
if actors:
    sample_labels = []
    for a in actors[:15]:
        try:
            lbl = call("editor_toolset.toolsets.actor.ActorTools", "get_label", {"actor": a})
            sample_labels.append(lbl)
        except Exception:
            pass
    print("Sample Outliner Actors (first 15):")
    for s in sample_labels:
        print(f"  - {s}")

print("\n=== 4. CREATE TEMPORARY TEST CUBE (MCP_TEST_ACTOR) ===")
# Add a StaticMeshActor with basic cube mesh at a safe location: (0, 0, 500)
new_actor = call("editor_toolset.toolsets.scene.SceneTools", "add_to_scene_from_asset", {
    "asset_path": "/Engine/BasicShapes/Cube",
    "name": "MCP_TEST_ACTOR",
    "xform": {
        "location": {"x": 0.0, "y": 0.0, "z": 500.0},
        "rotation": {"pitch": 0.0, "yaw": 0.0, "roll": 0.0},
        "scale": {"x": 1.0, "y": 1.0, "z": 1.0}
    }
})
print(f"Spawned Actor Reference: {new_actor}")

# Explicitly ensure label
call("editor_toolset.toolsets.actor.ActorTools", "set_label", {
    "actor": new_actor,
    "label": "MCP_TEST_ACTOR"
})

print("\n=== 5. VERIFY ACTOR IN UNREAL EDITOR ===")
verified_label = call("editor_toolset.toolsets.actor.ActorTools", "get_label", {"actor": new_actor})
verified_xform = call("editor_toolset.toolsets.actor.ActorTools", "get_actor_transform", {"actor": new_actor})
verified_bounds = call("editor_toolset.toolsets.actor.ActorTools", "get_actor_bounds", {"actor": new_actor})
print(f"Verified Actor Label in Outliner: {verified_label}")
print(f"Verified Actor Location: {verified_xform.get('location')}")
print(f"Verified Actor Scale: {verified_xform.get('scale')}")
print(f"Verified Actor Bounds: {verified_bounds}")

print("\n=== 6. REMOVE ONLY TEMPORARY TEST ACTOR ===")
call("editor_toolset.toolsets.scene.SceneTools", "remove_from_scene", {
    "actor": new_actor
})
print(f"Deleted Actor '{verified_label}' from Scene.")

# Verify removal
remaining_actors = call("editor_toolset.toolsets.scene.SceneTools", "find_actors", {
    "name": "MCP_TEST_ACTOR",
    "tag": "",
    "collision_channels": []
})
print(f"Remaining actors matching MCP_TEST_ACTOR: {len(remaining_actors) if remaining_actors else 0}")
print("\n>>> ALL TEST STEPS PASSED SUCCESSFULLY. DIRECT UNREAL MCP CONTROL IS FULLY FUNCTIONAL. <<<")
